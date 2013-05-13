from pymongo import MongoClient
import re
import math
import operator


con = MongoClient()
abhi = con.abhi
detail = abhi.Details
price = abhi.Review
ignore = abhi.ignore

def suggest_book(book, review):
    cluster_dict = {}
    recom_list = []
    o_isbn = book.get('_id')
    ## here original value start with o & comparative value start with n
    o_ap = int(review.get('avg_price'))
    o_rv = int(review.get('ratingValue'))
    o_rc = int(review.get('ratingCount'))

    name = str(book.get('name')).lower()
    '''ignore_cursor = ignore.find_one()
    ignore_list = ignore_cursor.values()[0]
    name = name.split()
    for e in ignore_list:
        if e in name:
            name.remove(e)
    name = ' '.join(name)'''

    cat  =  book.get('category')
    sub_cat = book.get('sub_category')
    #cluster =  detail.find({'category': re.compile(cat,re.IGNORECASE),
    #                        'sub_category': re.compile(sub_cat, re.IGNORECASE)},
    #                       {'_id':1})
    if cat:
        cluster = abhi.command("text","Details", search=name, filter={'category':cat, 'sub_category':sub_cat},
                 project={"_id": 1})
    else:
        cluster = abhi.command("text","Details", search=name, project={"_id": 1})
    cluster = cluster.get('results')

    for e in cluster:
        isbn = e.get('obj').get('_id')
        if isbn != o_isbn:
            res = price.find_one({'_id': isbn}, {'avg_price': 1, 'ratingCount': 1, 'ratingValue': 1})
            n_ap = int(res.get('avg_price'))
            n_rv = int(res.get('ratingValue'))
            n_rc = int(res.get('ratingCount'))
            distance = math.sqrt( (( o_ap - n_ap ) ** 2) + ( (o_rc - n_rc) ** 2) + ( (o_rv - n_rv) ** 2 ))
            norm_dist =  1 / (1+ distance)
            cluster_dict[isbn] = norm_dist

    result = sorted(cluster_dict.iteritems(), key=operator.itemgetter(1))#.reverse()
    result.reverse()
    result = result[0:4]
    for e in result:
        recom_list.append( detail.find_one({'_id': e[0]},{'name':1, 'image':1}) )

    return recom_list


