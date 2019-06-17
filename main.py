import os, sys
import re
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, 
                             QPushButton, QFileDialog, QMessageBox,
                             QGridLayout, QVBoxLayout, QHBoxLayout, 
                             QApplication, QCheckBox, QSizePolicy,
                             QProgressBar, QGroupBox, QTabWidget,
                             QMenu, QAction, QTreeView, QInputDialog,
                             QAbstractItemView)
from PyQt5.QtGui import QFont, QStandardItemModel, QPixmap, QIcon
from PyQt5.QtCore import Qt, QVariant, QEvent, QThread, pyqtSignal

from mylib import MyLib
from mygui import MyGUI
import iconQrc


class MainWindow(QMainWindow):   
    def __init__(self):
        super(MainWindow, self).__init__()        
        self.win_widget = WinWidget(self)
        self.win_widget.setWindowTitle('AlbumArtDownloader')
        self.win_widget.setWindowIcon(QIcon(':/icon.ico'))
        self.win_widget.setMinimumWidth(400)
        self.win_widget.show()

class WinWidget(QWidget):
    def __init__(self, parent):
        super().__init__()  
        self.PARENT_QMAINWINDOW = parent
        self.initUI()
    def initUI(self):
        self.gridrow01 = MyGUI.GridRow01(self)

        self.grid_layout = QGridLayout()
        self.grid_layout.addLayout(self.gridrow01, 0, 0)

        self.setLayout(self.grid_layout)






if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    _, _, SCREEN_WIDTH, SCREEN_HEIGHT = app.desktop().screenGeometry().getRect()
    gui = MainWindow()
    sys.exit(app.exec_())
