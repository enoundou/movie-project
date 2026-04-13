import random

from matplotlib import pyplot

import movie_storage_sql as storage

COMMAND_RANGE = 11



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


def add_movie(title, year, rating):
    """Adds a movie to the JSON file."""
    storage.add_movie(title, year, rating)


def delete_movie(title):
    """Deletes a movie from the JSON file."""
    storage.delete_movie(title)

def update_movie(title, rating):
    """Updates a movie's rating in the JSON file."""
    storage.update_movie(title, rating)
    
    
"""   

def enter_movie_rating(prompt):
    movie_rating = 0
    while True:
        try:
            movie_rating = float(input(prompt))
            if movie_rating < 0 or movie_rating > 10:
                raise ValueError
            else:
                break
        except ValueError:
            print("\033[31mPlease enter a positive number between 0 in 10.\033[0m")
            continue
    return movie_rating

"""
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
    movies= storage.list_movies(True)
    print_movies(movies)


def create_rating_histogram():
    movies= storage.list_movies()
    ratings = ratings = [movie["rating"] for movie in movies.values()]

    pyplot.hist(ratings, bins=5)
    pyplot.xlabel("Rating")
    pyplot.ylabel("Number of Movies")
    pyplot.title("Histogram of Movie Ratings")

    pyplot.show()


def generate_website(movies):
    pass


