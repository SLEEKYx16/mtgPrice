#!/usr/bin/python
#JSON parsing module
import json
#for sorting the cards
#for reading the now more complicated TSV
#for interacting with the Database
import pyodbc
#For dealing with unicode from the json
import codecs
# For dealing with unicode from the json
import codecs
import json
# for sorting the cards
# for reading the now more complicated TSV
# for interacting with the Database
import pyodbc


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
cardsJSON = json.load(codecs.open('./AllCards.json', 'r', 'utf-8-sig'))
#open connection to database
mtgdb = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-62G1QJF;"
                      "Database=MTG;"
                      "Trusted_Connection=yes;")
#Loop through all the cards and add them to the database
for card in cardsJSON:
    print(card)
