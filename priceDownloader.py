import json

data = json.load(open('AllSets.json', encoding="utf8"))




for set in data:
    for card in data[set]["cards"]:
        cardname = card["name"]
        cardname = cardname.replace(" ", "+")
        cardname = cardname.replace("'", "2527s")

        urlName = "https://www.mtggoldfish.com/price-download/paper/"+cardname+"+%255B"+ set + "%255D"
        print(urlName)


#https://www.mtggoldfish.com/price-download/paper/tarmogoyf+%255BFUT%255D
