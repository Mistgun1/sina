import subprocess, sys
from pb_scraper import TorrentFinder
from torrentp import TorrentDownloader
import asyncio
import configparser

def CreateFile(imdb_watchlist_link):    
    command = 'curl -L      -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"  -H "Connection: keep-alive" "'+imdb_watchlist_link+'" --output mylist.txt'
    subprocess.run(command,shell=True,executable="/bin/bash")

def DeleteFile(): 
    command = 'rm -r mylist.txt'
    subprocess.run(command,shell=True,executable="/bin/bash")


def NumberOfTitles(text):
    TitlesNumberMarker = "titles</li></ul><div"
    n=''
    j=0
    ch=''
    while n!='>':
        ch = n + ch
        n = text[text.find(TitlesNumberMarker)-1-j]
        j += 1
    return int(ch)

def FindFunction(text,marker,occurrence):
    if occurrence != 0 : 
        text = text[text.find(marker)+1:]
        return FindFunction(text,marker,occurrence-1)
    else :
        return text.find(marker), text


def MovieTitle(text,movie_number):
    TitleMarker = '"titleText":{"text":"'
    c = ''
    i = 0
    title = ''
    index , text = FindFunction(text,TitleMarker,movie_number)
    while c!='"':
        title+=c
        c = text[index+21+i]
        i += 1
    if (text[index+67+i]=='m'):
        title_type = "movie  "
    else:
        title_type = "tv show"
    return title, title_type

#def ScrapDataFromImdb():



if __name__=='__main__' :
    
    
    config = configparser.ConfigParser()
    config.read('sina.conf')
    imdb_watchlist_link = config.get('settings','imdb_watchlist_link')
    download_location = config.get('settings','download_location')

    CreateFile(imdb_watchlist_link)
    
    titles=[]
    with open("mylist.txt") as f:
        text = str(f.read()) 
        TitlesNumber = NumberOfTitles(text)
        for i in range(TitlesNumber):  
            title ,title_type= MovieTitle(text, i)
            titles.append((title ,title_type))
            print(str(i)+'. '+title_type+' : '+title)    

    DeleteFile()

    k = int(input("Type the number of the movie to download :"))        
    scrape = TorrentFinder()
    if titles[k][1][0]=='m':
        data = scrape.search_hd_movies(titles[k][0])
        if len(data)>5 :
            for i in range(5):
                print('Title: ' + data[i]['title'])
                print('Size: ' + data[i]['size'])
                print('Seeders: ' + data[i]['seeders'])
                print('Leechers: ' + data[i]['leechers'])
                print('_______________________________________________________________')
        else:    
            for result in data:
                print('title: ' + result['title'])
                print('size: ' + result['size'])
                print('seeders: ' + result['seeders'])
                print('leechers: ' + result['leechers'])
                print('_______________________________________________________________')
            
    else :
        data = scrape.search_hd_tv_shows(titles[k][0])    
        for result in data:
            print('title: ' + result['title'])
            print('size: ' + result['size'])
            print('seeders: ' + result['seeders'])
            print('leechers: ' + result['leechers'])
            print('_______________________________________________________________')
        
    torrent_choice = int(input("which file you want to download :"))
    torrent_file = TorrentDownloader(data[torrent_choice]['magnet'],download_location)
    asyncio.run(torrent_file.start_download())
