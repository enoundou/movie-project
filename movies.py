import movie_storage  # this is the old movie storage file


def command_list_movies():
    movie_storage.list_movies()
    ...


def command_add_movie():
    title = input("\nEnter new movie name: ")
    year = input("Enter new movie year: ")
    rating = input("Enter new movie rating: ")
    movie_storage.add_movie(title, year, rating)
    ...


def command_delete_movie():
    title = input("\nEnter movie name to delete: ")
    movie_storage.delete_movie(title)
    ...


def command_update_movie():
    title = input("\nEnter movie name to update: ")
    rating = input("Enter movie rating: ")
    movie_storage.update_movie(title, rating)


def command_statistics():
    """
    Show the statistics of movies
    """
    movie_storage.stats_movies()


def command_random_movie():
    """
    Show a random movie from the database
    """

    movie_storage.random_movie()
    ...

def command_search_movie():
    """
    search movie by name
    :return:
    """
    movie_storage.search_movie()


def command_movies_sorted_by_rating():
    """
    Show the movies sorted by rating
    :return:
    """
    movie_storage.movies_sorted_by_rating()


def command_create_rating_histogram():
    """
    Create a histogram of the ratings
    :return:
    """
    movie_storage.create_rating_histogram()


def command_generate_website():
    pass


def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("\nMenu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input("\nEnter choice (0-10): "))
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            pass
        print("\033[31mTry again...\033[0m")


"""
Function Dispatch Dictionary
"""
FUNCTIONS = {0: (quit, "Exit"),
             1: (command_list_movies, "List movies"),
             2: (command_add_movie, "Add movie"),
             3: (command_delete_movie, "Delete movie"),
             4: (command_update_movie, "Update movie"),
             5: (command_statistics, "Statistics"),
             6: (command_random_movie, "Random movie"),
             7: (command_search_movie, "Search movie"),
             8: (command_movies_sorted_by_rating, "Movies sorted by rating"),
             9: (command_generate_website, "Generate website"),
             10: (command_create_rating_histogram, "Create rating histogram")
             }


def main():
    # The Main Menu loop
    while True:
        # Print menu and Get command from user
        choice_func = show_menu_and_get_input()
        # Execute command
        print()
        choice_func()
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
