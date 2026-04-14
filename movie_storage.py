import json
import random

import requests
from matplotlib import pyplot

import movie_storage_sql as storage

COMMAND_RANGE = 11
API_KEY = "137c4ce9"
TEMPLATE_TITLE = "Masterschool's Movies App"


def print_movie(movie, data):
    print(f"{movie} ({data['year']}): {data['rating']}")


def print_movies(movies):
    for movie, data in movies.items():
        print_movie(movie, data)


def list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")

    print_movies(movies)


def api_search_movie(title):
    url = "http://www.omdbapi.com/?i=tt3896198&apikey=137c4ce9"
    params = {
        "t": title  # "t" = title search
    }
    data = None
    try:
        response = requests.get(url, params=params)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("\033[31mAPI not available.\033[0m")
    except json.decoder.JSONDecodeError as e:
        print("\033[31mJSON error.\033[0m")
    except ValueError as e:
        print("\033[31mValue error.\033[0m")
    except KeyError as e:
        print("\033[31mKey error.\033[0m")
    except IndexError as e:
        print("\033[31mIndex error.\033[0m")
    except Exception as e:
        print(f"\033[31mSomething went wrong: {e}.\033[0m")

    return data


def add_movie(title):
    """Adds a movie to the JSON file."""
    data = api_search_movie(title)
    if not data or data.get("Response") == "False":
        print(f"\033[31mError: The movie '{title}' was not found.\033[0m")
        return
    title = data.get("Title", "")
    try:
        year = int(data.get("Year", 0))
    except ValueError:
        print("year is null or invalid")
        return
    try:
        rating = float(data.get("imdbRating", 0))
    except ValueError:
        print("rating is invalid")
        return
    poster = data.get("Poster", "")
    if poster == "":
        print("Poster is invalid")
        return

    storage.add_movie(title, year, rating, poster)


def delete_movie(title):
    """Deletes a movie from the JSON file."""
    storage.delete_movie(title)


def update_movie(title, rating):
    """Updates a movie's rating in the JSON file."""
    storage.update_movie(title, rating)


def stats_movies():
    result = storage.statistics_movies()
    print(f"Average rating: {result['avg_rating']}")
    print(f"Median rating: {result['median_rating']}")
    print(f"Best movie: {'best_title'}, {result['best_rating']}")
    print(f"Worst movie: {'worst_title'}, {result['worst_rating']}")


def random_movie():
    movies = storage.list_movies()
    if movies == {}:
        print("no movie")
        return

    movie_key = list(movies.keys())[random.randint(0, len(movies) - 1)]
    movie_val = movies[movie_key]
    print_movie(movie_key, movie_val)


def search_movie():
    title = input("Enter part of movie name: ")

    movies = storage.search_movies(title)
    if movies is None:
        print(f'\033[31mThe movie "{title}" does not exist.\033[0m')
    else:
        print_movies(movies)


def movies_sorted_by_rating():
    movies = storage.list_movies(True)
    print_movies(movies)


def create_rating_histogram():
    movies = storage.list_movies()
    ratings = [movie["rating"] for movie in movies.values()]

    pyplot.hist(ratings, bins=5)
    pyplot.xlabel("Rating")
    pyplot.ylabel("Number of Movies")
    pyplot.title("Histogram of Movie Ratings")

    pyplot.show()


def serialize_movie(title, data):
    """
    serializes a movie to html file.
    :param title: title of the movie
    :param data: data of the movie
    """
    output = ''
    # append information to each string
    output += '<li class="movie">\n'
    output += f'<img src="{data["poster"]}" class="movie-poster" alt="{title}">\n'
    output += f'<div class="movie-title">{title}</div>\n'
    output += f'<div class="movie-year">{str(data["year"])}</div>\n'
    output += '</li>\n'
    return output


def generate_website():
    """
    Generates a website.
    """
    movies = storage.list_movies()
    # open and read file
    with open("./_static/index_template.html", "r") as file:
        content = file.read()

    # replace __TEMPLATE__
    content = content.replace("__TEMPLATE_TITLE__", TEMPLATE_TITLE)
    html_text = ""
    for title, data in movies.items():
        html_text += serialize_movie(title, data)
    content = content.replace("__TEMPLATE_MOVIE_GRID__", html_text)

    # write back to file
    with open("./_static/index.html", "w") as file:
        file.write(content)

    print("Website was generated successfully.")


def main():
    generate_website()


if __name__ == "__main__":
    main()
