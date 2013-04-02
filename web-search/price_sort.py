## take the input as a json doc from mongodb or simply a result of find_one operation
import re
import operator

def sort_prices(cursor):
    web_list = ['Bookadda', 'Crossword', 'Homeshop18', 'Infibeam', 'Rediffbook', 'flipkart']
    price =  {}

    for site in web_list:
        price[site] = cursor.get(site)

    p = re.compile(r'\d+')

    for k, v in price.items():
        if v == None or v == 'None':
            del price[k]

    for k, v in price.items():
        i = v.replace(',', '')
        price[k] = i

    for k, v in price.items():
        if p.search(v):
            price[k] = int(p.search(v).group())

    return sorted(price.iteritems(), key=operator.itemgetter(1))

