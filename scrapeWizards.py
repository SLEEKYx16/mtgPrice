#!/usr/bin/python
from bs4 import BeautifulSoup
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests #to connect to the internet
import csv #to output the information
#This date is which day will be looked up
lookupDate = '2018-02-22'
#Where to look for the URL
url = 'magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-'+ lookupDate
#Get the text with BeautifulSoup
r  = requests.get("http://" +url)
data = r.text
soup = BeautifulSoup(data)
#Make a list of all cards
playedCards = []
#Look for all the hyperlinks to gatherer which correspond to cards in the decks
# for span in soup.findAll('span', {'class':'row'}):
	# for child in span.children:
		# print(child)
		# if child['class'] == 'card-count':
			# number = child.string
		# elif child['class'] == 'deck-list-link':
			# name = child.string
		# print('\t'.join([number, name]))
for card in soup.findAll('a', {'class':'deck-list-link'}):
    if card.string not in playedCards:
        playedCards.append(card.string)  
df = pd.DataFrame({'Name': playedCards})
with open('collection.tsv', 'w') as csvfile:
    collection = csv.writer(csvfile, delimiter='\n', quotechar='\t', quoting=csv.QUOTE_MINIMAL)
    collection.writerow(playedCards)
print('fin')