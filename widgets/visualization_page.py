from PyQt5 import QtWidgets ,  QtGui , QtCore
import typing 
from typing import List, Tuple, Dict, Any , Callable
import pandas as pd
from UI import Ui_visualizerForm
from .mpl_widgets import MplWidgetMltrk

resistivity_mnemonics = ['RT','RT10','RT20','RT50','RT30','RT60','RT20','RT50','RT60']+['AT10','AT20','AT30','AT50','AT60','AT20','AT50','AT60']+['AF10','AF20','AF30','AF50','AF60','AF20','AF50','AF60']+['AO10','AO20','AO30','AO50','AO60','AO20','AO50','AO60'] + ['RESD','RESS','RESM']
class VisulizationPage(QtWidgets.QWidget,Ui_visualizerForm):
    def __init__(self, parent=None):
        super(VisulizationPage, self).__init__(parent)
        self.setupUi(self)
        self.scrollArea : QtWidgets.QScrollArea
        self.multitrackwidget = MplWidgetMltrk(self)
        self.scrollArea.setWidget(self.multitrackwidget)
            
    def set_dataframe_to_visualize(self,df : pd.DataFrame):
        self.df = df
        self.comboBox: QtWidgets.QComboBox
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox.addItems(df.columns)
        self.comboBox_2.addItems(df.columns)
        self.multitrackwidget.set_dataframe(df)
        
        res_col= [col for col in df.columns if col in resistivity_mnemonics]
        
        if res_col:
            self.comboBox_2.setItemsSelected(res_col)
        self.pushButton : QtWidgets.QPushButton
        self.pushButton.clicked.connect(self.plotting_button_clicked)
            
    def plotting_button_clicked(self):
        curve_for_plotting = self.comboBox.getSelectedItems()
        curve_for_semilog = self.comboBox_2.getSelectedItems()
        self.multitrackwidget.perform_plotting(curve_for_plotting , curve_for_semilog)
        
        
    
        
