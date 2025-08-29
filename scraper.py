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
order = 1


blocklist_titles = ["utstilling", "debatt", "politikk", "politisk"]  # legg til det du vil
exclude_ticket_statuses = ["Utsolgt"]  # legg til flere statuser hvis ønskelig


for row in event_list:
    event = {}
    event['title'] = row.h3.text.strip()
    event['url'] = row['href']
    event['price'] = "NOK 100"
    event['order'] = order
    event['id'] = event['url'].split('/')[4]

    img_long = re.findall(r'\((.*?)\)', row.div['style'])
    event['img'] = str(img_long).split("'")[1]

    event['date'] = row.span.text.strip()
    tickets_long = row.find('span', class_='tickets')
    event['ticketStatus'] = tickets_long.text.strip()

    # Sjekk om tittel inneholder et blokkeringsord (case-insensitivt)
    if any(word.lower() in event['title'].lower() for word in blocklist_titles):
        continue

    # Sjekk om ticketstatus skal ekskluderes
    if event['ticketStatus'] in exclude_ticket_statuses:
        continue

    # Unngå duplikater
    if event['title'] not in added:
        events.append(event)
        added.append(event['title'])
        order += 1
    


filename = 'meta.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['id', 'price', 'order', 'title', 'url', 'img', 'date', 'ticketStatus' ])
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
