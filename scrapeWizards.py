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
    def qtyMain(self,name):
        for eaEntry in self.entries:
            if not eaEntry.sideboard:
                if eaEntry.name == name:
                    return eaEntry.quantity
        #If it didn't match it wasn't played
        return 0
    def qtySide(self,name):
        for eaEntry in self.entries:
            if eaEntry.sideboard:
                if eaEntry.name == name:
                    return eaEntry.quantity
        #If it didn't match yet it wasn't played
        return 0
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
#for eaDeck in decklists:
#    print(str(eaDeck))
#Make a list of all cards played
playedCards = set()
for eaDecklist in decklists:
    playedCards.update(eaDecklist.uniqueCards())
#It's not useful to know that the basics see play, for what this is being used for right now.
for eaBasic in ['Plains','Island','Swamp','Mountain','Forest']:
    playedCards.remove(eaBasic)
playedCards = list(playedCards)
#Figure out how many cards were played main and side board
playedMainboard = []
playedSideboard = []
for eaCard in playedCards:
    eaQuantity = 0
    for eaDeck in decklists:
        eaQuantity += eaDeck.qtyMain(eaCard)
    playedMainboard.append(eaQuantity)
    eaQuantity = 0
    for eaDeck in decklists:
        eaQuantity += eaDeck.qtySide(eaCard)
    playedSideboard.append(eaQuantity)
#TODO:This data frame isn't even used again later. It litterally does nothing. I don't get it.
df = pd.DataFrame({'Name': playedCards, 'Main': playedMainboard, 'Side': playedSideboard})
#Print out a TSV of the collection.
with open('collection.tsv', 'w') as csvfile:
    #open the TSV
    collection = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #print out each card
    for name, main, side in zip(playedCards, playedMainboard, playedSideboard):
        #This needs to be passed a list!!!
        collection.writerow([name, main, side])
print('fin')
