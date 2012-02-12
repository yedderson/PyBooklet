#!/usr/bin/env python
from PySide import QtGui
import sys
from PyBooklet import main

if __name__ == "__main__":
    Application = QtGui.QApplication(sys.argv)
    Application.setApplicationName("PyBooklet")
    Application.setStyle('cleanlooks')

    MainWindow =  main.MainWindow()
    MainWindow.show()
    sys.exit(Application.exec_())