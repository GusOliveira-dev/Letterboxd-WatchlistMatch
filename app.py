from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from collections import Counter
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from imdb import IMDb
import random


load_dotenv()

app = Flask(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

poster_cache = {}

def get_watchlist(username):
    movies = []
    page = 1
    while True:
        url = f"https://letterboxd.com/{username}/watchlist/page/{page}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        posters = soup.select('li.poster-container')

        if not posters:
            break 

        for item in posters:
            img_tag = item.find('img')
            if img_tag and img_tag.has_attr('alt'):
                title = img_tag['alt']
                movies.append(title)
        page += 1

    return movies


def get_poster(title):
    if title in poster_cache:
        return poster_cache[title]

    try:
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title
        }

        response = requests.get(search_url, params=params)
        data = response.json()

        if data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                poster_cache[title] = poster_url
                return poster_url
    except Exception as e:
        print(f"[TMDb ERROR] {e}")

    poster_cache[title] = "/static/default.jpg"
    return "/static/default.jpg"


@app.route('/', methods=['GET', 'POST'])
def index():
    common = None 
    percent = None
    highlight = None 

    if request.method == 'POST':
        common = []
        user1 = request.form['user1']
        user2 = request.form['user2']
        w1 = get_watchlist(user1)
        w2 = get_watchlist(user2)

        titles1 = set(w1)
        titles2 = set(w2)
        common_titles = titles1 & titles2

        for title in sorted(common_titles):
            poster = get_poster(title)
            common.append({
                'title': title,
                'img': poster or '/static/default.jpg'
            })

        total = len(titles1 | titles2)
        match = len(common_titles)
        highlight = None
        if common:
            highlight = random.choice(common)

    return render_template('index.html', common=common, percent=percent, highlight=highlight)

if __name__ == "__main__":
    app.run(debug=True)
