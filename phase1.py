from bsddb3 import db
import sys
import re

def main():

    # Open files
    try:
        xml_record = sys.argv[1]
        records_file = open(xml_record,'r')
    except:
        print('Error: Could not open records file')
        exit(1)

    terms_file = open('terms.txt', 'w+')
    pdates_file = open('pdates.txt','w+')
    prices_file = open('prices.txt', 'w+')
    ads_file = open('ads.txt','w+')

    for line in records_file:
        items = get_items(line)
        if items != None:
            # Ads file
            ads_file.write(items['aid'] +':' + line)

            # Pdates file
            pdates_file.write(items['date'] + ':' + items['aid'] + ',' + items['cat'] + ',' + items['loc'] + '\n')

            # Prices file
            if items['price'] != None:
                prices_file.write(items['price'] + ':' + items['aid'] + ',' + items['cat'] + ',' + items['loc'] + '\n')

            # Terms file
            title_terms = get_terms(items['ti'])
            for term in title_terms:
                terms_file.write(term + ':' + items['aid'] + '\n')

            desc_terms = get_terms(items['desc'])
            for term in desc_terms:
                terms_file.write(term + ':' + items['aid'] + '\n')
        

    # Close files
    records_file.close()
    terms_file.close()
    pdates_file.close()
    prices_file.close()
    ads_file.close()

def get_items(line):
    organized_items = {}
    items = re.split("[<>]",line)
    if 'aid' not in items:
        return None

    for i in range(len(items)):

        if items[i] == 'aid':
           organized_items['aid'] = items[i+1]
        if items[i] == 'date':
            organized_items['date'] = items[i+1]
        if items[i] == 'loc':
            organized_items['loc'] = items[i+1]
        if items[i] == 'cat':
            organized_items['cat'] = items[i+1]
        if items[i] == 'ti':
            organized_items['ti'] = items[i+1]
        if items[i] == 'desc':
            organized_items['desc'] = items[i+1]
        if items[i] == 'price':
            if re.match('[0-9]+',items[i+1]):
                organized_items['price'] = items[i+1]
            else:
                organized_items['price'] = None

    return organized_items

def get_terms(term_string):
    # returns lower case terms
    terms = []
    term_string = re.sub('&#[0-9]+;', '', term_string)
    term_string = re.sub('&quot;', '/', term_string)  
    term_string = re.sub('&apos;', '"', term_string)
    term_string = re.sub('&amp;', '&', term_string)
    term_string = re.sub('[^0-9a-zA-Z_-]+', ' ', term_string)    
    for term in term_string.split():
        if re.match('[0-9a-zA-Z_-]{3}', term):
            terms.append(term.lower())
    return terms


main()