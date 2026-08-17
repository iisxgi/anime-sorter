
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
        amount_rated = len(ratings)

        genre_averages[genre] = {
            "average": average,
            "count": amount_rated
        }


    # Calculate confidence-weighted scores
    for genre, data in genre_averages.items():
        average = data["average"]
        count = data["count"]

        confidence = min(count / 5, 1)

        weighted_score = (average * confidence) + (5 * (1 - confidence))

        data["weighted_score"] = weighted_score


    # Sort genres by weighted score
    sorted_genres = sorted(
        genre_averages.items(),
        key=lambda item: item[1]["weighted_score"],
        reverse=True
    )
        

        # Display the genres
    for number, (genre, data) in enumerate(sorted_genres, start=1):
        average = data["average"]
        count = data["count"]
        weighted_score = data["weighted_score"]

        print(
            f"{number}. {genre} | "
            f"Average: {average:.1f}/10 | "
            f"Rated: {count} | "
            f"Preference Score: {weighted_score:.1f}/10"
        )

    # Display the favourite genre
    if sorted_genres:
        favourite_genre = sorted_genres[0][0]
        favourite_data = sorted_genres[0][1]

        favourite_average = favourite_data["average"]
        favourite_score = favourite_data["weighted_score"]

        print(
            f"\nYour favourite genre is {favourite_genre} "
            f"with an average rating of {favourite_average:.1f}/10 "
            f"and a preference score of {favourite_score:.1f}/10!"
        )

    # Give the calculated preferences back to whoever called this function
    return sorted_genres

# Get anime recommendations from AniList
def get_anime_by_genre(genre_name):
    url = "https://graphql.anilist.co"

    query = """
    query ($genre: String) {
        Page(page: 1, perPage: 20) {
            media(
                type: ANIME,
                genre: $genre,
                sort: SCORE_DESC,
                isAdult: false
            ) {
                title {
                    romaji
                }
                averageScore
                genres
            }
        }
    }
    """

    variables = {
        "genre": genre_name
    }

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": variables
        }
    )

    if response.status_code == 200:
        data = response.json()
        return data["data"]["Page"]["media"]
    else:
        print(f"API error: {response.status_code}")
        return None


def calculate_match_score(anime, preferences):
    preference_dict = dict(preferences)

    anime_genres = anime["genres"]
    
    matching_scores = []

    for genre in anime_genres:
        if genre in preference_dict:
            matching_scores.append(preference_dict[genre])

    if not matching_scores:
        return 0

    match_score = sum(matching_scores) / len(matching_scores)

    return match_score

def recommend_anime():
    preferences = show_preferences()

    if not preferences:
        print("Not enough data to make recommendations.")
        return

    favourite_genre = preferences[0][0]

    print(f"\nSearching for {favourite_genre} anime...")

    recommendations = get_anime_by_genre(favourite_genre)

    if not recommendations:
        print("Could not find any recommendations.")
        return

    watched_anime = []

    for anime in animes:
        watched_anime.append(anime["name"].lower())

    new_recommendations = []

    for anime in recommendations:
        if anime["title"]["romaji"].lower() not in watched_anime:
            new_recommendations.append(anime)

    scored_recommendations = []

    for anime in new_recommendations:
        match_score = calculate_match_score(anime, preferences)

        scored_recommendations.append(
            (anime, match_score)
        )

    scored_recommendations.sort(
        key=lambda item: item[1],
        reverse=True
    )

    print("\n===== PERSONALISED RECOMMENDATIONS =====")

    for anime, match_score in scored_recommendations:
        print(
            f"- {anime['title']['romaji']} | "
            f"Personal Match: {match_score:.1f}/10 | "
            f"AniList Score: {anime['averageScore']}/100"
        )



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

