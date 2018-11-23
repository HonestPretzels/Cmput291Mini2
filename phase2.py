import os
import re
from bsddb3 import db

def main():

    #Create database files
    adDatabase = db.DB()
    adDatabase.open("ad.idx",None,db.DB_HASH,db.DB_CREATE)
    teDatabase = db.DB()
    teDatabase.open("te.idx",None,db.DB_BTREE,db.DB_CREATE)
    prDatabase = db.DB()
    prDatabase.open("pr.idx",None,db.DB_BTREE,db.DB_CREATE)
    daDatabase = db.DB()
    daDatabase.open("da.idx",None,db.DB_BTREE,db.DB_CREATE)

    # Sort files
    os.system("sort -u -o sortedPrices.txt prices.txt")
    os.system("sort -n -o sortedPrices.txt sortedPrices.txt")
    os.system("sort -u -o sortedAds.txt ads.txt")
    os.system("sort -u -o sortedPdates.txt pdates.txt")
    os.system("sort -u -o sortedTerms.txt terms.txt")

    # Scrub the Ad file
    inputFile = open("sortedAds.txt",'r')

    for line in inputFile:
        items = line.split(":<ad>")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            adDatabase.put(items[0].encode("utf-8"),cleaned)

    inputFile.close()
    adDatabase.close()

    # Scrub the prices file
    inputFile = open("sortedPrices.txt",'r')

    for line in inputFile:
        items = line.split(":")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            prDatabase.put(items[0].encode("utf-8"),items[1]) 

    inputFile.close()
    prDatabase.close()

    # Scrub the pdates file
    inputFile = open("sortedPdates.txt",'r')

    for line in inputFile:
        items = line.split(":")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            daDatabase.put(items[0].encode("utf-8"),items[1])

    inputFile.close()
    daDatabase.close()

    # Scrub the terms file
    inputFile = open("sortedTerms.txt",'r')

    for line in inputFile:
        items = line.split(":")
        if len(items) == 2:
            cleaned = re.sub(r"\\", r"\\\\", items[1])
            teDatabase.put(items[0].encode("utf-8"),items[1])

    inputFile.close()
    teDatabase.close()

main()