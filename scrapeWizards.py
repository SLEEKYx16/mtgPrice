#!/usr/bin/python
#HTML parser
#Replaces beautiful soup because beautiful soup wasn't as easy to use for what I wanted
from lxml import html
from lxml.html.clean import clean_html
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests #to connect to the internet
import csv #to output the information
#Classes
#Class for decklist entries
class entry:
    def __init__(self,name,quantity,sideboard):
        self.name = name
        self.quantity = quantity
        #This is a flag so should be TRUE/False
        if isinstance(sideboard, bool):
            self.sideboard = sideboard
        else:
            raise ValueError('Sideboard was ' + str(type(sideboard)) + ' rather than boolean')
    def __str__(self):
        if self.sideboard:
            return 'SB: ' + str(self.quantity) + ' ' + self.name
        else:
            return str(self.quantity) + ' ' + self.name
#Class for decklists
class decklist:
    def __init__(self,player,date,kind):
        self.player = player
        self.date = date
        self.format = kind
        self.entries = []
        self.mainTotal = 0
        self.sideTotal = 0
    def append(self,newentry):
        #Should take an entry object
        self.entries.append(newentry)
        if newentry.sideboard:
            self.sideTotal += newentry.quantity
        else:
            self.mainTotal += newentry.quantity
    def __str__(self):
        #TODO: print sideboard cards all together
        #Print out all the entries nicely
        output = self.player + '\t' + self.date + '\n'
        output = output + str(len(self.uniqueCards())) + ' unique cards\n'
        output = output + str(self.mainTotal) + ':' + str(self.sideTotal) + '\n'
        output = output + '\n'.join([str(x) for x in self.entries])
        return output
    def uniqueCards(self):
        #return a set of unique cardnames
        unique = set()
        for eaEntry in self.entries:
            unique.add(eaEntry.name)
        return unique
#This date is which day will be looked up
lookupDate = '2018-02-22'
#Where to look for the URL
url = 'magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-'+ lookupDate
#Get the webpage text
r  = requests.get("http://" +url)
#XML/HTML tree structure which can be used with XPATH
tree = html.fromstring(r.content)
#List of decklists
decklists = []
#Select all divs containing decklists
decklistdivs = tree.xpath('//div[@class="deck-group"]')
for eaDecklistdiv in decklistdivs:
    thisPlayer = eaDecklistdiv.xpath('.//h4/text()')[0].replace(' (5-0)','')
    #make the decklist
    thisDeck = decklist(str(thisPlayer),lookupDate,'standard')
    for eaMainboard in eaDecklistdiv.xpath('descendant::div[@class="sorted-by-overview-container sortedContainer"]/descendant::span[@class="row"]'):
        (quantity, name) = (eaMainboard.xpath('child::span'))
        #Append the entry for the card to the decklist
        thisDeck.append(entry(name.text_content(),int(quantity.text_content()),False))
    for eaSideboard in eaDecklistdiv.xpath('descendant::div[@class="sorted-by-sideboard-container  clearfix element"]/descendant::span[@class="row"]'):
        (quantity, name) = (eaSideboard.xpath('child::span'))
        #Append the entry for the card to the decklist
        thisDeck.append(entry(name.text_content(),int(quantity.text_content()),True))
    #Add the deck to the list
    decklists.append(thisDeck)
#Test printing the decklists
for eaDeck in decklists:
    print(str(eaDeck))
#Exit after testing that the objects contain what they are supposed to
exit()

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
