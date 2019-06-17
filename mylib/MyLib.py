import os, sys
import re
from tinytag import TinyTag, TinyTagException
import requests
from requests.exceptions import MissingSchema, ConnectionError
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import numpy as np




def GetUncoverDir(DirRoot):
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

    for path, dirnames, filenames in os.walk(musicfoldername):

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

def getHTML(url):
    '''Input URL, Return requests.response'''
    headers = {'user-agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r    
    
def getGoogleImgHTML(keyword):
    '''Input KEYWORD, Return GooglePics Serach requests.response'''
    payload = {'q': keyword, 'tbm': 'isch'}
    #tbs=isz:lt,islt:vga >>> bigger than 640x480
    headers = {'user-agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = requests.get('https://www.google.com/search', params=payload, headers=headers)
    return r

def keywordParser(keyword):
    '''Parse Searching KEYWORD, return KEYWORD'''
    keyword = re.sub('(?:DISC|DISK|Disk|Disc|disk|disc).', '', keyword)
    keyword = re.sub(r'(?:[|])', ' ', keyword)
    keyword = re.sub(' ( )*', ' ', keyword)
    return keyword

def imgUrlParser(bs):
    '''Input BeautifulSoup of GooglePics Search Result, Return ImageURL|None'''
    try:
        img_scrab = bs.find('div', {'class':'rg_meta notranslate'})
        img_url = eval(img_scrab.text)['ou']
        return img_url
    except:
        # Can't get the Image URL
        return None

def imgUrlOpen(img_url):
    '''Input Image URL, Retrun PIL.Image|None'''
    try:
        with getHTML(img_url) as r:
            img = Image.open( BytesIO(r.content) )
            img = img.convert('RGB')
            print('Get Image successfully!\n')
            return img            
    except ConnectionError:
        print('HTTP Error 404: Not Found!\n')
        return None
    except MissingSchema:
        print('HTTP Address Failed!\n')
        return None
    except OSError:
        print('Cannot Identify Image File!\n')
        return None
