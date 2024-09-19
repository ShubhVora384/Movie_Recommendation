import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Read movies data
movies = pd.read_csv("movies.csv")

# Read ratings data
ratings = pd.read_csv("ratings.csv")


# Clean movie titles
def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title



movies["clean_title"] = movies["title"].apply(clean_title)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vectorizer.fit_transform(movies["clean_title"])


# Define search function
def search(title):
    title = clean_title(title)

    #It turns the title into a set of numbers
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    result = movies.iloc[indices].iloc[::-1]
    return result


# Define function to find similar movies
def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]

    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .10]

    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())

    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]

    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)

    similar_movies_info = rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[
        ["title", "genres"]]
    similar_movies_info_str = ""
    for idx, row in similar_movies_info.iterrows():
        similar_movies_info_str += f"Title: {row['title']}\nGenres: {row['genres']}\n\n"

    return similar_movies_info_str


# Function to handle button click
def on_ok_button_click():
    title = movie_name_entry.get()
    result = search(title)

    if not result.empty:
        movie_id = result.iloc[0]['movieId']  # extracts the value of the 'movieId' column from the first row of the DataFrame result
        title_str = "\tTitle \t\tGenres\t\tclean_title\n\n"
        result_str = ""

        # iterates over each row in the DataFrame result, providing both the index (idx) and the contents of each row (row)
        for idx, row in result.iterrows():
            result_str += f"{row['title']},\t\t {row['genres']},\t\t {row['clean_title']}\n\n"

        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, title_str)
        result_text.insert(tk.END, result_str)
        result_text.config(state="disabled")

        similar_movies = find_similar_movies(movie_id)
        if similar_movies:
            messagebox.showinfo("Similar Movies", str(similar_movies))
    else:
        messagebox.showinfo("Movie Search Result", "No movies found.")


# Create Tkinter window
root = tk.Tk()
root.title("Movie Recommendation System")

# Create entry widget for movie name input
movie_name_label = tk.Label(root, text="Enter Movie Name:")
movie_name_label.pack()  #organizes widgets in horizontal and vertical boxes that are limited to left, right, top, bottom positions.
movie_name_entry = tk.Entry(root)
movie_name_entry.pack()

# Create OK button
ok_button = tk.Button(root, text="OK", command=on_ok_button_click)
ok_button.pack()

result_text = tk.Text(root, font=("Arial", 12), height=20, wrap="word")  #breaks the section of a particular text to fit into multiple sections of lines where possible.
result_text.pack()

root.mainloop()
