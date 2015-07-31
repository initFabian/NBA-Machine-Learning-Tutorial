import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

'''
PER
    FGM - totals.FG
    Stl - totals.STL
    3PTM - totals.3P
    FTM - totals.FT
    Blk - totals.BLK
    Off_Reb - totals.ORB
    Ast - totals.AST
    Def_Reb - totals.DRB
    Foul - totals.PF
    FT_Miss - totals.FTA-totals.FT
    FG_Miss - totals.FGA-totals.FG
    TO - totals.TOV
'''

PER_FEATURES = [
    'FG',
    'STL',
    '3P',
    'FT',
    'BLK',
    'ORB',
    'AST',
    'DRB',
    'PF',
    'FT_M', #FT_Miss - totals.FTA-totals.FT
    'FG_M', #FG_Miss - totals.FGA-totals.FG
    'TOV',
    'MP'
]

WANTED_FEATURES = {
    'Seasons.advanced.PER': 1,  # double
    'Seasons.totals.MP': 1,     # Int32
    'Seasons.totals.STL': 1,    # Int32
    'Seasons.totals.3P': 1,     # Int32
    'Seasons.totals.FT': 1,     # Int32
    'Seasons.totals.BLK': 1,    # Int32
    'Seasons.totals.ORB': 1,    # Int32
    'Seasons.totals.AST': 1,    # Int32
    'Seasons.totals.DRB': 1,    # Int32
    'Seasons.totals.PF': 1,     # Int32
    'Seasons.totals.FTA': 1,    # Int32
    'Seasons.totals.FGA': 1,    # Int32
    'Seasons.totals.FG': 1,     # Int32
    'Seasons.totals.TOV': 1     # Int32
}


# Connect to MongoDB
def connectMongo(db, host='localhost', port=27017, mongo_uri=None):

    """ A util for making a connection to mongo """

    if mongo_uri:
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

def readMongo(db, collection, query={}, queryReturn=None,
                _limit=None,no_id=True,mongo_uri=None):

    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = connectMongo(db=db, mongo_uri=mongo_uri)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query, queryReturn)

    # Check if a limit was set
    if _limit:
        cursor = cursor.limit(_limit)
    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df