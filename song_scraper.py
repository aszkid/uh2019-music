import requests 
import re
import json
import pprint
from bs4 import BeautifulSoup

def scrape_from_ug(fname):
    song_stack = list() 
    burl = "https://www.ultimate-guitar.com/explore?page={}&type[]=Chords"

    for x in range(1,21): #21
        page = requests.get(burl.format(x))
        if(page.status_code != 200):
            print("Hit an error")
            continue
        html = re.findall(r"window\.UGAPP\.store\.page = (.*);",page.text)
        
        b = json.loads(html[0])
        for x in range(1,50):
            specific = b['data']['data']['tabs'][x] 
            song = dict()
            song['song_name'] = specific['song_name'] 
            song['tab_url'] = specific['tab_url']
            song['tonality_name'] = specific['tonality_name']
            song['artist_name'] = specific['artist_name']
            song['tab_access_type'] = specific['tab_access_type']
            song['chords'] = ''
            song_stack.append(song)
            print(specific['song_name'])
        #     print(specific['tonality_name'])
        #     print(specific['tab_access_type'])
        #     print(specific['artist_name'])
        #     print(specific['tab_url'])
        #     print("\n")

    for sg in song_stack:
        tab_wp = requests.get(sg['tab_url'])
        if(tab_wp.status_code != 200):
            print("Hit an error getting to a song page")
            break
        
        g = open("listofsongs","a")
        g.write(sg['song_name'])
        g.close()
        
        f = open("scraped/{}".format(sg['song_name']),'w')
        f.write(tab_wp.text)
        f.close()
        
        ppchords = re.findall(r"\[ch\](.*?)\[\\/ch\]",tab_wp.text)
        sg['chords'] = ppchords

    print(song_stack)

    q = open(fname,"w")
    q.write(json.dumps(song_stack))
    q.close()

#TODO - Make other scraping functions from different sites 

if __name__ == "__main__":
    print("scraping song module starting now")
    scrape_from_ug("songs.json")

    z = open("json_songs.json","r")
    output = json.loads(z.read())
    z.close()

    print(output[0])