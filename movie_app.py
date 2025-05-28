import statistics
import random
from colorama import init, Fore, Style


class MovieApp:
    """
    Core application class to handle user interactions
    and delegate storage operations.
    """

    def __init__(self, storage):
        """
        Initialize MovieApp with a storage implementing IStorage.

        :param storage: Instance of IStorage
        """
        self._storage = storage
        init(autoreset=True)

    def _print_menu(self):
        """Display the main menu options."""
        print(Fore.CYAN + "\n********** My Movies Database **********\n" + Style.RESET_ALL)
        options = [
            "0. Exit",
            "1. List movies",
            "2. Add movie",
            "3. Delete movie",
            "4. Update movie rating",
            "5. Stats",
            "6. Random movie",
            "7. Search movie",
            "8. Movies sorted by rating",
        ]
        for opt in options:
            print(Fore.CYAN + opt + Style.RESET_ALL)

    def _command_list_movies(self):
        """List all movies."""
        movies = self._storage.list_movies()
        count = len(movies)
        suffix = 's' if count != 1 else ''
        print(f"{count} movie{suffix} in total")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")

    def _command_add_movie(self):
        """Add a new movie."""
        title = input("Enter movie title: ").strip()
        year = int(input("Enter year of release: ").strip())
        rating = float(input("Enter rating (1-10): ").strip())
        poster = input("Enter poster URL/path: ").strip()
        movies = self._storage.list_movies()
        if title in movies:
            print(Fore.RED + f"Error: Movie '{title}' already exists." + Style.RESET_ALL)
            return
        self._storage.add_movie(title, year, rating, poster)
        print(f"Added '{title}' ({year}) with rating {rating}.")

    def _command_delete_movie(self):
        """Delete an existing movie."""
        title = input("Enter movie title to delete: ").strip()
        movies = self._storage.list_movies()
        if title not in movies:
            print(Fore.RED + f"Error: Movie '{title}' not found." + Style.RESET_ALL)
            return
        self._storage.delete_movie(title)
        print(f"Deleted '{title}'.")

    def _command_update_movie_rating(self):
        """Update rating for an existing movie."""
        title = input("Enter movie title to update rating: ").strip()
        movies = self._storage.list_movies()
        if title not in movies:
            print(Fore.RED + f"Error: Movie '{title}' not found." + Style.RESET_ALL)
            return
        rating = float(input("Enter new rating (1-10): ").strip())
        self._storage.update_movie(title, rating)
        print(f"Updated '{title}' to new rating {rating}.")

    def _command_show_stats(self):
        """Show statistics: avg, median, best and worst movies."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database.")
            return
        ratings = [info['rating'] for info in movies.values()]
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        max_rating = max(ratings)
        min_rating = min(ratings)
        best = [t for t, info in movies.items() if info['rating'] == max_rating]
        worst = [t for t, info in movies.items() if info['rating'] == min_rating]
        plural_best = 's' if len(best) > 1 else ''
        plural_worst = 's' if len(worst) > 1 else ''
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie{plural_best} ({max_rating}): {', '.join(best)}")
        print(f"Worst movie{plural_worst} ({min_rating}): {', '.join(worst)}")

    def _command_pick_random_movie(self):
        """Pick and display a random movie."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database.")
            return
        title, info = random.choice(list(movies.items()))
        print(f"Random pick: {title} ({info['year']}), {info['rating']}")

    def _command_search_movies(self):
        """Search movies by partial title."""
        movies = self._storage.list_movies()
        query = input("Enter part of movie title: ").strip().lower()
        results = [(t, info) for t, info in movies.items() if query in t.lower()]
        if results:
            for t, info in results:
                print(f"{t} ({info['year']}), {info['rating']}")
        else:
            print("No matching movies found.")

    def _command_sorted_by_rating(self):
        """List movies sorted by descending rating."""
        movies = self._storage.list_movies()
        sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        for t, info in sorted_list:
            print(f"{t} ({info['year']}): {info['rating']}")

    def _generate_website(self):
        """Placeholder for static website generation logic."""
        pass

    def run(self):
        """Main loop: display menu, read input, dispatch commands."""
        commands = {
            '0': lambda: print("Bye!"),
            '1': self._command_list_movies,
            '2': self._command_add_movie,
            '3': self._command_delete_movie,
            '4': self._command_update_movie_rating,
            '5': self._command_show_stats,
            '6': self._command_pick_random_movie,
            '7': self._command_search_movies,
            '8': self._command_sorted_by_rating,
        }

        while True:
            self._print_menu()
            choice = input(Fore.GREEN + "Enter choice (0-8): " + Style.RESET_ALL).strip()
            action = commands.get(choice)
            if not action:
                print(Fore.RED + "Invalid choice, please enter a number between 0 and 8." + Style.RESET_ALL)
                continue
            if choice == '0':
                action()
                break
            action()
