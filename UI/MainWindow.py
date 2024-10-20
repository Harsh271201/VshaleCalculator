# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_appMainWindow(object):
    def setupUi(self, appMainWindow):
        appMainWindow.setObjectName("appMainWindow")
        appMainWindow.resize(1122, 753)
        self.centralwidget = QtWidgets.QWidget(appMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        appMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(appMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        appMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(appMainWindow)
        self.statusbar.setObjectName("statusbar")
        appMainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(appMainWindow)
        self.toolBar.setObjectName("toolBar")
        appMainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionDataLoader = QtWidgets.QAction(appMainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/fugue-icons-3.5.6/icons/database.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDataLoader.setIcon(icon)
        self.actionDataLoader.setObjectName("actionDataLoader")
        self.actionVisualization = QtWidgets.QAction(appMainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/fugue-icons-3.5.6/icons/spectrum-small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVisualization.setIcon(icon1)
        self.actionVisualization.setObjectName("actionVisualization")
        self.actionShaleCalcuation = QtWidgets.QAction(appMainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/fugue-icons-3.5.6/icons/calculator-scientific.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShaleCalcuation.setIcon(icon2)
        self.actionShaleCalcuation.setObjectName("actionShaleCalcuation")
        self.actionOpen_File = QtWidgets.QAction(appMainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionSave_File = QtWidgets.QAction(appMainWindow)
        self.actionSave_File.setObjectName("actionSave_File")
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionSave_File)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionDataLoader)
        self.toolBar.addAction(self.actionShaleCalcuation)
        self.toolBar.addAction(self.actionVisualization)

        self.retranslateUi(appMainWindow)
        QtCore.QMetaObject.connectSlotsByName(appMainWindow)

    def retranslateUi(self, appMainWindow):
        _translate = QtCore.QCoreApplication.translate
        appMainWindow.setWindowTitle(_translate("appMainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("appMainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("appMainWindow", "toolBar"))
        self.actionDataLoader.setText(_translate("appMainWindow", "DataLoader"))
        self.actionDataLoader.setToolTip(_translate("appMainWindow", "\'To Open DataLoading page\'"))
        self.actionVisualization.setText(_translate("appMainWindow", "Visualization"))
        self.actionVisualization.setToolTip(_translate("appMainWindow", "To Open the Visualization Page"))
        self.actionShaleCalcuation.setText(_translate("appMainWindow", "ShaleCalcuation"))
        self.actionShaleCalcuation.setToolTip(_translate("appMainWindow", "To Open the Shale Calculation page"))
        self.actionOpen_File.setText(_translate("appMainWindow", "Open File"))
        self.actionSave_File.setText(_translate("appMainWindow", "Save File "))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = QtWidgets.QMainWindow()
    ui = Ui_appMainWindow()
    ui.setupUi(appMainWindow)
    appMainWindow.show()
    sys.exit(app.exec_())
