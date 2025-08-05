import requests
from bs4 import BeautifulSoup
import re
import csv
import hashlib

def hash_sha256(input_str):
    hash_obj = hashlib.sha256(input_str.encode('utf-8'))
    return hash_obj.hexdigest()

URL = 'https://www.hamar-kulturhus.no/program/'
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

event_list = soup.findAll('a', attrs = {'class':'event-list-card'}) 
events = []
added = []

for row in event_list:
    event = {}
    event['title'] = row.h3.text
    # event['id-hash'] = hash_sha256(row.h3.text)
    event['url'] = row['href']
    event['price'] = "NOK 100"

    event['id'] = event['url'].split('/')[4]

    img_long = re.findall(r'\((.*?)\)', row.div['style'])
    event['img'] = str(img_long).split("'")[1]
    
    event['date'] = row.span.text
    tickets_long = row.find('span', class_='tickets')
    event['ticketStatus'] =  tickets_long.text

    if event['title'] in added:
        print(event['title'])

    
    if "Utstilling" not in event['title'] and event['title'] not in added:
        events.append(event)
        added.append(event['title'])
    


filename = 'meta.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['id', 'price', 'title', 'url', 'img', 'date', 'ticketStatus' ])
    w.writeheader()
    for event in events:
        w.writerow(event)

filename = 'google.csv'
google_headers = ['ID', 'Price', 'Item title', 'Final URL', 'Image URL', 'Item subtitle', 'Availability']
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, google_headers)
    w.writeheader()
    for event in events:
        row = {
            'ID': event['id'],
            'Price': event['price'],
            'Item title': event['title'],
            'Final URL': event['url'],
            'Image URL': event['img'],
            'Item subtitle': event['date'],
            'Availability': event['ticketStatus']
        }
        w.writerow(row)
