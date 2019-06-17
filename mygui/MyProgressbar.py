from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, 
                            QPushButton, QSizePolicy, QProgressBar,
                            QDesktopWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon

from mylib import MyLib
from mygui import MyFunc, MyReport

from PIL import Image
from PIL.ImageQt import ImageQt
from io import BytesIO

class ProgressBarWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.PARENT = parent
        self.PARAMS()
        self.GEOMETRY()
        self.THREAD()
        self.ELEMENTS()
        self.ELEMENTS_PROPERTIES()
        self.ELEMENTS_DEPLOYMENT()
        self.LAYOUT_SETTING()
        self.START()

    def PARAMS(self):
        self.DIRNAME = self.PARENT.lineedit_dirpath.text()
        self.SAVEIMAGE = self.PARENT.checkbox_saveimagefile.isChecked()
        self.WAITING_TIME = self.PARENT.spinbox_waitingtime.value()
        self.ResultReport = {}

    def GEOMETRY(self):
        self.setWindowTitle('Progressing...')
        self.setWindowIcon(QIcon(':/icon.ico'))
        self.WIDGET_WIDTH, self.WIDGET_HEIGHT = 420, 500
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height()
 
    def THREAD(self):
        self.thread_mission = MyFunc.MainThread(self)
        self.thread_mission.label_states.connect(self.setStatesLabel)
        self.thread_mission.label_detail.connect(self.setDetailLabel)
        self.thread_mission.title_text.connect(self.setTitleText)
        self.thread_mission.progressbar_setmax.connect(self.setProgressbarMax)
        self.thread_mission.progressbar_update.connect(self.setProgressbarValue)
        self.thread_mission.label_image.connect(self.setLabelImage)
        self.thread_mission.label_imgurl.connect(self.setLabelImgUrl)
        self.thread_mission.result_report.connect(self.getResultReport)
        self.thread_mission.finished.connect(self.FINISHED)

    def ELEMENTS(self):
        self.label_space0000 = QLabel('')
        self.label_states = QLabel()
        self.label_detail = QLabel('Waiting to start...')
        self.progressbar_states = QProgressBar()
        self.button_abort = QPushButton('Cancel')
        self.label_imgpreview = QLabel('Image Preview')
        self.pixmap_image = QPixmap()
        self.label_imgurl = QLabel("https://")

    def ELEMENTS_PROPERTIES(self):
        self.label_states.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_detail.setFixedWidth(400)
        self.label_detail.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.progressbar_states.setAlignment(Qt.AlignCenter)
        self.button_abort.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_abort.clicked.connect(self.ABORT)
        self.label_imgpreview.setFrameShape(QFrame.StyledPanel)
        self.label_imgpreview.setFrameShadow(QFrame.Sunken)
        self.label_imgpreview.setAlignment(Qt.AlignCenter)
        self.label_imgurl.setAlignment(Qt.AlignCenter)
        self.label_imgurl.setFixedWidth(400)
        self.label_imgurl.setWordWrap(True)
        self.label_imgurl.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def ELEMENTS_DEPLOYMENT(self):
        self.gridrow01 = QGridLayout()
        self.gridrow01.addWidget(self.label_states, 0,0)
        self.gridrow01.addWidget(self.label_detail, 1,0)
        self.gridrow01.addWidget(self.progressbar_states, 2,0)
        self.gridrow01.addWidget(self.label_space0000, 3,0)
        self.gridrow01.addWidget(self.button_abort, 4,0, alignment=Qt.AlignCenter)
        self.gridrow01.addWidget(self.label_space0000, 5,0)

        self.grid_img = QGridLayout()
        self.grid_img.addWidget(self.label_imgpreview, 0,0)
        self.grid_img.addWidget(self.label_imgurl, 1,0)
        self.grid_img.setRowStretch(0, 1)

        self.grid_layout = QGridLayout()
        self.grid_layout.addLayout(self.gridrow01, 0, 0)
        self.grid_layout.addLayout(self.grid_img, 1, 0)
        self.grid_layout.setRowStretch(1, 1)

        self.setLayout(self.grid_layout)

    def LAYOUT_SETTING(self):
        self.setWindowModality(Qt.ApplicationModal) # Lock on windowsTop
        self.setGeometry( int((self.SCREEN_WIDTH-self.WIDGET_WIDTH)/2),
                          int((self.SCREEN_HEIGHT-self.WIDGET_HEIGHT)/2),
                          self.WIDGET_WIDTH, self.WIDGET_HEIGHT )

    def START(self):
        self.thread_mission.params(save_img=self.SAVEIMAGE, waiting_time=self.WAITING_TIME)
        self.thread_mission.start()

    def ABORT(self):       
        self.close()

    def FINISHED(self):
        self.close()

    def closeEvent(self, event):
        if self.thread_mission.isFinished() == False:
            self.thread_mission.stop()     
        self.result_report = MyReport.ResultReport(self.ResultReport)
        self.result_report.show()

    def setStatesLabel(self, string):
        self.label_states.setText(string)
    def setDetailLabel(self, string):
        self.label_detail.setText(string)
    def setTitleText(self, string):
        self.setWindowTitle(string)
    def setProgressbarMax(self, value):
        self.progressbar_states.setMaximum(value)
    def setProgressbarValue(self, value):
        self.progressbar_states.setValue(value)
    def setLabelImage(self, img):
        img_limit = 400
        imageqt = ImageQt(img) #convert PIL image to a PIL.ImageQt object
        qimage = QImage(imageqt) #cast PIL.ImageQt object to QImage object
        #self.LAYOUT_SETTING()
        self.pixmap_image = QPixmap(qimage).scaled(img_limit, img_limit, aspectRatioMode=Qt.KeepAspectRatio)
        self.label_imgpreview.setPixmap(self.pixmap_image)
    def setLabelImgUrl(self, string):
        self.label_imgurl.setText(string)
    def getResultReport(self, dict01):
        self.ResultReport = dict01
