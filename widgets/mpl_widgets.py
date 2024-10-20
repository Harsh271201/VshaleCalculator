
from PyQt5.QtWidgets import QVBoxLayout,QWidget ,QTableWidget,QComboBox,QTableWidgetItem,QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore , QtGui ,QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import pandas as pd 
from typing import List

class MplCanvas(FigureCanvas):
    def __init__(self,fig,parent=None,):
        super(MplCanvas, self).__init__(fig)


class MplWidgetMltrk(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.var_names = []
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas)
        self.vlayout.addWidget(self.toolbar)
        self.setLayout(self.vlayout)
        self.data = None
        
    
    def set_dataframe(self,data : pd.DataFrame ,color_map : str = 'tab10'):
        self.figure.clear()
        self.data = data
        self.columns = list(self.data.columns)
        self.depth_col = self.columns[0]

        self.depthmax = np.max(self.data[self.depth_col].values)
        self.depthmin = np.min(self.data[self.depth_col].values)
        self.cmap = plt.cm.get_cmap(color_map ,len(self.columns))
        plot_colors = {}
        for i in range(len(self.columns)):
            plot_colors[self.columns[i]] = self.cmap(i)
        self.plot_colors =plot_colors
    
    def perform_plotting(self,plotting_curve : List[str] , curve_for_semilog : List[str] = None):
        if self.data is not None:
            self.figure.clear()
            n_vars = len(plotting_curve)
            if n_vars:
                ax = self.figure.add_subplot(1, n_vars, 1)  
                for i, var_name in enumerate(plotting_curve):
                    if i > 0:
                        ax = self.figure.add_subplot(1, n_vars, i + 1, sharey=ax)
                    color = self.plot_colors[var_name]
                    ax.plot(self.data[var_name],self.data[self.depth_col],color = color)
                    ax.xaxis.set_label_position('top')
                    xlabel_ax = var_name
                    ax.set_xlabel(xlabel_ax,color=color)
                    ax.tick_params(axis='x', colors=color)
                    ax.spines['top'].set_edgecolor(color)
                    ax.set_ylim(self.depthmax,self.depthmin)
                    ax.grid(visible=True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
                    # if i != 0 :
                    #     ax.set_yticklabels([])
                    #     ax.set_ylabel('')
                    #     ax.set_yticks([])
                    if i == 0:
                        ax.set_ylabel('Depth')
                                            
                    if curve_for_semilog:
                        if var_name in curve_for_semilog:
                            try:
                                ax.set_xscale('log')
                            except Exception as e:
                                print(f"Error in semilogx for {var_name} : {e}")
                self.figure.tight_layout()
                self.canvas.draw()

        
class agecombo(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(['Linear','Larinor_older','Larinor_tertiary','Clavier','Stieber'])
class sandshalespinbox(QDoubleSpinBox):
   def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximum(500)
        self.setMinimum(0.1)
        self.setSingleStep(0.1)


class VshaletableModel(QTableWidget):
    def __init__(self, vshwidget):
        super().__init__()
        header_item_list = ['zones', 'Top', 'Bottom', 'Age correction', 'Sand line', 'Shale line']
        self.setColumnCount(len(header_item_list))
        self.setHorizontalHeaderLabels(header_item_list)
        self.header_item_list = header_item_list
        self.vshwidget = vshwidget
        self.num_zones = len(self.vshwidget.depth_boundaries_gr) - 1
        self.setRowCount(self.num_zones)
        self.populating_table()

    def populating_table(self):
        self.agecombobox_list = []
        self.sandspinbox_list = []
        self.shalespinbox_list = []
        self.zone_gr_list = []
        for i in range(self.num_zones):
            condition = (self.vshwidget.depth_boundaries_gr[i] <= self.vshwidget.data[self.vshwidget.selected_column_DEPTH]) & (self.vshwidget.depth_boundaries_gr[i+1] >= self.vshwidget.data[self.vshwidget.selected_column_DEPTH])
            pmax = np.percentile(self.vshwidget.gammaray[condition], self.vshwidget.sand_shale_lines[i][1])
            pmin = np.percentile(self.vshwidget.gammaray[condition], self.vshwidget.sand_shale_lines[i][0])
            self.zone_gr_list.append(self.vshwidget.gammaray[condition])
            for j in range(len(self.header_item_list)):
                if self.header_item_list[j] == 'Age correction':
                    agecombobox = agecombo(self)
                    self.agecombobox_list.append(agecombobox)
                    agecombobox.setCurrentText(self.vshwidget.age_correction[i])
                    self.setCellWidget(i, j, agecombobox)
                elif self.header_item_list[j] == 'zones':
                    self.setItem(i, j, QTableWidgetItem(str(i+1)))
                elif self.header_item_list[j] == 'Top':
                    self.setItem(i, j, QTableWidgetItem(str(np.round(self.vshwidget.depth_boundaries_gr[i],2))))
                elif self.header_item_list[j] == 'Bottom':
                    self.setItem(i, j, QTableWidgetItem(str(np.round(self.vshwidget.depth_boundaries_gr[i+1],2))))
                elif self.header_item_list[j] == 'Sand line':
                    sandspinbox = sandshalespinbox(self)
                    sandspinbox.setValue(pmin)
                    self.sandspinbox_list.append(sandspinbox)
                    self.setCellWidget(i, j, sandspinbox)
                elif self.header_item_list[j] == 'Shale line':
                    shalespinbox = sandshalespinbox(self)
                    shalespinbox.setValue(pmax)
                    self.shalespinbox_list.append(shalespinbox)
                    self.setCellWidget(i, j, shalespinbox)




from utils.vshaleCalculation import VshaleCalculator
class VshaleMplwidget(QWidget):
    zone_split = pyqtSignal(VshaletableModel)
    def __init__(self,data,selected_column_depth ,parent = None):
        super().__init__(parent=parent)
        self.vshcal = VshaleCalculator(data, selected_column_depth)
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.selected_column_DEPTH = selected_column_depth
        self.fig, self.axes = plt.subplots(ncols=4, figsize=(10, 10), gridspec_kw={'width_ratios': [0.3, 1, 1, 1]})
        self.canvas = FigureCanvas(self.fig)
        self.navigation = NavigationToolbar(self.canvas, self)
        self.navigation.setIconSize(QtCore.QSize(20, 20))
        
        self.vlayout.addWidget(self.navigation)
        self.vlayout.addWidget(self.canvas)
        
        
        self.colunm_gr = None
        self.column_phi1 = None
        self.column_phi2 = None
        self.phi1sh = None
        self.phi2sh = None
        self.update_plot()
        
    def zone_split_singal_emitted(self):
        table = VshaletableModel(self.vshcal)
        self.zone_split.emit(table)
    
    def clear_layout(self,layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def gammaray_plot(self,colunm_gr):
        self.vshcal.vshale_gr(colunm_gr=colunm_gr)
        #self.data[self.colunm_gr].plot.line(y=self.selected_column_DEPTH,ax=self.axes[1], color='red')
        self.colunm_gr = colunm_gr
        self.axes[1].plot(self.vshcal.data[self.colunm_gr] ,self.vshcal.data[self.selected_column_DEPTH] , color = 'red')
        xlabel_gr = colunm_gr
        self.axes[1].set_xlabel(xlabel_gr , color='red')
        self.axes[1].tick_params(axis='x', colors='red')
        self.sand_lines = {}
        self.shale_lines = {}
        if len(self.vshcal.depth_boundaries_gr)-1==len(self.vshcal.sand_shale_lines):
            n=len(self.vshcal.depth_boundaries_gr)-1
            cmap = plt.cm.get_cmap('rainbow', n)
            for i in range(len(self.vshcal.depth_boundaries_gr)-1):
                condition=(self.vshcal.depth_boundaries_gr[i]<=self.vshcal.data[self.selected_column_DEPTH]) & (self.vshcal.depth_boundaries_gr[i+1]>=self.vshcal.data[self.selected_column_DEPTH])
                pmax = np.percentile(self.vshcal.gammaray[condition],self.vshcal.sand_shale_lines[i][1])
                pmin = np.percentile(self.vshcal.gammaray[condition],self.vshcal.sand_shale_lines[i][0])
                self.shale_lines[str(i+1)]=self.axes[1].plot([pmax, pmax], [self.vshcal.depth_boundaries_gr[i],self.vshcal.depth_boundaries_gr[i+1]], color='gray', linewidth=2, label='Shale line')[0]
                self.sand_lines[str(i+1)]=self.axes[1].plot([pmin, pmin], [self.vshcal.depth_boundaries_gr[i],self.vshcal.depth_boundaries_gr[i+1]], color='yellow', linewidth=2, label='Sand line')[0]
                self.axes[1].axhline(y=self.vshcal.depth_boundaries_gr[i+1], color='k', linestyle='--')
                self.axes[0].fill_betweenx(self.vshcal.data[self.selected_column_DEPTH], 0, 1, where=condition, facecolor=cmap(i), alpha=0.5)
                self.axes[0].axhline(y=self.vshcal.depth_boundaries_gr[i+1], color='k', linestyle='--')
                self.axes[0].text(0, (self.vshcal.depth_boundaries_gr[i]+self.vshcal.depth_boundaries_gr[i+1])/2,self.vshcal.age_correction[i],fontsize=10,color='k',rotation=90)
            #self.data['Vsh_GR'].plot.line(y=self.selected_column_DEPTH, ax=self.axes[3],color='green')
            self.axes[3].plot(self.vshcal.data['Vsh_GR'],self.vshcal.data[self.vshcal.selected_column_DEPTH],color='green')
            xlabel_sh = 'Vsh_GR'
            self.axes[3].set_xlabel(xlabel_sh , color='green')
            self.axes[3].tick_params(axis='x', colors='green')
            
    def set_porosity_args(self,phi1,phi1sh,phi2,phi2sh):
        self.column_phi1 = phi1
        self.phi1sh = phi1sh
        self.column_phi2 = phi2
        self.phi2sh = phi2sh

    def porosity_plot(self,phi1,phi1sh,phi2,phi2sh):
        self.vshcal.vsh_phi(selected_column_phi1=phi1,phi1sh=phi1sh,selected_column_phi2=phi2,phi2sh=phi2sh)
        axes0=self.axes[2].twiny()        
        self.axes[2].plot(self.vshcal.data[self.column_phi1],self.vshcal.data[self.selected_column_DEPTH] ,color='red' )   
        axes0.plot(self.vshcal.data[self.column_phi2],self.vshcal.data[self.selected_column_DEPTH] ,color='blue')
        xlabel_phi1 = self.column_phi1
        self.axes[2].set_xlabel(xlabel_phi1, color='red')
        xlabel_phi2 = self.column_phi2
        axes0.set_xlabel(xlabel_phi2, color='blue')
        self.axes[2].tick_params(axis='x', colors='red')
        axes0.tick_params(axis='x', colors='blue')
        self.axes[2].spines['top'].set_position(("axes", 1))
        axes0.spines['top'].set_position(("axes", 1.04))
        self.axes[2].xaxis.set_ticks_position('top')
        self.axes[2].xaxis.set_label_position('top')
        max_phi=np.max([np.max(self.vshcal.data[self.column_phi1]),np.max(self.vshcal.data[self.column_phi2])])
        min_phi=np.min([np.min(self.vshcal.data[self.column_phi1]),np.min(self.vshcal.data[self.column_phi2])])
        self.axes[2].set_xlim(max_phi+0.2,min_phi-0.2)
        axes0.set_xlim(max_phi+0.2,min_phi-0.2)
        condition_1 = self.vshcal.data[self.column_phi1] > self.vshcal.data[self.column_phi2]
        condition_2=  self.vshcal.data[self.column_phi1] < self.vshcal.data[self.column_phi2]
        self.axes[2].fill_betweenx(self.vshcal.data[self.selected_column_DEPTH], self.vshcal.data[self.column_phi1],
              self.vshcal.data[self.column_phi2], where=condition_1, facecolor='yellow', alpha=0.5)
        self.axes[2].fill_betweenx(self.vshcal.data[self.selected_column_DEPTH], self.vshcal.data[self.column_phi1],
              self.vshcal.data[self.column_phi2], where=condition_2, facecolor='grey', hatch='xxx', alpha=0.8)
        axes3 = self.axes[3].twiny()
        axes3.plot(self.vshcal.data['Vsh_phi'],self.vshcal.data[self.selected_column_DEPTH] ,color='blue' )
        xlabel_Vsh_phi = 'Vsh_phi'
        axes3.set_xlabel(xlabel_Vsh_phi , color='blue')
        axes3.tick_params(axis='x', colors='blue')
        axes3.spines['top'].set_position(("axes", 1.04))
        #axes[1].set_xlim(-0.15,1.15)
        self.axes[2].plot([self.phi1sh,self.phi1sh], [self.vshcal.depth_boundaries_phi[0],self.vshcal.depth_boundaries_phi[-1]], color='k', linewidth=2, label=self.column_phi1+'_shale')
        axes0.plot([self.phi2sh, self.phi2sh], [self.vshcal.depth_boundaries_phi[0],self.vshcal.depth_boundaries_phi[-1]], color='yellow', linewidth=2, label=self.column_phi2+'_shale')
        self.fig.canvas.draw()
        
        
    def update_plot(self):
        print(2.1)
        self.clear_layout(self.vlayout)
        print(2.2)
        self.fig,self.axes = plt.subplots(ncols=4,figsize=(10,10),gridspec_kw={'width_ratios': [0.3,1,1,1]})
        plt.subplots_adjust(wspace=0)
        self.axes[0].set_xticklabels([])
        self.axes[0].set_xticks([])
        for i in range(3):
            self.axes[i+1].xaxis.set_ticks_position('top')
            self.axes[i+1].xaxis.set_label_position('top')
            self.axes[i+1].spines['top'].set_position(("axes", 1))
            self.axes[i+1].grid()
            self.axes[i+1].set_ylim(self.vshcal.depth_boundaries_gr[-1],self.vshcal.depth_boundaries_gr[0])
        self.axes[0].set_ylim(self.vshcal.depth_boundaries_gr[-1],self.vshcal.depth_boundaries_gr[0])
        self.canvas = FigureCanvas(figure=self.fig)
        self.navigation = NavigationToolbar(self.canvas)
        self.navigation.setIconSize(QtCore.QSize(20, 20))
        self.vlayout.addWidget(self.navigation)
        self.vlayout.addWidget(self.canvas)
        #self.setLayout(self.layout)
        #self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #self.canvas.updateGeometry()
        self.enable_interaction()
        if self.colunm_gr is not None:
            self.gammaray_plot(colunm_gr=self.colunm_gr)
   
        if all(attr is not None for attr in [self.column_phi1, self.column_phi2, self.phi1sh, self.phi2sh]):
            self.porosity_plot(self.column_phi1,self.phi1sh,self.column_phi2,self.phi2sh)
            
        self.fig.subplots_adjust(top=0.9, 
                         bottom=0.03, 
                         left=0.065, 
                         right=0.965, 
                         hspace=0.2, 
                         wspace=0.0)
        self.fig.canvas.draw()
        

    def on_axes_enter(self, event):
        ax = event.inaxes
        if ax is not None:
            return ax
        else:
            return None

    def on_click_left(self, event):
        self.zone_split_singal_emitted()
        ax = self.on_axes_enter(event)
        if event.button == 1 and ax == self.axes[0]: 
            y = event.ydata
            if y is not None:
                self.vshcal.adding_zone_gr(depth=y)
                self.vshcal.vshale_gr(colunm_gr=self.colunm_gr)
                plt.close('all')
                self.update_plot()
                
    def on_click_right(self, event):
        self.zone_split_singal_emitted()
        ax = self.on_axes_enter(event)
        if event.button == 3 and ax == self.axes[0]:  
            y = event.ydata
            if y is not None:
                self.vshcal.deleting_zone_gr(depth=y)
                self.vshcal.vshale_gr(colunm_gr=self.colunm_gr)
                plt.close('all')
                self.update_plot()
    
    def enable_interaction(self):
        self.cid_left = self.canvas.mpl_connect('button_press_event', self.on_click_left)
        self.cid_right = self.canvas.mpl_connect('button_press_event', self.on_click_right)
        self.cid_axes_enter = [
            self.axes[0].figure.canvas.mpl_connect('axes_enter_event', self.on_axes_enter),
            self.axes[1].figure.canvas.mpl_connect('axes_enter_event', self.on_axes_enter),
            self.axes[2].figure.canvas.mpl_connect('axes_enter_event', self.on_axes_enter),
            self.axes[3].figure.canvas.mpl_connect('axes_enter_event', self.on_axes_enter)
        ]
        

    def disable_interaction(self):
        if self.cid_left is not None:
            self.canvas.mpl_disconnect(self.cid_left)
            self.cid_left = None
        if self.cid_right is not None:
            self.canvas.mpl_disconnect(self.cid_right)
            self.cid_right = None
        for i in range(4):
            if self.cid_axes_enter[i] is not None:
                self.axes[i].figure.canvas.mpl_disconnect(self.cid_axes_enter[i])
                self.cid_axes_enter[i] = None
                
                

