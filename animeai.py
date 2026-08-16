
import json
import requests
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
#creating a function to delete an anime from the list
def delete_anime():
    show_animes()
    number = int(input("\nEnter the number of the anime you want to delete: "))
    removed_anime = animes.pop(number - 1)
    save_animes()
    print(f"Anime '{removed_anime['name']}' deleted successfully!")

#creating a function to edit an anime in the list
def edit_anime():
    show_animes()

    number = int(input("\nEnter the number of the anime you want to edit: "))

    anime = animes[number - 1]

    print(f"\nEditing: {anime['name']}")
    print("Press Enter to keep the current value.\n")

    name = input(f"Name [{anime['name']}]: ")
    rating = input(f"Rating [{anime['rating']}]: ")

    current_genres = ", ".join(anime["genre"])
    genre_input = input(f"Genres [{current_genres}]: ")

    status = input(f"Status [{anime['status']}]: ")

    if name:
        anime["name"] = name

    if rating:
        anime["rating"] = rating

    if genre_input:
        anime["genre"] = [
            genre.strip().title()
            for genre in genre_input.split(",")
        ]

    if status:
        anime["status"] = status

    save_animes()

    print(f"\nAnime '{anime['name']}' updated successfully!")

#Creating a preference function to get the user's preferred genres and ratings
# Creating a preference function to get the user's preferred genres and ratings
def show_preferences():
    genre_ratings = {}

    # Go through every anime
    for anime in animes:
        rating = int(anime["rating"])

        # Go through every genre belonging to that anime
        for genre in anime["genre"]:

            # If we haven't seen this genre before, create an empty list
            if genre not in genre_ratings:
                genre_ratings[genre] = []

            # Add the anime's rating to that genre
            genre_ratings[genre].append(rating)

    # Calculate the average rating for each genre
    genre_averages = {}

    for genre, ratings in genre_ratings.items():
        average = sum(ratings) / len(ratings)
        genre_averages[genre] = average

    # Sort genres from highest average rating to lowest
    sorted_genres = sorted(
        genre_averages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # Display the genres
    for number, (genre, average) in enumerate(sorted_genres, start=1):
        print(f"{number}. {genre}: {average:.1f}/10")

    # Display the favourite genre
    if sorted_genres:
        favourite_genre = sorted_genres[0][0]
        favourite_score = sorted_genres[0][1]

        print(
            f"\nYour favourite genre is {favourite_genre} "
            f"with an average rating of {favourite_score:.1f}/10!"
        )

    # Give the calculated preferences back to whoever called this function
    return sorted_genres

#linking an api
def search_anime(anime_name):
    url = "https://api.jikan.moe/v4/anime"

    params = {
        "q": anime_name,
        "limit": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"API error: {response.status_code}")
        return None
    

    
def get_anime_by_genre(genre_id):
    url = "https://api.jikan.moe/v4/anime"

    params = {
        "genres": genre_id,
        "order_by": "score",
        "sort": "desc",
        "limit": 10
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        print(f"API error: {response.status_code}")
        return None


def get_genre_id(genre_name):
    genre_ids = {
        "Action": 1,
        "Adventure": 2,
        "Comedy": 4,
        "Mystery": 7,
        "Drama": 8,
        "Fantasy": 10,
        "Horror": 14,
        "Romance": 22,
        "Sci-Fi": 24,
        "Sports": 30,
        "Slice of Life": 36,
        "Supernatural": 37,
        "Suspense": 41
    }

    return genre_ids.get(genre_name)



def recommend_anime():
    preferences = show_preferences()

    if not preferences:
        print("Not enough data to make recommendations.")
        return

    favourite_genre = preferences[0][0]

    print(f"\nSearching for {favourite_genre} anime...")

    genre_id = get_genre_id(favourite_genre)

    if genre_id is None:
        print("Could not find that genre.")
        return

    print(f"Genre ID found: {genre_id}")

    recommendations = get_anime_by_genre(genre_id)

    if not recommendations:
        print("Could not find any recommendations.")
        return

    print("\nTop recommendations:")

    for anime in recommendations:
        print(f"- {anime['title']} | Score: {anime['score']}")


#creating a menu for the user to interact with
while True:
    print("\n===== ANIME AI =====")
    print("1. Add Anime")
    print("2. View anime list")
    print("3. Edit anime")
    print("4. Delete anime")
    print("5. Get anime recommendations")
    print("6. View my preferences")
    print("7. Exit")


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
        print("\nEdit Anime: ")
        edit_anime()

    elif choice == "4":
        print("\nDelete Anime: ")
        delete_anime()


    elif choice == "5":
        print("\n===== ANIME RECOMMENDATIONS =====")
        recommend_anime()

    elif choice == "6":
        print("\nYour Preferences:")
        show_preferences()

    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose 1-7.")

