from bsddb3 import db
from datetime import datetime
import re

def get_id(it):
    it = it.decode("utf-8")
    items = it.split(',')
    return items[0]

# given a list of item_ids, retrieve the full info
def get_full_data(item_ids):
    database = db.DB()
    database.open('ad.idx')
    date = ''
    loc = ''
    cat = ''
    desc = ''
    price = ''
    data = []

    for entry in item_ids:
        cur = database.cursor()
        # it = cur.first()

        values = database.get(entry.encode("utf-8"))

        it = values.decode("utf-8")
        it = it.replace('><', '{SplitTarget}')
        it = it.replace('<', '{SplitTarget}')
        it = it.replace('>', '{SplitTarget}')
        it = it.replace('"\\"', '{SplitTarget}')
        it = it.split('{SplitTarget}')

        # print(it)

        title = ''
        i = 0
        for item in it:
            if (item == 'ti'):
                title = it[i+1]
            elif (item == 'date'):
                date = it[i+1]
            elif (item == 'loc'):
                loc = it[i+1]
            elif (item == 'cat'):
                cat = it[i+1]
            elif (item == 'desc'):
                desc = it[i+1]
            elif (item == 'price'):
                price = it[i+1]
            i += 1

        data.append([entry, date, loc, cat, title, desc, price])


        cur.close()
    
    database.close()

    return data


