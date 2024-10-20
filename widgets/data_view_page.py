from PyQt5 import QtWidgets ,  QtGui , QtCore
import typing 
from typing import List, Tuple, Dict, Any , Callable
import pandas as pd
from UI import Ui_dataViewForm
from .DataTable import DataFrameTableModel
class DataViewPage(QtWidgets.QWidget,Ui_dataViewForm):
    def __init__(self, parent=None):
        super(DataViewPage, self).__init__(parent)
        self.setupUi(self)
        
    def add_dataframe_in_table(self,df : pd.DataFrame):
        self.tablemodel = DataFrameTableModel(df)
        self.tableView.setModel(self.tablemodel)
    