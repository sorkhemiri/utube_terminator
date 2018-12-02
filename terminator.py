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


def title_for_url (Url):
    res = requests.get(Url).text
    soup = BeautifulSoup(res , "lxml")
    title = soup.find('span',class_="watch-title").text\
    .replace("\n",'').strip()
    return title

def list_Terminator(Url , Sub):

    pi = get_play_list_id(Url)
    videos , number = get_video_urls(pi)


    print("there are {} videos in this playlist".format(number))
    for i in range(len(videos)):
        print(str(i+1)+"-"+title_for_url(videos[i]))
    select = input("Enter Number of videos you want with '-' between:")


    if not os.path.exists("/home/mahdi/Downloads/utube"):
        os.mkdir("/home/mahdi/Downloads/utube")
    if not os.path.exists("/home/mahdi/Downloads/utube/"+pi):
        os.mkdir("/home/mahdi/Downloads/utube/"+pi)


    if (not Sub) and (select == '0'):
        #just download all list without sub
        print("we are here")

    elif (not Sub) and (select != '0'):
        #downloading choosen items without sub
        pass

    elif (Sub) and (select == '0'):
        #download all list with sub
        pass

    elif (Sub) and (select != '0'):
        #downloading choosen items with sub
        pass
        
    else:
        print("the value of sub parameter or the numbers of videos is invalid")

def Terminator ():
    initialize()
    if connection_check():
        url = input("Enter Youtube Url:")
        options = input("for downloading a list Enter (L/l) and for Single viedo Enter (S/s):")
        sub = input("do you want subtitle(y/Y) for yes and (n/N) for no:")
        
        if options.lower() == 'l' and sub.lower() == 'n':
            list_Terminator(url,False)
        elif options.lower() == 'l' and sub.lower() == 'y':
            pass
        elif options.lower() == 's' and sub.lower() == 'n':
            pass
        elif options.lower() == 's' and sub.lower() == 'y':
            pass
        else:
            print("is it a list or a single video?")

if __name__ == "__main__":
    Terminator()