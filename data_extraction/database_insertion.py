import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from ast import literal_eval
import re

# Use a service account
cred = credentials.Certificate('resources/movielix-36036-c50612a3eafd.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

df = pd.read_csv('resources/cleaned_movies.csv', converters={'9': literal_eval})
df.fillna(' ', inplace=True)
df = df.drop(columns=['7'])
movies_dict = df.T.to_dict().values()


for movie in movies_dict:
    try:
        id = movie['1']
        del movie['1']
        db.collection('movies').add(movie, document_id=id)
    except Exception as e:
        print(e)
        print(movie)


df_suggestion = df[['1', '2', '3', '8', '9']]
suggestion_dict = df_suggestion.T.to_dict().values()


for suggestion in suggestion_dict:
    try:
        id = suggestion['1']
        del suggestion['1']
        db.collection('movies_suggestions').add(suggestion, document_id=id)
    except Exception as e:
        print(e)
        print(suggestion)


df_search = df[['1', '2']]
df_search['2'] = df_search['2'].map(lambda x: x.lower())
df_search['2'] = df_search['2'].map(lambda x: re.sub(r'[^áéíóúüñÑA-Za-z0-9\s]', "", x))
df_search['2'] = df_search['2'].map(lambda x: x.replace('ñ', '-&-'))
df_search['2'] = df_search['2'].str.normalize('NFKD').\
    str.encode('ascii', errors='ignore').str.decode('utf-8')
df_search['2'] = df_search['2'].map(lambda x: x.replace('-&-', 'ñ'))
df_search['3'] = df_search['2'].map(lambda x: x.split())
search_dict = df_search.T.to_dict().values()

for search in search_dict:
    try:
        id = search['1']
        del search['1']
        db.collection('movies_search').add(search, document_id=id)
    except Exception as e:
        print(e)
        print(search)


df_lite = df[['1', '2', '3', '5', '6', '8', '9', '10']]
lite_dict = df_lite.T.to_dict().values()

for lite in lite_dict:
    try:
        id = lite['1']
        del lite['1']
        db.collection('movies_lite').add(lite, document_id=id)
    except Exception as e:
        print(e)
        print(lite)
