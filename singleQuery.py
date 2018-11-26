from bsddb3 import db
from datetime import datetime
import re


def query(search, data):

    term = ''
    open_db = ''
    item_id = ''


    if ('date' in search):

        return search_date(search, data)

    elif ('price' in search):

        return search_price(search, data)

    else:

        return search_term(search, data)



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
        it = cur.first()

        #Match each item with one in the db and retrieve full info
        while it:
            if (entry in it[1].decode("utf-8")):
                it = it[1].decode("utf-8")
                it = it.replace('><', ';')
                it = it.replace('<', ';')
                it = it.replace('>', ';')
                it = it.replace('"\\"', ';')
                it = it.split(';')
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

            it = cur.next()

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
                if (datetime.strptime(it[0].decode("utf-8"), "%y/%m/%d") <= datetime.strptime(term, "%y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('>=' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%y/%m/%d") >= datetime.strptime(term, "%y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('>' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%y/%m/%d") > datetime.strptime(term, "%y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('<' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%y/%m/%d") < datetime.strptime(term, "%y/%m/%d")):
                    item_id = get_id(it[1])
            elif ('=' in search):
                if (datetime.strptime(it[0].decode("utf-8"), "%y/%m/%d") == datetime.strptime(term, "%y/%m/%d")):
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
                if (datetime.strptime(item[1], "%y/%m/%d") <= datetime.strptime(term, "%y/%m/%d")):
                    new_data.append(item)
            elif ('>=' in search):
                if (datetime.strptime(item[1], "%y/%m/%d") >= datetime.strptime(term, "%y/%m/%d")):
                    new_data.append(item)
            elif ('>' in search):
                if (datetime.strptime(item[1], "%y/%m/%d") > datetime.strptime(term, "%y/%m/%d")):
                    new_data.append(item)
            elif ('<' in search):
                if (datetime.strptime(item[1], "%y/%m/%d") < datetime.strptime(term, "%y/%m/%d")):
                    new_data.append(item)
            elif ('=' in search):
                if (datetime.strptime(item[1], "%y/%m/%d") == datetime.strptime(term, "%y/%m/%d")):
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
        it = cur.first()

        while it:
            if (term in it[0].decode("utf-8")):
                item_id = get_id(it[1])

            if (item_id != ''):
                item_ids.append(item_id)
                item_id = ''

            it = cur.next()

        cur.close()
        database.close()

        if ('%' in search):
            return (search_term(search, get_full_data(item_ids)))

        return get_full_data(item_ids)

    else:
        new_data = []

        for item in data:
            if ('%' in search):
                if (term == item[4][:len(term)] or term == item[5][:len(term)]):

                    print(item[4][:len(term)])
                    print(item[5][:len(term)])
                    new_data.append(item)

            else:
                if (term in item[4] or term in item[5]):
                    new_data.append(item)

            if (item_id != ''):
                item_ids.append(item_id)
                item_id = ''

        return new_data

