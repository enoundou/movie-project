from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)
QUERY_LIST_MOVIES = "SELECT title, year, rating, poster FROM movies "
QUERY_FIND_MOVIE = "SELECT title, year, rating, poster FROM movies  WHERE title = :title"
QUERY_ADD = "INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"
QUERY_DELETE = "DELETE FROM movies WHERE title = :title"
QUERY_UPDATE = "UPDATE movies set rating = :rating WHERE title = :title"
QUERY_STATISTICS = """SELECT AVG(rating) AS                                 avg_rating,
                             (SELECT title FROM movies ORDER BY rating DESC LIMIT 1) AS best_title,
    MAX(rating) AS best_rating,
    (SELECT title FROM movies ORDER BY rating ASC LIMIT 1) AS worst_title,
    MIN(rating) AS worst_rating,
    (
        SELECT AVG(rating)
        FROM (
            SELECT rating
            FROM movies
            ORDER BY rating
            LIMIT 2 - (SELECT COUNT(*) FROM movies) % 2
            OFFSET (SELECT (COUNT(*) - 1) / 2 FROM movies)
        )
    ) AS median_rating
                      FROM movies;"""

QUERY_SEARCH_MOVIES = "SELECT title, year, rating, poster FROM movies WHERE Upper(title) like  Upper(:title) "

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS movies
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                title
                                TEXT
                                UNIQUE
                                NOT
                                NULL,
                                year
                                INTEGER
                                NOT
                                NULL,
                                rating
                                REAL
                                NOT
                                NULL,
                                poster
                                TEXT
                                NOT
                                NULL
                            )
                            """))
    connection.commit()


def list_movies(sorted_by_rating=False):
    """
    list all movies in the database
    :param sorted_by_rating: oder sorted by rating or not
    :return:
    """
    with engine.connect() as connection:
        if sorted_by_rating:
            result = connection.execute(text(QUERY_LIST_MOVIES + " ORDER BY rating DESC"))
        else:
            result = connection.execute(text(QUERY_LIST_MOVIES))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def exist_movie(con, title):
    exist = False
    result = con.execute(text(QUERY_FIND_MOVIE),
                         {"title": title})
    movie = result.fetchall()
    if len(movie) > 0:
        exist = True

    return exist


def add_movie(title, year, rating, poster):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            if exist_movie(connection, title):
                raise Exception(f"Movie '{title}' is already out!")

            connection.execute(text(QUERY_ADD),
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            if not exist_movie(connection, title):
                raise Exception(f"Movie '{title}' doesn't exist!")

            connection.execute(text(QUERY_DELETE),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            if not exist_movie(connection, title):
                raise Exception(f"Movie '{title}' doesn't exist!")

            connection.execute(text(QUERY_UPDATE),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")


def statistics_movies():
    """Retrieve statistics about all movies in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text(QUERY_STATISTICS))
            row = result.fetchone()
            if row is None:
                return None

            return {
                "avg_rating": row[0],
                "best_title": row[1],
                "best_rating": row[2],
                "worst_title": row[3],
                "worst_rating": row[4],
                "median_rating": row[5],
            }
        except Exception as e:
            print("Error:", e)
            return None


def search_movies(title):
    with engine.connect() as connection:
        try:
            result = connection.execute(text(QUERY_SEARCH_MOVIES),
                                        {"title": f"%{title}%"})
            movies = result.fetchall()
        except Exception as e:
            print("Error:", e)

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}
