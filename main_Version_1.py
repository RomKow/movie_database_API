import statistics
import random
from colorama import init, Fore, Style

def main():
    init(autoreset=True)
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }

    while True:
        # Menu in cyan
        print(Fore.CYAN + "\n********** My Movies Database **********\n" + Style.RESET_ALL)
        print(Fore.CYAN + "Menu:" + Style.RESET_ALL)
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")

        # Input prompt in green
        choice = input(Fore.GREEN + "Enter choice (1-8): " + Style.RESET_ALL).strip()

        if choice == '1':
            count = len(movies)
            print(f"{count} movie{'s' if count != 1 else ''} in total")
            for name, rating in movies.items():
                print(f"{name}: {rating}")

        elif choice == '2':
            name = input("Enter movie name: ").strip()
            rating = float(input("Enter rating (1-10): ").strip())
            movies[name] = rating
            print(f"Added '{name}' with rating {rating}.")

        elif choice == '3':
            name = input("Enter movie name to delete: ").strip()
            if name in movies:
                del movies[name]
                print(f"Deleted '{name}'.")
            else:
                print(Fore.RED + f"Error: Movie '{name}' not found." + Style.RESET_ALL)

        elif choice == '4':
            name = input("Enter movie name to update: ").strip()
            if name in movies:
                rating = float(input("Enter new rating (1-10): ").strip())
                movies[name] = rating
                print(f"Updated '{name}' to rating {rating}.")
            else:
                print(Fore.RED + f"Error: Movie '{name}' not found." + Style.RESET_ALL)

        elif choice == '5':
            if not movies:
                print("No movies in database.")
            else:
                ratings = list(movies.values())
                avg = statistics.mean(ratings)
                med = statistics.median(ratings)
                max_rating = max(ratings)
                min_rating = min(ratings)
                best = [n for n, r in movies.items() if r == max_rating]
                worst = [n for n, r in movies.items() if r == min_rating]
                print(f"Average rating: {avg:.2f}")
                print(f"Median rating: {med:.2f}")
                print(f"Best movie{'s' if len(best)>1 else ''} ({max_rating}): {', '.join(best)}")
                print(f"Worst movie{'s' if len(worst)>1 else ''} ({min_rating}): {', '.join(worst)}")

        elif choice == '6':
            if not movies:
                print("No movies in database.")
            else:
                name = random.choice(list(movies.keys()))
                print(f"Random pick: {name}, {movies[name]}")

        elif choice == '7':
            query = input("Enter part of movie name: ").strip().lower()
            # Search without list comprehension
            results = []
            for n, r in movies.items():
                if query in n.lower():
                    results.append((n, r))
            if results:
                for n, r in results:
                    print(f"{n}, {r}")
            else:
                print("No matching movies found.")

        elif choice == '8':
            for n, r in sorted(movies.items(), key=lambda x: x[1], reverse=True):
                print(f"{n}: {r}")

        else:
            print(Fore.RED + "Invalid choice, please enter a number between 1 and 8." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
