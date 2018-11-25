from bsddb3 import db
from datetime import datetime
import re


def query(search):
    #Get an instance of BerkeleyDB
    # running = True
    full = 0        # "bool" for keeping track of output type: brief, full

    # while running:
    database = db.DB()

    # search = input("Enter a search term: ")
    term = ''
    open_db = ''
    item_id = ''


    if ('output' in search.lower()):
        if ('brief' in search.lower()):
            full = 0
        elif ('full' in search.lower()):
            full = 1
    elif (search == 'exit program'):
        running = False
        return

    else:

        if ('date' in search.lower()):
            database.open("da.idx")
            term = search[-10:]
            open_db = 'date'
        elif ('price' in search.lower()):
            database.open("pr.idx")
            open_db = 'price'
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
        else:
            database.open("te.idx")
            open_db = 'terms'
            if ('%' in search):
                term = search[0:len(search)-1]
            else:
                term = search

        cur = database.cursor()
        it = cur.first()

        item_ids = []
        while it:
            if (open_db == 'terms'):
                if ('%' in search):
                    if (term in it[0].decode("utf-8")):
                        item_id = get_id(it[1])
                else:
                    if (term == it[0].decode("utf-8")):
                        item_id = get_id(it[1])
            elif (open_db == 'date'):
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
            elif (open_db == 'price'):
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

        database2 = db.DB()
        database2.open('ad.idx')
        date = ''
        loc = ''
        cat = ''
        desc = ''
        price = ''
        for entry in item_ids:
            cur2 = database2.cursor()
            it = cur2.first()

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

                    if not full:
                            print(entry + " | " + title)
                    else:
                        print(entry + " | " + date + " | " + loc + " | " + cat + " | " + title + " | " + desc + " | " + price)


                it = cur2.next()
                

        cur.close()
        cur2.close()
        database.close()
        database2.close()

def get_id(it):
    it = it.decode("utf-8")
    items = it.split(',')
    return items[0]
