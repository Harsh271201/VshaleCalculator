import sys
from PyQt5 import QtWidgets
from widgets.AppMainWindow import Mainwindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    try:
        window = Mainwindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        sys.exit(1)

if __name__ == '__main__':
    main()

