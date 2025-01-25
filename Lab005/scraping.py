import requests
from bs4 import BeautifulSoup
import json
import argparse

parser = argparse.ArgumentParser(description = 'Scraping Metallica albums')
parser.add_argument('album_name', type = str, help = 'Name of the album to scrape')
parser.add_argument('filename', type = str, help = 'Name of the file to save the results')
args = parser.parse_args()

album_name = args.album_name.replace(' ', '_') + '_(album)'
filename = args.filename

url = f'https://metallica.fandom.com/wiki/{album_name}'
res = requests.get(url)

if res.status_code != 200:
    print('That album does not exist!')
    exit()

soup = BeautifulSoup(res.text, 'html.parser')
table = soup.find('table', class_ = 'tracklist')
tr_all = table.find_all('tr')

songs_in_album = {}

for tr in tr_all:
    td_all = tr.find_all('td')
    if len(td_all) < 4:
        continue
    _ = td_all[0].text.strip()
    song_name = td_all[1].text.strip()
    composers = td_all[2].text.strip()
    length = td_all[3].text.strip()
    songs_in_album[song_name] = {
        'composers': composers,
        'length': length
    }

with open(f'Lab005/{filename}.json', 'w') as file:
    json.dump(songs_in_album, file, indent=4)