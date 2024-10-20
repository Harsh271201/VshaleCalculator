from PyQt5 import QtWidgets ,  QtGui , QtCore
import typing 
from typing import List, Tuple, Dict, Any , Callable
from UI import Ui_appMainWindow 
from .data_view_page import DataViewPage
from .visualization_page import VisulizationPage
from .vshale_page import VshalePage
import lasio
class Mainwindow(QtWidgets.QMainWindow , Ui_appMainWindow):
    def __init__(self , parent = None):
        super(Mainwindow , self).__init__(parent)
        self.setupUi(self)
        self.las = None
        self.stack_widget = QtWidgets.QStackedWidget(self)
        self.dataViewPage = DataViewPage(self)   
        self.visulizationPage = VisulizationPage(self) 
        self.vshalePage = VshalePage(self)
        
        self.setCentralWidget(self.stack_widget)
        self.stack_widget.addWidget(self.dataViewPage)
        self.stack_widget.addWidget(self.vshalePage)
        self.stack_widget.addWidget(self.visulizationPage)
        self.actionDataLoader.triggered.connect(self.set_data_view_page)
        self.actionVisualization.triggered.connect(self.set_visualization_page)
        self.actionShaleCalcuation.triggered.connect(self.set_vshale_page)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionSave_File.triggered.connect(self.save_file)
        
    
    def set_data_view_page(self):
        self.stack_widget.setCurrentWidget(self.dataViewPage)
    def set_visualization_page(self):
        self.stack_widget.setCurrentWidget(self.visulizationPage)
    def set_vshale_page(self):
        self.stack_widget.setCurrentWidget(self.vshalePage)
        
    def open_file(self):
        file_paths = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '.', 'Data Files(*.las *.LAS)')
        if file_paths and file_paths[0]:
            try:
                self.las = lasio.read(file_paths[0])
                print("File read successfully.")  
                self.data = self.las.df().reset_index()
                self.dataViewPage.add_dataframe_in_table(self.data)
                self.visulizationPage.set_dataframe_to_visualize(self.data)
                self.vshalePage.set_data(self.data , self.data.columns[0])
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to open the file:\n{str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "No file selected.")
            
    def update_las_File(self):
        if hasattr(self,'vshalePage'):
            if hasattr(self.vshalePage , 'vshwidget'):
                new_data = self.vshalePage.vshwidget.vshcal.data
                if 'Vsh_GR' in new_data.columns:
                    self.las.append_curve(
                        mnemonic='Vsh_GR',
                        data=new_data['Vsh_GR'],
                        unit='',
                        descr='Vshale GR',
                    )
                if 'Vsh_phi' in new_data.columns:
                    self.las.append_curve(
                        mnemonic='Vsh_phi',
                        data=new_data['Vsh_phi'],
                        unit='',
                        descr='Vshale phi',
                        )
        else:
            return
        
                    
            
    def save_file(self):
        if self.las is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "No LAS file loaded to save.")
            return
        self.update_las_File()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog 
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
                                                             "Save LAS File", 
                                                             "", 
                                                             "LAS Files (*.las);;All Files (*)", 
                                                             options=options)
        if file_path:
            try:
                if not file_path.endswith(".las"):
                    file_path += ".las"
                self.las.write(file_path, version=2.0) 
                QtWidgets.QMessageBox.information(self, "Success", f"LAS file saved successfully at: {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save LAS file: {str(e)}")
        
        
