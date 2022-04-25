from flask import Flask, render_template, request
import requests
import urllib.request
import re
import os

API_KEY = os.environ.get("API_KEY")
ENDPOINT = "https://api.themoviedb.org/3/"



popular = []
now_playing = []
trending = []
for i in range(1, 5):
    params = {
        "api_key": API_KEY,
        "region": "US",
        "page": i,
    }
    get_popular = requests.get(f"{ENDPOINT}movie/popular", params=params)
    get_popular_data = get_popular.json()["results"]
    for movie in get_popular_data:
        if movie["original_language"] == "en" and movie["poster_path"]:
            popular.append(movie)


for i in range(1, 2):
    params = {
        "api_key": API_KEY,
        "region": "US",
        "page": i,
    }
    get_now_playing = requests.get(f"{ENDPOINT}movie/now_playing", params=params)
    get_now_playing_data = get_now_playing.json()["results"]
    for movie in get_now_playing_data:
        if movie["original_language"] == "en" and movie["poster_path"]:
            now_playing.append(movie)


for i in range(1, 2):
    params = {
        "api_key": API_KEY,
        "region": "US",
        "page": i,
    }
    get_trending = requests.get(f"{ENDPOINT}trending/movie/week", params=params)
    get_trending_data = get_trending.json()["results"]
    for movie in get_trending_data:
        if movie["original_language"] == "en" and movie["poster_path"]:
            trending.append(movie)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", popular=popular, now_playing=now_playing, trending=trending)


@app.route("/details")
def details():
    parameters = {
        "api_key": API_KEY,
        "language": "en",
        "region": "US"
    }
    get_genre = requests.get(f"{ENDPOINT}genre/movie/list", params=parameters)
    genre_id = get_genre.json()['genres']

    movie_id = request.args.get("id")
    movie_name = request.args.get("name").split()
    genres = request.args.get("genre")

    get_similar = requests.get(f"{ENDPOINT}movie/{movie_id}/recommendations", params=params)
    get_similar_data = get_similar.json()["results"]
    get_similar_data_2 = []
    for data in get_similar_data:
        if data["original_language"] == "en" and movie["poster_path"]:
            get_similar_data_2.append(data)


    genre_names = None
    for genre in genre_id:
        if int(genres) == int(genre["id"]):
            genre_names = genre["name"]

    search_name = ""
    for tag in movie_name:
        name = tag + "+"
        search_name += name

    search_movie = f"{search_name}trailer"
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_movie)
    video = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    link = ("https://www.youtube.com/embed/" + video[0])

    get_movie = requests.get(f"{ENDPOINT}movie/{movie_id}", params=params)
    movie_data = get_movie.json()

    return render_template("details.html", link=link, data=movie_data, genre=genre_names, similar_movies=get_similar_data_2)


@app.route("/search", methods=["GET", "POST"])
def search():
    movie_name = request.form.get("name")
    parameters = {
        "api_key": API_KEY,
        "query": movie_name,
        "region": "US"
    }
    search_movie = requests.get(f"{ENDPOINT}search/movie", params=parameters)
    search_movie_data = search_movie.json()["results"]
    search_movie_data_2 = []
    for movie in search_movie_data:
        if movie["poster_path"] and movie["original_language"] == "en":
            search_movie_data_2.append(movie)
    return render_template("search.html", name=movie_name, data=search_movie_data_2)


if __name__ == "__main__":
    app.run(debug=True)
