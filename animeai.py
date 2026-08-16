
import json
import os

print("JSON FILE IS HERE: ")
print(os.path.abspath("animes_data.json"))

#creating a function to load the animes list from a json file
def load_animes():
    try:
        with open("animes_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

#creating a function to save the animes list to a json file
def save_animes():
    with open("animes_data.json", "w") as file:
        json.dump(animes, file, indent=4)


#anime variables
animes = load_animes()

#creating a function to add an anime to the list
def add_anime(name, rating, genre, status):
    anime = {
        "name": name,
        "rating": rating,
        "genre": genre,
        "status": status
    }
    animes.append(anime)
    print(f"Anime '{name}' added successfully!")
    save_animes()

#creating a function to display all animes in the list
def show_animes():
    for number, anime in enumerate(animes, start=1):
        genres = ", ".join(anime['genre'])  # Join the list of genres into a string
        print(
            f"{number}. {anime['name']} | "
            f"{anime['rating']}/10 | "
            f"{genres} | "
            f"{anime['status']}"
        )

#creating a menu for the user to interact with
while True:
    print("\n===== ANIME AI =====")
    print("1. Add Anime")
    print("2. View anime list")
    print("3. Get anime recommendations")
    print("4. View my preferences")
    print("5. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        name = input("Enter anime name: ")
        rating = input("Enter anime rating (1-10): ")
        genre_input = input("Enter anime genres (seperate with commas): ")
        genre = [genre.strip().title() for genre in genre_input.split(",")]
        status = input("Enter anime status (watching, completed, on-hold, dropped): ")
        add_anime(name, rating, genre, status)

    elif choice == "2":
        print("\nYour Anime List:")
        show_animes()

    elif choice == "3":
        print("\nAnime Recommendation system coming soon!:")

    elif choice == "4":
        print("\nPreference system coming soon!")


    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose 1-5.")