# query the database or iterate over the data given to complete a date query
def search_date(search, data):

    term = search[-10:]

    # if there has not been a query yet, query the database, otherwise, check the current data and query that
    if (data is None):
        database = db.DB()
        database.open("da.idx")

        cur = database.cursor()
        it = cur.first()

        item_ids = []
        item_id = ''


        while it:
            if ('<=' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%Y/%m/%d") <= datetime.strptime(term, "%Y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('>=' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%Y/%m/%d") >= datetime.strptime(term, "%Y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('>' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%Y/%m/%d") > datetime.strptime(term, "%Y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('<' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%Y/%m/%d") < datetime.strptime(term, "%Y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('=' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%Y/%m/%d") == datetime.strptime(term, "%Y/%m/%d")):
                    item_id = get_id(it[1])

            if (item_id != ''):
                item_ids.append(item_id)
                item_id = ''
            it = cur.next()

        cur.close()
        database.close()

        return get_full_data(item_ids)

    else:
        new_data = []

        for item in data:
            if ('<=' in search):
                if (datetime.strptime(item[1], "%Y/%m/%d") <= datetime.strptime(term, "%Y/%m/%d")):
                    new_data.append(item)
            elif ('>=' in search):
                if (datetime.strptime(item[1], "%Y/%m/%d") >= datetime.strptime(term, "%Y/%m/%d")):
                    new_data.append(item)
            elif ('>' in search):
                if (datetime.strptime(item[1], "%Y/%m/%d") > datetime.strptime(term, "%Y/%m/%d")):
                    new_data.append(item)
            elif ('<' in search):
                if (datetime.strptime(item[1], "%Y/%m/%d") < datetime.strptime(term, "%Y/%m/%d")):
                    new_data.append(item)
            elif ('=' in search):
                if (datetime.strptime(item[1], "%Y/%m/%d") == datetime.strptime(term, "%Y/%m/%d")):
                    new_data.append(item)

        return new_data

# query db or data for price query
def search_price(search, data):

    is_int = True
    i = len(search) - 1
    j = 0

    while is_int:
        try:
            int(search[i])
            j += 1
            i -= 1
        except ValueError:
            is_int = False
    if j > 0:
        term = search[-j:]

    # print(term)

    if (data is None):
        database = db.DB()
        database.open("pr.idx")

        cur = database.cursor()
        it = cur.first()

        item_ids = []
        item_id = ''


        while it:
            if ('<=' in search):
                if (int(it[0].decode("utf-8")) <= int(term)):
                    item_id = get_id(it[1])
            elif ('>=' in search):
                if (int(it[0].decode("utf-8")) >= int(term)):
                    item_id = get_id(it[1])
            elif ('<' in search):
                if (int(it[0].decode("utf-8")) < int(term)):
                    item_id = get_id(it[1])
            elif ('>' in search):
                if (int(it[0].decode("utf-8")) > int(term)):
                    item_id = get_id(it[1])
            elif ('=' in search):
                if (int(it[0].decode("utf-8")) == int(term)):
                    item_id = get_id(it[1])

            if (item_id != ''):
                item_ids.append(item_id)
                item_id = ''
            it = cur.next()

        cur.close()
        database.close()

        return get_full_data(item_ids)

    else:
        new_data = []

        for item in data:
            if ('<=' in search):
                if (int(item[6]) <= int(term)):
                    new_data.append(item)
            elif ('>=' in search):
                if (int(item[6]) >= int(term)):
                    new_data.append(item)
            elif ('<' in search):
                if (int(item[6]) < int(term)):
                    new_data.append(item)
            elif ('>' in search):
                if (int(item[6]) > int(term)):
                    new_data.append(item)
            elif ('=' in search):
                if (int(item[6]) == int(term)):
                    new_data.append(item)

        return new_data

# Search for terms in title
def search_term(search, data):

    item_ids = []
    item_id = ''

    if ('%' in search):
        term = search[0:len(search)-1]
    else:
        term = search

    if (data is None):
        database = db.DB()
        database.open("te.idx")
        cur = database.cursor()
        it = cur.set_range(term.encode("utf-8"))

        while it:
            if ('%' in search):
                if (term in it[0].decode("utf-8")):
                    item_id = get_id(it[1])
            elif (term == it[0].decode("utf-8")):
                    item_id = get_id(it[1])               
            else:
                break

            if (item_id != ''):

                if item_id not in item_ids:
                    item_ids.append(item_id)

                item_id = ''

            it = cur.next()

        cur.close()
        database.close()

        return get_full_data(item_ids)

    else:
        new_data = []

        for item in data:
            if ('%' in search):
                if (term in item[4].lower() or term in item[5].lower()):
                    new_data.append(item)

            else:
                title_terms = item[4].split()
                desc_terms = item[5].split()

                term_seen = False

                for word in title_terms:
                    if (word == term):
                        term_seen = True
                        break

                if not term_seen:
                    for word in desc_terms:
                        if (word == term):
                            term_seen = True
                            break

            if (item_id != ''):
                item_ids.append(item_id)
                item_id = ''

        return new_data

def search_cat(term, data):

    if (data is None):
        database = db.DB()
        database.open('ad.idx')
        date = ''
        loc = ''
        cat = ''
        desc = ''
        price = ''
        title = ''
        data = []

        cur = database.cursor()
        it = cur.first()

        #Match each item with one in the db and retrieve full info
        while it:
            entry = it[0].decode("utf-8")
            it = it[1].decode("utf-8")
            it = it.replace('><', '{SplitTarget}')
            it = it.replace('<', '{SplitTarget}')
            it = it.replace('>', '{SplitTarget}')
            it = it.replace('"\\"', '{SplitTarget}')
            it = it.split('{SplitTarget}')
            
            i = 0
            for item in it:
                if (item == 'ti'):
                    title = it[i+1]
                elif (item == 'date'):
                    date = it[i+1]
                elif (item == 'loc'):
                    loc = it[i+1]
                elif (item == 'cat'):
                    cat = it[i+1]
                elif (item == 'desc'):
                    desc = it[i+1]
                elif (item == 'price'):
                    price = it[i+1]
                i += 1

            if(cat.lower() == term):
                data.append([entry, date, loc, cat, title, desc, price])

            it = cur.next()
        cur.close()
        database.close()
        return data

    else:
        new_data = []

        for item in data:
            if (item[3].lower() == term):
                new_data.append(item)

        return new_data

def search_location(term, data):

    if (data is None):
        database = db.DB()
        database.open('ad.idx')
        date = ''
        loc = ''
        cat = ''
        desc = ''
        price = ''
        title = ''
        data = []

        cur = database.cursor()
        it = cur.first()

        #Match each item with one in the db and retrieve full info
        while it:
            entry = it[0].decode("utf-8")
            it = it[1].decode("utf-8")
            it = it.replace('><', '{SplitTarget}')
            it = it.replace('<', '{SplitTarget}')
            it = it.replace('>', '{SplitTarget}')
            it = it.replace('"\\"', '{SplitTarget}')
            it = it.split('{SplitTarget}')
            
            i = 0
            for item in it:
                if (item == 'ti'):
                    title = it[i+1]
                elif (item == 'date'):
                    date = it[i+1]
                elif (item == 'loc'):
                    loc = it[i+1]
                elif (item == 'cat'):
                    cat = it[i+1]
                elif (item == 'desc'):
                    desc = it[i+1]
                elif (item == 'price'):
                    price = it[i+1]
                i += 1

            if(loc.lower() == term):
                # print("match")
                data.append([entry, date, loc, cat, title, desc, price])

            it = cur.next()

        cur.close()
        database.close()

        return data

    else:
        new_data = []

        for item in data:
            if (item[2].lower() == term):
                new_data.append(item)

        return new_data