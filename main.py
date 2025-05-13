import statistics
import random
import movie_storage
from colorama import init, Fore, Style  # noqa: E0401


def print_menu():
    """Print the main menu."""
    print(Fore.CYAN + "\n********** My Movies Database **********\n" + Style.RESET_ALL)
    print(Fore.CYAN + "Menu:" + Style.RESET_ALL)
    print(Fore.CYAN + "0. Exit" + Style.RESET_ALL)
    print(Fore.CYAN + "1. List movies" + Style.RESET_ALL)
    print(Fore.CYAN + "2. Add movie" + Style.RESET_ALL)
    print(Fore.CYAN + "3. Delete movie" + Style.RESET_ALL)
    print(Fore.CYAN + "4. Update movie rating" + Style.RESET_ALL)
    print(Fore.CYAN + "5. Stats" + Style.RESET_ALL)
    print(Fore.CYAN + "6. Random movie" + Style.RESET_ALL)
    print(Fore.CYAN + "7. Search movie" + Style.RESET_ALL)
    print(Fore.CYAN + "8. Movies sorted by rating" + Style.RESET_ALL)


def list_movies(_: dict = None) -> None:
    """List all movies by loading them from storage."""
    movies = movie_storage.get_movies()
    count = len(movies)
    suffix = 's' if count != 1 else ''
    print(f"{count} movie{suffix} in total")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def add_movie(_: dict = None) -> None:
    """Add a new movie to the database via storage."""
    title = input("Enter movie title: ").strip()
    year = int(input("Enter year of release: ").strip())
    rating = float(input("Enter rating (1-10): ").strip())
    movies = movie_storage.get_movies()
    if title in movies:
        print(Fore.RED + f"Error: Movie '{title}' already exists." + Style.RESET_ALL)
        return
    movie_storage.add_movie(title, year, rating)
    print(f"Added '{title}' ({year}) with rating {rating}.")


def delete_movie(_: dict = None) -> None:
    """Delete a movie from the database via storage."""
    title = input("Enter movie title to delete: ").strip()
    movies = movie_storage.get_movies()
    if title not in movies:
        print(Fore.RED + f"Error: Movie '{title}' not found." + Style.RESET_ALL)
        return
    movie_storage.delete_movie(title)
    print(f"Deleted '{title}'.")


def update_movie_rating(_: dict = None) -> None:
    """Update the rating of an existing movie via storage."""
    title = input("Enter movie title to update rating: ").strip()
    movies = movie_storage.get_movies()
    if title not in movies:
        print(Fore.RED + f"Error: Movie '{title}' not found." + Style.RESET_ALL)
        return
    rating = float(input("Enter new rating (1-10): ").strip())
    movie_storage.update_movie(title, rating)
    print(f"Updated '{title}' to new rating {rating}.")


def show_stats(_: dict = None) -> None:
    """Show statistics: average, median, best and worst movies."""
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in database.")
        return
    ratings = [info['rating'] for info in movies.values()]
    avg_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)
    best_movies = [t for t, info in movies.items() if info['rating'] == max_rating]
    worst_movies = [t for t, info in movies.items() if info['rating'] == min_rating]
    print(f"Average rating: {avg_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    plural_best = 's' if len(best_movies) > 1 else ''
    plural_worst = 's' if len(worst_movies) > 1 else ''
    print(f"Best movie{plural_best} ({max_rating}): {', '.join(best_movies)}")
    print(f"Worst movie{plural_worst} ({min_rating}): {', '.join(worst_movies)}")


def pick_random_movie(_: dict = None) -> None:
    """Pick and show a random movie."""
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in database.")
        return
    title, info = random.choice(list(movies.items()))
    print(f"Random pick: {title} ({info['year']}), {info['rating']}")


def search_movies(_: dict = None) -> None:
    """Search for movies by partial title."""
    movies = movie_storage.get_movies()
    query = input("Enter part of movie title: ").strip().lower()
    results = [(t, info) for t, info in movies.items() if query in t.lower()]
    if results:
        for t, info in results:
            print(f"{t} ({info['year']}), {info['rating']}")
    else:
        print("No matching movies found.")


def movies_sorted_by_rating(_: dict = None) -> None:
    """List movies sorted by rating descending."""
    movies = movie_storage.get_movies()
    sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for t, info in sorted_list:
        print(f"{t} ({info['year']}): {info['rating']}")


def main() -> None:
    """Main entry point for the movies CLI application."""
    init(autoreset=True)
    actions = {
        '0': lambda: print("Bye!"),
        '1': list_movies,
        '2': add_movie,
        '3': delete_movie,
        '4': update_movie_rating,
        '5': show_stats,
        '6': pick_random_movie,
        '7': search_movies,
        '8': movies_sorted_by_rating
    }
    while True:
        print_menu()
        choice = input(Fore.GREEN + "Enter choice (0-8): " + Style.RESET_ALL).strip()
        action = actions.get(choice)
        if not action:
            print(Fore.RED + "Invalid choice, please enter a number between 0 and 8." + Style.RESET_ALL)
            continue
        if choice == '0':
            action()
            break
        action()


if __name__ == "__main__":
    main()
