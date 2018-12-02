import requests
import re
from bs4 import BeautifulSoup
from pytube import YouTube
import os
import pickle

def connection_check():
    # internet connection check!
    try:
        res = requests.get("https://www.google.com/",timeout=5)
        try:
            res = requests.get("https://www.youtube.com/",timeout=5) 
            return True
        except:
            print("check your proxy")
            return False
    except:
        print("check your connection")
        return False

def initialize():
    if not os.path.exists("/home/mahdi/Downloads/utube"):
        os.mkdir("/home/mahdi/Downloads/utube")
    if not os.path.exists("/home/mahdi/.utube"):
        os.mkdir("/home/mahdi/.utube")

def get_play_list_id (Url):
    #extract playlist id from link
    if re.search(r'list=\S+', Url):
        urlCore = Url.split("/")[-1]
        urlList = urlCore.split("&")
        for item in urlList:
             if 'list=' in item:
                urlCore = item
        ind = urlCore.index("=") + 1
        urlCore = urlCore[ind:]
        return urlCore
    else:
        print("this Url doesn't contain list")
        return None

def final_video_urls (Urls):
    #generates valid video urls
    finals = []
    for url in Urls:
        ind = url.index("&")
        furl = 'http://www.youtube.com/'+url[:ind]
        finals.append(furl)
    finals = list(set(finals))
    return finals , len(finals)

def set_files_generator(playlist_id , videos):
    if not os.path.exists("/home/mahdi/.utube/"+playlist_id):
        os.mkdir("/home/mahdi/.utube/"+playlist_id)
    with open("/home/mahdi/.utube/{}/.utt".format(playlist_id),"wb") as file:
        pickle.dump(videos,file)


def get_video_urls (playlist_id):
    #extracts playlist links with given id
    rawhtml = requests.get("https://www.youtube.com/playlist?list={}".format(playlist_id)).text
    patern = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    matches = list(re.findall(patern , rawhtml))
    videos , num = final_video_urls(matches)
    set_files_generator(playlist_id,videos)
    return videos , num




if __name__ == "__main__":
    initialize()
    if connection_check():
        url = input("Enter Youtube Url:")
        pl = get_play_list_id(url)
        v , n = get_video_urls(pl)