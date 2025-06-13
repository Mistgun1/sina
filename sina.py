from tpb import TPB
from tpb import CATEGORIES, ORDERS
import subprocess, sys

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
    movie_title = ''
    index , text = FindFunction(text,TitleMarker,movie_number)
    while c!='"':
        movie_title+=c
        c = text[index+21+i]
        i += 1
    return movie_title

t = TPB('https://thepiratebay.org/')

command = 'curl -L      -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"  -H "Connection: keep-alive" "https://www.imdb.com/user/ur198572812/watchlist/?ref_=nv_usr_wl_all_0" --output mylist.txt'
subprocess.run(command,shell=True,executable="/bin/bash")

movie_titles = []

f = open("mylist.txt")
text = str(f.read())

TitlesNumber = NumberOfTitles(text)

for i in range(TitlesNumber):  
    movie_title = MovieTitle(text, i)
    movie_titles.append(movie_title)
    print(str(i)+'. '+movie_title)    
k = int(input("Type the number of the movie to download :"))
for torrent in t.search(movie_titles[k]):
    print(torrent.files)
f.close()
