from bs4 import BeautifulSoup
import requests
import json
import sys
import os


_tagText = "div"
_tagTextId = "content-list-component yr-content-list-text text"
_tagImg = 'img'
_tagImgId = 'image__src'

_RawJsonUseToCrawlData = 'crawlData/sample.json'
_rootDirSavedAllImages = 'data/huffpost/images'
_rootFolderSavedAllAnnotation = 'data/huffpost/annotations'
class HuffPost:
    __name = "huffpost"
    
    def __init__(self):
        self._urls = []

    def start_request(self, amounts, dirStored="./"):
        self.rootFolderStored = dirStored
        self._loadListUrls()
        for i in range(amounts):
            self._newsID = self._urls[i].split("/")[-1]
            self.parse(self._urls[i])
    
    def parse(self, url):
        reponse = requests.get(url)
        if reponse.status_code != 200 :
            print(f"can't connect to {url}!!!")

        self.soup = BeautifulSoup(reponse.text)
        content = self.getContentNews()
        arrImg = self.getArrImagesNews() 
        self.NewsDict = {f'{self._newsID}': {'content': content, 'listImages': arrImg}}

        self._startProcessDownloadImages()
        self._startSaveAnnotation()
    
    def _startProcessDownloadImages(self):
        if os.path.exists(f"{self.rootFolderStored}/{_rootDirSavedAllImages}") != True:
            os.makedirs(f"{self.rootFolderStored}/{_rootDirSavedAllImages}")
        
        images = self.soup.find_all(_tagImg,_tagImgId)
        imgID = 0
        arrImg = []
        for image in images:
            imgName = f"{self._newsID}_{imgID}"
            self._downloadEachImage(image['src'], imgName)
            arrImg.append(imgName)
            imgID += 1
        print(f"complete download image from: {self._newsID}")
    
    def _startSaveAnnotation(self):
        if os.path.exists(f"{self.rootFolderStored}/{_rootFolderSavedAllAnnotation}") != True:
            os.makedirs(f"{self.rootFolderStored}/{_rootFolderSavedAllAnnotation}")
        
        with open(f"{self.rootFolderStored}/{_rootFolderSavedAllAnnotation}/{self._newsID}.json",'w') as ouputJson:
            json.dump(self.NewsDict, ouputJson)


    def getArrImagesNews(self):
        images = self.soup.find_all(_tagImg,_tagImgId)
        imgID = 0
        arrImg = []
        for image in images:
            imgName = f"{self._newsID}_{imgID}"
            arrImg.append(imgName)
            imgID += 1
        return arrImg
    
    def _downloadEachImage(self, url, imgName):
        imgRespone = requests.get(url)
        if imgRespone.status_code != 200:
            print(f"Can't download image from {url}")
            return
        
        dirSavedImg = f"{self.rootFolderStored}/{_rootDirSavedAllImages}/{self._newsID}"

        if os.path.exists(dirSavedImg) != True:
            os.mkdir(dirSavedImg)

        with open(f'{dirSavedImg}/{imgName}.jpeg','wb') as writeImg:
            writeImg.write(imgRespone.content)
        
    
    def getContentNews(self):
        texts = self.soup.find_all(_tagText, _tagTextId)
        content = ""
        for text in texts:
            if len(content) == 1:
                content = content + text.get_text()
            content = content + '\n' + text.get_text()
        return content
    
    def _loadListUrls(self):
        f = open(f"{_RawJsonUseToCrawlData}",'r')
        listObj = json.load(f)
        for obj in listObj['listObj']:
            self._urls.append(obj['link'])
        f.close() 
