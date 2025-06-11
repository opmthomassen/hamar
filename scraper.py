import requests
from bs4 import BeautifulSoup
import re
import csv

URL = 'https://www.hamar-kulturhus.no/program/'
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

event_list = soup.findAll('a', attrs = {'class':'event-list-card'}) 
events = []

for row in event_list:
    event = {}
    event['title'] = row.h3.text
    event['url'] = row['href']

    event['id'] = event['url'].split('/')[4]

    img_long = re.findall(r'\((.*?)\)', row.div['style'])
    event['img'] = str(img_long).split("'")[1]
    
    event['date'] = row.span.text
    tickets_long = row.find('span', class_='tickets')
    event['ticketStatus'] =  tickets_long.text

    events.append(event)

print(events)

filename = 'hamar.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['id', 'title','url','img', 'date', 'ticketStatus' ])
    w.writeheader()
    for event in events:
        w.writerow(event)
