import tkinter as tk
import pandas as pd
import csv
from tkinter import ttk
import random

# The link below is the link that one has to download in order for the program to run properly.
# https://uillinoisedu-my.sharepoint.com/:u:/g/personal/millard5_illinois_edu/ESsTEfkTbZFDvJvZ4L86lRsBHhab-1UnjjWuuBS70qHr5g?e=bkMT0D
class Book:


	def __init__ (self, title, author, isbn, description, series, date_published, pages, genre):
		self.title = title
		self.author = author
		self.isbn = isbn
		self.description = description
		if series:
			self.series = series
		else:
			self.series = False
		self.date_published = date_published
		self.pages = pages
		self.genre = genre


	def __str__(self):
	
		if self.series:
			display = self.title + " by " + self.author + "\n\t" + "Description: " + self.description + "\n\t" + "ISBN: " + self.isbn + "\n\t" + "Series: " + self.series
		else:
			display = self.title + " by " + self.author + "\n\t" + "Description: " + self.description + "\n\t" + "ISBN: " + self.isbn

		return display

def create_library(file_path):
	fileObj = open(file_path, "r", encoding="utf-8")
	reader = csv.reader(fileObj, delimiter=',', quotechar='"')
	header = next(reader)

	library = []

	for line in reader:
		if len(line[3]) > 0:
			series = line[3].strip("()")
		else:
			series = None
		if line[16].isdigit() == True:
			date = int(line[16])
		else:
			strip_bc = line[16].strip("-")
			if strip_bc.isdigit() == True:
				date = int(line[16])
			elif len(line[16]) == 0:
				date = "Unknown"
			else:
				date_split = line[16].split(" ")
				date = int(date_split[-1])

		genres = line[19].split(",")
		genre_cleaned = []
		for genre_with_num in genres:
			genre_list = genre_with_num.split(" ")
			genre = "".join(genre_list[:-1])
			genre_cleaned.append(genre)
		if line[15].isdigit():
			pages = int(line[15])
		else:
			pages = "Unknown"



		book = Book(line[1], line[5], line[20], line[30], series, date, pages, genre_cleaned)
		library.append(book)

	return library


