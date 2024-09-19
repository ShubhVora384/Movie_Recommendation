import tkinter as tk
from tkinter import ttk
import requests

def get_movie_details_by_id(imdb_id, omdb_api_key):
    """
    Fetch detailed information for a movie by its IMDb ID from the OMDB API.
    """
    omdb_details_url = f'http://www.omdbapi.com/?apikey={omdb_api_key}&i={imdb_id}&plot=short&r=json'
    response = requests.get(omdb_details_url)
    if response.status_code == 200:
        movie_details = response.json()
        if movie_details['Response'] == 'True':
            return movie_details
    return None

def get_movie_recommendations(genre, omdb_api_key='7f82bbf4'):  # Default API key, replace with your own
    """
    Fetch movie recommendations based on the selected genre.
    """
    omdb_url = f'http://www.omdbapi.com/?apikey={omdb_api_key}&type=movie&s={genre}&r=json'
    response = requests.get(omdb_url)
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            movies = []
            page = 1
            total_results = int(data['totalResults'])
            while len(movies) < min(20, total_results):  # Fetch until 20 movies or all available movies
                omdb_url_page = f'http://www.omdbapi.com/?apikey={omdb_api_key}&type=movie&s={genre}&page={page}&r=json'
                response_page = requests.get(omdb_url_page)
                if response_page.status_code == 200:
                    data_page = response_page.json()
                    if data_page['Response'] == 'True':
                        for movie in data_page['Search']:
                            imdb_id = movie['imdbID']
                            movie_details = get_movie_details_by_id(imdb_id, omdb_api_key)
                            if movie_details and 'imdbRating' in movie_details and movie_details['imdbRating'] != "N/A":
                                title = movie_details['Title']
                                year = movie_details['Year']
                                rating = movie_details['imdbRating']
                                movies.append((title, year, rating))
                page += 1

            return movies[:20]  # Return up to 20 movies
    return "Failed to fetch movies from OMDB API."


def fetch_recommendations():
    genre = genre_combobox.get()
    recommendations = get_movie_recommendations(genre)
    result_text.delete('1.0', tk.END)
    result_text.tag_configure('header', font=('Helvetica', 14))
    if isinstance(recommendations, list):
        result_text.insert(tk.END, "Recommended movies:\n\n", 'header')
        for i, (movie_title, year, ratings) in enumerate(recommendations, start=1):
            result_text.insert(tk.END, f"{i}. {movie_title} ({year}) -{ratings}\n\n")
    else:
        result_text.insert(tk.END, recommendations)

# Create the main window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("700x600")  # Set initial size of the window
root.configure(bg='lightgray')  # Set background color

# Create a frame for widgets
frame = ttk.Frame(root, padding="10", relief='raised', borderwidth=2)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label for genre selection
genre_label = ttk.Label(frame, text="Genre:", font=("Helvetica", 12))
genre_label.grid(column=0, row=0, padx=5, pady=5)

# Dropdown menu for selecting genre
genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
          'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War',
          'Western']
genre_combobox = ttk.Combobox(frame, values=genres, state="readonly", font=("Helvetica", 10))
genre_combobox.grid(column=1, row=0, padx=5, pady=5)

# Button to fetch movie recommendations
fetch_button = ttk.Button(frame, text="Fetch Recommendations", command=fetch_recommendations)
fetch_button.grid(column=2, row=0, padx=5, pady=5)

# Text widget to display recommendations
result_text = tk.Text(root, height=30, width=70, wrap="word", font=("Helvetica", 10))
result_text.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
