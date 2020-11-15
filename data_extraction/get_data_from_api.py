import requests
import csv
from data_extraction.api_configuration import api_keys
from data_extraction.preprocessing import preprocessing


# The Movie Database Info
URL_MOVIE_DB = "https://api.themoviedb.org/3/movie/"
PARAMS = {'api_key': api_keys.api_keys['movie_db_api_key'], 'language': 'es-ES'}

# RapidApi info
URL_RAPID_API = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

headers_rapid_api = {
    'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com",
    'x-rapidapi-key': api_keys.api_keys['rapid_api_key']
    }

movies_not_found = 0


def get_movie_list():
    """
    API Get request to get the netflix movie list updated
    :return:
    """

    global movies_not_found
    querystring = {"q": "get:new1000:ES", "p": "1", "t": "ns", "st": "adv"}
    response = requests.request("GET", URL_RAPID_API, headers=headers_rapid_api, params=querystring)

    if response.status_code == 200:
        data = response.json()
        count = data['COUNT']
        print(count)
        '''
        for item in data['ITEMS']:
            if "tt" in item['imdbid']:
                image, runtime, imdb_rating, imdb_votes, rated = get_movie_image(item['imdbid'])
                get_movie_info(item['imdbid'], image, runtime, imdb_rating, imdb_votes, rated)
        '''
    else:
        print("RapidApi connection failed")
        return -1

    # We need to iterate as the results are in sets of 100

    iterations = int(count) // 100

    for i in range(2, iterations + 2):
        querystring = {"q": "get:new400:ES", "p": i, "t": "ns", "st": "adv"}
        response = requests.request("GET", URL_RAPID_API, headers=headers_rapid_api, params=querystring)
        data_page = response.json()
        for item in data_page['ITEMS']:
            if "tt" in item['imdbid']:
                image, runtime, imdb_rating, imdb_votes, rated = get_movie_image(item['imdbid'])
                get_movie_info(item['imdbid'], image, runtime, imdb_rating, imdb_votes, rated)


def get_movie_image(movie_id):

    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
    querystring = {"i": movie_id, "r": "json"}
    headers = {
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com",
        'x-rapidapi-key': "392eac5962mshd6cbfe2e3d4f643p17704bjsn75e2a2d6d3ab"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        try:
            runtime = data['Runtime']
            imdb_rating = data['imdbRating']
            imdb_votes = data['imdbVotes']
            try:
                rated = data['Rated']
            except Exception:
                rated = " "
            try:
                image = data['Poster']
            except Exception:
                print("error de imagen")
                image = ""
        except Exception :
            print(movie_id)
            image = " "
            imdb_votes = " "
            imdb_rating = " "
            runtime = " "
            rated = " "
        return image, runtime, imdb_rating, imdb_votes, rated
    else:
        return " ", " "


def get_movie_info(movie_id, image, runtime, imdb_rating, imdb_votes, rated):

    global movies_not_found

    if "tt" in movie_id:
        response = requests.get(URL_MOVIE_DB + movie_id, PARAMS)
        data = response.json()
        if response.status_code == 200:
            # interesting attributes
            row = []
            genre_list = []
            row.append(movie_id)
            row.append(data['title'])
            row.append(data['release_date'])
            row.append(data['overview'])
            row.append(runtime)
            row.append(imdb_rating)
            row.append(imdb_votes)
            row.append(image)

            for item in data['genres']:
                genre_list.append(item['name'])

            row.append(genre_list)
            row.append(rated)

            write_in_csv_file(row)
        else:
            movies_not_found += 1
    else:
        movies_not_found += 1


def write_in_csv_file(row):

    with open('resources/movies.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(row)


get_movie_list()
# print("Movies not found: " + str(movies_not_found))
# preprocessing.preprocess()
