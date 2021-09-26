import pandas as pd
import requests
import os
import sys


_RawTSVFile = 'crawlData/2019JanData.tsv'
_Images = 'images'
_Annotation = 'annotations'
_root = "data/ksta"

_ColImageUrl = 'imageUrl'
_ColArticle = 'article'

def downloadEachImage(url, dirContainImg, articleID):
    imgResponse = requests.request('GET', url=url, headers={'User-Agent': 'Mozilla/5.0'})
    imageName = f"{articleID}.{url.split('/')[-1].split('.')[-1]}"

    if imgResponse.status_code != 200:
        print(f"connection error!! Can't download image {articleID} with statuscode: {imgResponse.status_code}")
        return

    if os.path.exists(dirContainImg) != True:
        os.mkdir(dirContainImg)
    
    with open(f"{dirContainImg}/{imageName}",'wb') as output:
        output.write(imgResponse.content)
    
    #os.system(f"wget -nd -r -P {dirContainImg} -A jpeg,jpg,bmp,gif,png {url}")

    print(f'complete downloaded: {imageName}')


def startDownloadAllImages(amounts, rootFolder="./"):
    if os.path.exists(f"{rootFolder}/{_root}") != True:
        os.makedirs(f"{rootFolder}/{_root}")

    _DirSavedAllImages = f"{rootFolder}/{_root}/{_Images}"
    _DirSavedALlAnnotation = f"{rootFolder}/{_root}/{_Annotation}"

    df = pd.read_csv(f"{_RawTSVFile}", sep='\t')

    for i in range(amounts):
        downloadEachImage(df[_ColImageUrl][i],_DirSavedAllImages, df[_ColArticle][i])
    print('Complete Download------')


