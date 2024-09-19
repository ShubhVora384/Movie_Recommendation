import tkinter as tk
from tkinter import messagebox
import subprocess

class MovieRecommendationDialog:
    def __init__(self, master):
        self.master = master
        master.title("Movie Recommendation System")

        self.heading_label = tk.Label(master, text="Movie Recommendation System", font=("Helvetica", 20))
        self.heading_label.pack(pady=20)

        self.question_label = tk.Label(master, text="Which method you want to check?", font=(15))
        self.question_label.pack(pady=10)

        self.name_label = tk.Label(master, text="1. Movie recommendation based on name:")
        self.name_label.pack()

        self.name_button = tk.Button(master, text="Open", command=self.open_app)
        self.name_button.pack(pady=20)

        self.genre_label = tk.Label(master, text="2.Movie recommendation based on Genre:")
        self.genre_label.pack(pady=20)

        self.genre_button = tk.Button(master, text="Open", command=self.open_genre)
        self.genre_button.pack()

    def open_app(self):
        try:
            subprocess.Popen(["python", "app.py"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_genre(self):
        try:
            subprocess.Popen(["python", "Genre.py"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    root.geometry("600x400")
    app = MovieRecommendationDialog(root)
    root.mainloop()

if __name__ == "__main__":
    main()
