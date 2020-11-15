import pandas as pd
import numpy as np
import unicodedata as ud

LATIN_LETTERS = {}
NO_DESCR_MOVIE = "No hay una descripción en este momento"


def is_latin(uchr):
    try: return LATIN_LETTERS[uchr]
    except KeyError:
         return LATIN_LETTERS.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):
    return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def preprocess():
    df = pd.read_csv('resources/movies.csv', names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], header=None,
                     index_col=[0])

    df = df.replace(np.nan, ' ', regex=True)

    # remove non-latin alphabet characters
    df['2'] = df['2'].map(lambda x: x if only_roman_chars(x) else " ")
    df['4'] = df['4'].map(lambda x: NO_DESCR_MOVIE if pd.isna(x) else x)
    df['4'] = df['4'].map(lambda x: NO_DESCR_MOVIE if x == "" else x)

    # indexes_to_remove = df[df['original_title'].isnull()].index.tolist()
    # df.drop(index=indexes_to_remove)
    df['5'] = df['5'].map(lambda x: x.replace(" min", ""))
    df['5'] = df['5'].map(lambda x: x.replace(' ', '0'))
    df['5'] = df['5'].astype(int)

    df['6'] = df['6'].map(lambda x: x.replace(' ', '0'))
    df['6'] = df['6'].astype(float)

    df['10'] = df['10'].map(lambda x: " " if pd.isna(x) else x)

    df['10'] = df['10'].map(lambda x: x.replace("Not Rated", " "))
    df['10'] = df['10'].map(lambda x: x.replace("Unrated", " "))

    # replacing semicolon with dot for the votes
    df['7'] = df['7'].apply(lambda x: x.replace(',', '.'))

    # replacing string format
    df['9'] = df['9'].map(lambda x: x.replace("['", ""))
    df['9'] = df['9'].map(lambda x: x.replace("']", ""))
    df['9'] = df['9'].map(lambda x: x.replace("'", ""))
    df['9'] = df['9'].map(lambda x: x.split(","))

    df['3'] = pd.DatetimeIndex(df['3']).year

    df.to_csv('resources/cleaned_movies.csv')




