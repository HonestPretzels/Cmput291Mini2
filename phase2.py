import os
import re
from bsddb3 import db

def main():

    # Sort files
    os.system("sort -u -o sortedPrices.txt prices.txt")
    os.system("sort -n -o sortedPrices.txt sortedPrices.txt")
    os.system("sort -u -o sortedAds.txt ads.txt")
    os.system("sort -u -o sortedPdates.txt pdates.txt")
    os.system("sort -u -o sortedTerms.txt terms.txt")

    # Create database
    adDB = db.DB()
    adDB.open("ad.idx")
    adDB.set_flags(db.DB_DUP)
    teDB = db.DB()
    teDB.open("te.idx")
    teDB.set_flags(db.DB_DUP)
    prDB = db.DB()
    prDB.open("pr.idx")
    prDB.set_flags(db.DB_DUP)
    daDB = db.DB()
    daDB.open("da.idx")
    daDB.set_flags(db.DB_DUP)

    # Scrub the Ad file
    inputAdFile = open("sortedAds.txt",'r')
    outputAdFile = open("readyAds.txt",'w')

    for line in inputAdFile:
        items = line.split(":<ad>")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            outputString = items[0] + "\n" + "<ad>" + cleaned 
            outputAdFile.write(outputString)

    inputAdFile.close()
    outputAdFile.close()

    # Scrub the prices file
    inputAdFile = open("sortedPrices.txt",'r')
    outputAdFile = open("readyPrices.txt",'w')

    for line in inputAdFile:
        items = line.split(":")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            outputString = items[0] + "\n" + cleaned
            outputAdFile.write(outputString)

    inputAdFile.close()
    outputAdFile.close()

    # Scrub the pdates file
    inputAdFile = open("sortedPdates.txt",'r')
    outputAdFile = open("readyPdates.txt",'w')

    for line in inputAdFile:
        items = line.split(":")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            outputString = items[0] + "\n" + cleaned
            outputAdFile.write(outputString)

    inputAdFile.close()
    outputAdFile.close()

    # Scrub the terms file
    inputAdFile = open("sortedTerms.txt",'r')
    outputAdFile = open("readyTerms.txt",'w')

    for line in inputAdFile:
        items = line.split(":")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            outputString = items[0] + "\n" + cleaned
            outputAdFile.write(outputString)

    inputAdFile.close()
    outputAdFile.close()

    # Create indexes
    os.system("db_load -f readyAds.txt -t hash -T ad.idx")
    os.system("db_load -f readyPdates.txt -t btree -T da.idx")
    os.system("db_load -f readyTerms.txt -t btree -T te.idx")
    os.system("db_load -f readyPrices.txt -t btree -T pr.idx")

main()
