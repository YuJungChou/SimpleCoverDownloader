from PyQt5.QtWidgets import (QWidget, QTextEdit, QGridLayout)
from PyQt5.QtGui import QIcon

class ResultReport(QWidget):
    def __init__(self, result_report):
        super().__init__()
        self.RESULT_REPORT = result_report
        self.PARAMS()
        self.GEOMETRY()
        self.THREAD()
        self.ELEMENTS()
        self.ELEMENTS_PROPERTIES()
        self.ELEMENTS_DEPLOYMENT()
        self.LAYOUT_SETTING()
        self.START()

    def PARAMS(self):
        pass
    
    def GEOMETRY(self):
        self.setWindowTitle('Report')
        self.setWindowIcon(QIcon(':/icon.ico'))
    
    def THREAD(self):
        pass
    
    def ELEMENTS(self):
        self.textedit_report = QTextEdit()
    
    def ELEMENTS_PROPERTIES(self):
        pass
    
    def ELEMENTS_DEPLOYMENT(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.textedit_report, 0, 0)

        self.setLayout(self.grid_layout)

    def LAYOUT_SETTING(self):
        pass
    
    def START(self):
        failure_counts = len(self.RESULT_REPORT["FAILURE"]["DIR"])

        report_text = "Result Report:\n\n"
        report_text = report_text + "*Failure Counts: {0}\n".format( str(failure_counts) )
        for i in range(failure_counts):
            report_text = report_text + str(i+1) + ".\n"
            report_text = report_text + "{0:20s}: ".format("Directory") + self.RESULT_REPORT["FAILURE"]["DIR"][i] + "\n"
            report_text = report_text + self.RESULT_REPORT["FAILURE"]["DETAIL"][i]
            report_text += "\n"

        self.textedit_report.setText(report_text)
        