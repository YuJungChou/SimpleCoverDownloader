import os
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit, 
                            QPushButton, QFileDialog, QCheckBox,
                            QSizePolicy, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt
from mygui import MyProgressbar

class GridRow01(QGridLayout):
    def __init__(self, parent):
        super().__init__()
        self.PARENT_QWIDGET = parent

        # Elements
        self.label_inputpath = QLabel('Please input the music directory path :')
        self.lineedit_dirpath = QLineEdit()
        self.button_browser = QPushButton('Browser')
        self.checkbox_saveimagefile = QCheckBox('Save Image File')
        self.label_waitingtime = QLabel('Waiting Time (Seconds): ')
        self.spinbox_waitingtime = QSpinBox()
        self.button_start = QPushButton('START')
        self.space0000 = QLabel('')
        # Properties
        self.button_browser.clicked.connect(self.Push_button_browser)
        self.button_start.clicked.connect(self.Push_button_start)
        self.button_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.checkbox_saveimagefile.setChecked(False)
        self.spinbox_waitingtime.setRange(0, 100)
        self.spinbox_waitingtime.setValue(20)
        self.spinbox_waitingtime.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Deployment
        self.addWidget(self.label_inputpath, 0,0)
        self.addWidget(self.lineedit_dirpath, 1,0,1,2)
        self.addWidget(self.button_browser, 1,2)
        self.addWidget(self.space0000, 2,1)
        self.addWidget(self.space0000, 3,0)
        self.addWidget(self.button_start, 4,2,2,1)
        self.addWidget(self.checkbox_saveimagefile, 3,2)
        self.addWidget(self.label_waitingtime, 4,0)
        self.addWidget(self.space0000, 4,1)
        self.addWidget(self.spinbox_waitingtime, 5,0)
        self.setColumnStretch(1, 1)
        self.setRowStretch(2, 1)

    def Push_button_browser(self):
        dirpath = QFileDialog.getExistingDirectory(self.PARENT_QWIDGET, 'Select the music directory')
        self.lineedit_dirpath.setText(dirpath)
        del dirpath

    def Push_button_start(self):
        dirname = self.lineedit_dirpath.text()
        if os.path.isdir(dirname):
            print('\nStart!')
            self.progressbar_widget = MyProgressbar.ProgressBarWidget(self)
            self.progressbar_widget.show()
        else:
            message = 'Incorrect directory:\n "' + dirname + '"'
            QMessageBox.about(self.PARENT_QWIDGET, "Incorrect Directory", message)

