import os, sys
import re
from tinytag import TinyTag, TinyTagException
import requests
from requests.exceptions import MissingSchema, ConnectionError
from bs4 import BeautifulSoup
from PIL import Image
import time

from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import Qt, QEvent, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from mylib import MyLib

class MainThread(QThread):

    label_states = pyqtSignal(str)
    label_detail = pyqtSignal(str)
    title_text = pyqtSignal(str)
    progressbar_setmax = pyqtSignal(int)
    progressbar_update = pyqtSignal(int)
    label_image = pyqtSignal(object)
    label_imgurl = pyqtSignal(str)
    result_report = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__()        
        self.PARENT = parent
        self.RESULT = {}
        self.TotalQuestCounts = 0
        self.SAVEIMAGE = False
        self.WAITING_TIME = 20

        self.StopFlag = False

    def stop(self):
        self.StopFlag = True

    def __del__(self):
        self.quit()
        self.wait()

    def params(self, save_img=False, waiting_time=20):
        self.SAVEIMAGE = save_img
        self.WAITING_TIME = waiting_time

    def run(self):
        self.RESULT = {
            "COVERED":{"DIR":[]},
            "UNCOVER":{"DIR":[], "KEYWORD":[]},
            "FAILURE":{"DIR":[], "DETAIL":[]}
            }
        self.RESULT = self.GetUncoverDir(self.PARENT.DIRNAME)
        self.TotalQuestCounts = len( self.RESULT["UNCOVER"]["DIR"] )
        self.progressbar_setmax.emit(self.TotalQuestCounts)
        self.WebScraping()
        if self.StopFlag == False:
            print('Thread Finished!')
            self.finished.emit()

    def GetUncoverDir(self, DirRoot):
        '''
        Walk the directory, return dictionary with (no cover.jpg) path and keyword: \n 
        dict GetUncoverDir(str dirpath) \n
        RESULT = {\n
            "COVERED":{"DIR":[]},
            "UNCOVER":{"DIR":[], "KEYWORD":[]},
            "FAILURE":{"DIR":[], "DETAIL":[]}
            }
        '''
        musicfoldername = DirRoot
        r = re.compile(r'(?:cover|COVER).(?:jpg|JPG|png|PNG)$')
        result = {"COVERED":{"DIR":[]}, 
                "UNCOVER":{"DIR":[], "KEYWORD":[]}, 
                "FAILURE":{"DIR":[], "DETAIL":[]}}

        self.label_states.emit("Searching the folder:")

        for path, dirnames, filenames in os.walk(musicfoldername):
            
            self.label_detail.emit(path)

            if filenames == []:
                # No files in this folder
                pass

            else:
                cover_file_list = list(filter(r.match, filenames)) # Try to find the cover.jpg in this folder

                if len(cover_file_list) != 0:
                    # cover.jpg exists
                    result["COVERED"]["DIR"].append(path)

                else:
                    # No cover.jpg 
                    for filename in filenames: # for<filename_loop>
                        # Try to get a music tag
                        try:
                            keyword = ""
                            tag = TinyTag.get( os.path.join(path, filename) )
                            tag_artist = tag.artist
                            tag_album = tag.album
                            if (tag_artist==None) & (tag_album==None):
                                keyword = filename
                            else:
                                if tag_artist == None:
                                    keyword = keyword + filename + " " + tag_album
                                elif tag_album == None:
                                    keyword = keyword + filename + " " + tag_artist
                                else:
                                    keyword = tag_album + " " + tag_artist
                            result["UNCOVER"]["DIR"].append(path)
                            result["UNCOVER"]["KEYWORD"].append(keyword)
                            break # END for<filename_loop>
                        except TinyTagException:
                            # Not support filetype
                            pass
                    else: # ELSE for<filename_loop>
                        result["FAILURE"]["DIR"].append(path)
                        result["FAILURE"]["DETAIL"].append('No Support files in The Folder')
            
        return result

    def WebScraping(self):

        for i in range(self.TotalQuestCounts):

            if self.StopFlag:
                print('Thread Stop!')
                break #Breaks main loop to finish 'run()'

            path = self.RESULT["UNCOVER"]["DIR"][i]
            keyword = self.RESULT["UNCOVER"]["KEYWORD"][i]
            print('Source Keyword: ' + keyword)
            
            self.label_states.emit("Processing... ({0}/{1})".format(str(i+1), str(self.TotalQuestCounts)))
            self.label_detail.emit("Searching Keyword  >>>  {0}".format(keyword))
            self.title_text.emit("({0}/{1}) {2}".format(str(i+1), str(self.TotalQuestCounts), keyword))
            self.progressbar_update.emit(i+1)

            r = MyLib.getGoogleImgHTML(keyword)
            r.connection.close()
            print('Source GoogleURL: ' + r.url)

            bs = BeautifulSoup(r.text, 'html.parser')
            img_url = MyLib.imgUrlParser(bs)
            
            if img_url != None:
                print('Source Image: ' + img_url)
                img = MyLib.imgUrlOpen(img_url)
                if img != None:
                    self.label_image.emit(img)
                    self.label_imgurl.emit(img_url)
                    if self.SAVEIMAGE:
                        img.save( os.path.join(path, 'cover.jpg'), 'JPEG')
                        print("Save Image Successfuly!")
                else:
                    print("Get Image Failure!")
                    self.RESULT["FAILURE"]["DIR"].append(path)
                    self.RESULT["FAILURE"]["DETAIL"].append("{0:20s}: {1}\nGet Image Failure: {2}".format("Keyword", keyword, img_url))    
            else:
                print("No Matching Image Search Results Found")
                self.RESULT["FAILURE"]["DIR"].append(path)
                self.RESULT["FAILURE"]["DETAIL"].append("{0:20s}: {1}\nNo Matching Image Search Results Found".format("Keyword", keyword))

            self.result_report.emit(self.RESULT)
            print()
            if (i+1) == self.TotalQuestCounts:
                print('Complete.')
            else:
                print('Wait ' + str(self.WAITING_TIME) + ' Seconds...')
                time.sleep(self.WAITING_TIME)








'''
        self.thread_set_max.emit(len(self.sc)) #To GUI

        self.DIR_STATES = MyLib.GetUncoverDir(self.DIRNAME)
        self.TotalQuestCounts = len( self.DIR_STATES["UNCOVER"]["DIR"] )

        super().__init__()  
        self._exportphotos_thread = ExportPhotosThread()
        self._exportphotos_thread.thread_set_max.connect(self.UIprogressbar1_set_max)
        self._exportphotos_thread.thread_update.connect(self.UIprogressbar2_set_value)
        self.initUI()

class ExportPhotosThread(QThread):
    thread_set_max = pyqtSignal(int)
    thread_update = pyqtSignal(int)
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()



    def UIprogressbar1_set_max(self, data):
        self.progress_bar.setMaximum(data)
    def UIprogressbar2_set_value(self, data):
        self.progress_bar.setValue(data)
        if data == self.progress_bar.maximum():
            self.progress_bar.setStyleSheet(COMPLETED_STYLE)
        elif data == 0:
            self.progress_bar.setStyleSheet(DEFAULT_STYLE)
    def UIprogressbar3_start(self):
        self._exportphotos_thread.params(self.sc, self.photos_path, self.export_path,
                                         self.checkbox_key_name, self.checkbox_key_snum, 
                                         self.checkbox_key_idnum, self.checkbox_export_name,
                                         self.checkbox_export_snum, self.checkbox_export_idnum,
                                         self.checkbox_export_cls, self.checkbox_export_num,
                                         self.checkbox_downgrade_image)
        self._exportphotos_thread.start()
'''