class Display:


	def __init__ (self, library):
		self.library = library
		self.recommendations = library
		self.root = tk.Tk()
		self.init_window()      


	def init_window(self):
		self.screen_size = (500, 500) 
		self.root.minsize(self.screen_size[1], self.screen_size[0])

		self.root.title("Book Recommendations Just For You!")

		self.frame = tk.Frame(self.root)
		self.frame.grid()

		self.title_label = tk.Label(self.frame, text="Book Recommendations Just For You!")
		self.title_label.grid(row=0)

		self.series_question_label = tk.Label(self.frame, text="Would you like to read a book series?")
		self.series_question_label.grid(row=2)
		self.series_answer = ttk.Combobox(self.frame, state="readonly", values=["yes", "no"])
		self.series_answer.grid(row=3)

		self.published_date_label = tk.Label(self.frame, text="How recent would you like the book to have been published?")       # The answers are not lining up where I want them to
		self.published_date_label.grid(row=4)
		self.published_answer = ttk.Combobox(self.frame, state="readonly", values=["1960s and earlier", "1970s-1990s", "2000s"])
		self.published_answer.grid(row=5)

		self.length_question_label = tk.Label(self.frame, text="How long of a book would you like to read?")
		self.length_question_label.grid(row=6)
		self.length_answer = ttk.Combobox(self.frame, state="readonly", values=["0-300", "300-600", "600+"])
		self.length_answer.grid(row=7)

		self.genre_question_label = tk.Label(self.frame, text="What is your favorite genre to read?")
		self.genre_question_label.grid(row=8)
		self.genre_answer = ttk.Combobox(self.frame, state="readonly", values=["Academic", "Adult", "Adventure", "Alcohol", "Animals", "Art", "Asian Literature", "Biography", "Biology", "Business", "Childrens", "Christian", "Classics", "Comics", "Computer Science", "Cultural", "Economics", "Environment", "Erotica", "European Literature", "Fairy Tales", "Fantasy", "Folk", "Food and Drink", "Games", "Health", "Historical", "Holiday", "Horror", "Literature", "Media", "Mystery", "Mythology", "Nonfiction", "Novels", "Occult", "Paranormal", "Philosophy", "Plays", "Politics", "Psychology", "Religion", "Romance", "Science Fiction", "Science", "Self-Help", "Sequential Art", "Sociology", "Spirituality", "Sports", "Suspense", "Thriller", "Travel", "War", "Womens", "Writing", "Young Adult"])
		self.genre_answer.grid(row=9)

		self.go_button = tk.Button(self.frame, text="Go", command=self.generate_book)   
		self.go_button.grid(row=10)

		self.new_book_button = tk.Button(self.frame, text="Choose New Book", command=self.another_book)
		self.new_book_button.grid(row=11)

		self.quit_button = tk.Button(self.frame, text="Quit", command=self.root.destroy)
		self.quit_button.grid(row=12)

		self.display_label = tk.Label(self.frame, text="\n", wraplength=500)
		self.display_label.grid(row=13)


	def generate_book(self):
		series = self.series_answer.get()
		published = self.published_answer.get()
		length = self.length_answer.get()
		genre = self.genre_answer.get()

		series_recommendations = []
		if series == "yes":
			for book in self.library:
				if book.series != None:
					series_recommendations.append(book)
		elif series == "no":
			for book in self.library:
				if not book.series:
					series_recommendations.append(book)
		else:
			series_recommendations = self.library


		published_recommendations = []
		if published == "1960s and earlier":
			for book in series_recommendations:
				if book.date_published != "Unknown":
					if book.date_published <= 1969:
						published_recommendations.append(book)
		elif published == "1970s-1990s":
			for book in series_recommendations:
				if book.date_published != "Unknown":
					if book.date_published <= 1999 and book.date_published >= 1970:
						published_recommendations.append(book)
		elif published == "2000s":
			for book in series_recommendations:
				if book.date_published != "Unknown":
					if book.date_published >= 2000:
						published_recommendations.append(book) 
		else:
			published_recommendations = series_recommendations


		length_recommendations = []
		if length == "0-300":
			for book in published_recommendations:
				if book.pages != "Unknown":
					if book.pages >= 0 and book.pages <= 300:
						length_recommendations.append(book)
		elif length == "300-600":
			for book in published_recommendations:
				if book.pages != "Unknown":
					if book.pages >= 300 and book.pages <= 600:
						length_recommendations.append(book)
		elif length == "600+":
			for book in published_recommendations:
				if book.pages != "Unknown":
					if book.pages >= 600:
						length_recommendations.append(book)
		else:
			length_recommendations = published_recommendations


		final_recommendations = []
		if genre == "Academic":
			for book in length_recommendations:
				for book_genre in book.genre:
					if "Academic" in book_genre:
						final_recommendations.append(book)
		elif genre == "Adult":
			for book in length_recommendations:
				for book_genre in book.genre:
					if "Adult" in book_genre:
						final_recommendations.append(book)
		
		# finish all other genres
		else:
			final_recommendations = length_recommendations

		self.recommendations = final_recommendations
		if len(self.recommendations) < 1:
			self.display_label.config(text=str("There are no books that fit this description."))
		else:
			chosen_book = random.choice(self.recommendations)
			self.display_label.config(text=str(chosen_book))

	def another_book(self):
		if len(self.recommendations) < 1:
			self.display_label.config(text=str("There are no books that fit this description."))
		else:
			chosen_book = random.choice(self.recommendations)
			self.display_label.config(text=str(chosen_book))





def main():
	file_path = "goodreads_books.csv"
	'''
	title = "A Court of Thorns and Roses"
	author = "Sarah J. Maas"
	isbn = "1234"
	description = "so cool"
	series = "ACOTAR (1)"
	date_published = "June 1 2024"
	pages = "655"
	genre = "fantasy"

	book = Book(title, author, isbn, description, series, date_published, pages, genre)
	print(book)
	'''
	library = create_library(file_path)
	window = Display(library)
	window.root.mainloop()
	

if __name__ == "__main__":
    main()
