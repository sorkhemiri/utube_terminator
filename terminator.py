import requests
import re
from bs4 import BeautifulSoup
from pytube import YouTube
import os

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






if __name__ == "__main__":
    url = input("Enter Youtube Url:")
    print(get_play_list_id(url))