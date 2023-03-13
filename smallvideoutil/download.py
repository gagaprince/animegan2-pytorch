import requests
import json
import wget
import os
import hashlib


def loadVideoUrl(text):
    url = "https://vd.gagaprince.top/smallvideo/all"
    data = {
        'content': text
    }
    x = requests.post(url, json=data)
    print(x.text)
    jsonData = json.loads(x.text)
    print(jsonData)
    videoUrl = jsonData.get('data').get('videoUrl')
    print(videoUrl)
    return videoUrl


def md5(text):
    hl = hashlib.md5()
    hl.update(text.encode(encoding = 'utf-8'))
    return hl.hexdigest()


def main():
    inputFile = './readme.txt'
    savePath = '../smallvideo/videos/'

    for line in open(inputFile):
        print(line)
        videoUrl = loadVideoUrl(line)
        if videoUrl is not None:
            wget.download(videoUrl, os.path.join(savePath, md5(videoUrl) + '.mp4'))



if __name__ == '__main__':
    main()
