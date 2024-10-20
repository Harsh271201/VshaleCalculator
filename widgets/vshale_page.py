from PyQt5 import QtWidgets ,  QtGui , QtCore
import typing 
from typing import List, Tuple, Dict, Any , Callable
import pandas as pd
from UI import Ui_vShaleForm
import numpy as np
from .mpl_widgets import VshaleMplwidget , VshaletableModel
from scipy import stats

class VshalePage(QtWidgets.QWidget,Ui_vShaleForm):
    def __init__(self, parent=None):
        super(VshalePage, self).__init__(parent)
        self.setupUi(self)
        self.nphi_col =None 
        self.nphi_col =None
        self.gr_col = None
        self.first_file = True
    
    def set_data(self,data : pd.DataFrame , selected_column_DEPTH : str):
        if hasattr(self, 'vshwidget'):
            if hasattr(self.vshwidget, 'fig'):
                self.vshwidget.fig.clear()
            
        self.data = data
        self.depth_column = selected_column_DEPTH
        self.gammacombo.clear()
        self.dphicombo.clear()
        self.nphicombo.clear()
        self.gammacombo.addItems(['Select'] + list(data.columns))
        self.dphicombo.addItems(['Select'] + list(data.columns))
        self.nphicombo.addItems(['Select'] + list(data.columns))
        if self.first_file:
            self.nphicombo.currentTextChanged.connect(self.setting_up_nphi)
            self.dphicombo.currentTextChanged.connect(self.setting_up_dphi)
            self.gammacombo.currentTextChanged.connect(self.setting_up_gr)
            self.vshiPushButton.clicked.connect(self.vsh_push_button_clicked)
            self.vshgreditButton.clicked.connect(self.gredit_button_checked)        
            self.vshgr_zone_donebutton.clicked.connect(self.vshalegr_done_button_clicked)
            self.first_file = False
    
    
    def setting_up_dphi(self,name):
        if name != 'Select':
            self.dphi_col = name
           
    def setting_up_nphi(self,name):
        if name != 'Select':    
            self.nphi_col = name
    

    def setting_up_gr(self,name):
        if name!= 'Select':
            self.gr_col = name
            print(self.gr_col)

    def vsh_push_button_clicked(self):
        print(self.gr_col)
        if hasattr(self, 'vshwidget'):
           pass
        else:
            self.vshwidget=VshaleMplwidget(self.data,self.depth_column)
            self.vshwidget.zone_split.connect(self.zone_table_maker)
            self.Vshale_scroll_area.setWidget(self.vshwidget)
        if self.nphi_col is not None and self.dphi_col is not None:
            dphish_val = self.dphish.value()
            nphish_val = self.nphish.value()
            self.vshwidget.set_porosity_args(self.dphi_col,dphish_val,self.nphi_col,nphish_val)
            self.vshwidget.update_plot()

        if self.gr_col is not None:
            self.vshwidget.gammaray_plot(self.gr_col)
            table = VshaletableModel(self.vshwidget.vshcal)
            self.zone_table_maker(table)
            self.vshwidget.canvas.draw()


    def zone_table_maker(self,table):
        if table is not None:
            self.vshgr_table  = table
            self.vshaleTableScrollarea.setWidget(self.vshgr_table)

    def gredit_button_checked(self):
        if hasattr(self, 'vshwidget'):
            if self.vshgreditButton.isChecked():
                print('Going to disable interaction')
                self.vshwidget.disable_interaction()
            else:
                self.vshwidget.enable_interaction()
                
    def vshalegr_done_button_clicked(self):
        if hasattr(self, 'vshgr_table') and self.vshgreditButton.isChecked():
            self.edited_agecorr = []
            self.edited_sand_shale_lines = []
            for combobox, sandbox, shaledbox,grdata in zip(self.vshgr_table.agecombobox_list, self.vshgr_table.sandspinbox_list,self.vshgr_table.shalespinbox_list,self.vshgr_table.zone_gr_list):
                self.edited_agecorr.append(combobox.currentText())
                sand_percentile = stats.percentileofscore(grdata,sandbox.value())
                shale_percentile = stats.percentileofscore(grdata,shaledbox.value())
                self.edited_sand_shale_lines.append([sand_percentile,shale_percentile])      
            self.vshwidget.vshcal.sand_shale_lines = self.edited_sand_shale_lines
            self.vshwidget.vshcal.age_correction = self.edited_agecorr
            self.vshwidget.update_plot()
            self.vshgreditButton.setChecked(False)
            

        
