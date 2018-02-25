#!/usr/bin/python
#JSON parsing module
import json
#for sorting the cards
from operator import itemgetter, attrgetter, methodcaller
#Classes
#Class for a card
class mtgcard:
  def __init__(self, name, colourID, set):
    self.name = name
    self.cid = colourID
    self.set = set
  def __str__(self):
    return '\t'.join([self.name, self.cid, self.set]) + '\n'
#load the set list
JSON = open('allSets.json','r',encoding='utf-8')
cardsJSON = json.load(JSON)
#Load the list of all the cards played in Standard, produced by the Jupyter Notebook
#The list is scraped from WotC's weekly decklists
playedCardsF = open('collection.tsv','r',encoding="utf-8")
playedCards = playedCardsF.readlines()
playedCards = [x.strip() for x in playedCards]
#Remove basic lands from the list of played cards because it is not interesting to know about them.
basics = ['Plains','Island','Swamp','Mountain','Forest']
for eaBasic in basics:
  try:
    playedCards.remove(eaBasic)
  except ValueError:
  #If a basic isn't played in Standard, we don't want to fail for that reason.
    print(eaBasic + ' was missing')
#Make a list of sets in Standard to loop through to save time.
standardSets = ['XLN','RIX','AKH','HOU','W17','KLD','AER']
#Loop through all the cards in standard, and if they are played then print their information
#This information will be placed in playedCards.tsv
#List into which to place cards
knownCards = []
for eaSet in standardSets:
  for card in cardsJSON[eaSet]['cards']:
    for playedCard in playedCards:
      if playedCard == card['name']:
        #If a card is colourless, there will be no entry in the JSON file.
        #This is solved here by adding "C" as the colour identity if we throw a keyerror
        try:
          colorID = ''.join(card['colorIdentity'])
        except KeyError:
          colorID = 'C'
        #append the card object to a list
        obj = mtgcard(playedCard, colorID, eaSet)
        knownCards.append(obj)
tsvout = open('playedCards.tsv','w',encoding="utf-8")
for knownCard in sorted(knownCards, key = attrgetter('set','name')):
  tsvout.write(str(knownCard))
tsvout.close()