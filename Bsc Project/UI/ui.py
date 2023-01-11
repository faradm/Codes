'''
Entry point of program. create MainWindow and run program. 
'''

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)
from PySide2.QtCharts import QtCharts

import sys
from Widget import Widget
from MainWindow import MainWindow
import pydicom

class cancer_diag_app():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.central_widget = Widget()
        self.img = None
        self.window = MainWindow(self.central_widget)
        # self.window.showMaximized()
        # self.window.show()

if __name__ == "__main__":
    cancer_app = cancer_diag_app()
    # Execute application
    cancer_app.window.showMaximized()
    sys.exit(cancer_app.app.exec_())
