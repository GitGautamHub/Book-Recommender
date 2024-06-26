import streamlit as st
import requests
import urllib.parse
import time
from transformers import pipeline

# Google Books API key
google_books_api_key = "AIzaSyAf-GF13cw6ZSObioHfUvbOo8MLgrW1yy4"



# To get a list of books based on genre from Google Books API
def fetch_books_by_genre(genre, progress_bar):
    encoded_genre = urllib.parse.quote(genre)
    books = []

    for start_index in range(0, 120, 40):
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=subject:{encoded_genre}&startIndex={start_index}&maxResults=40&orderBy=relevance&key={google_books_api_key}"
        )
        if response.status_code == 200:
            books_data = response.json()
            books.extend([
                {
                    "title": item["volumeInfo"].get("title", "N/A"),
                    "author": ", ".join(item["volumeInfo"].get("authors", ["N/A"])),
                    "averageRating": item["volumeInfo"].get("averageRating", 0),
                    "ratingsCount": item["volumeInfo"].get("ratingsCount", 0)
                }
                for item in books_data.get("items", [])
            ])
            progress_bar.progress((start_index + 40) / 120)
        else:
            st.error(f"Failed to fetch books: {response.status_code}")
            return []

        if len(books) >= 100:
            break

    return books[:100]



# To display books
def display_books(books):
    num_cols = 3
    cols = st.columns(num_cols)

    for i, book in enumerate(books):
        col = cols[i % num_cols]
        with col:
            st.markdown(f"<h3 style='color:#4B8BBE;'>{i + 1}. {book['title']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#306998;'>by {book['author']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>{rating_to_emoji(book['averageRating'])} ({book['ratingsCount']} reviews)</p>", unsafe_allow_html=True)
            st.markdown("---")



# To convert rating to emojis
def rating_to_emoji(rating):
    if rating is None or rating == 0:
        return "No rating"
    rating = int(round(rating))
    return "⭐" * rating + "✰" * (5 - rating)



# To find the best match book using Hugging Face transformer
def find_best_match_book(books, query, progress_bar):
    nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    book_descriptions = [f"{book['title']} by {book['author']}" for book in books]
    results = nlp(query, book_descriptions)
    best_match_index = results['labels'].index(
        max(results['labels'], key=lambda label: results['scores'][results['labels'].index(label)]))
    best_match = books[best_match_index]
    progress_bar.progress(1.0)
    return best_match



# Headiing
st.markdown("<h1 style='text-align:center; color: white;'>Book Recommender</h1>", unsafe_allow_html=True)

# User Input
genre = st.text_input("Enter a genre:")
specific_query = st.text_input("Enter your specific query:")

if st.button("Find Books"):
    progress_bar = st.progress(0)


    # Getting top books based on genre
    books = fetch_books_by_genre(genre, progress_bar)


    if books:

        # Sorting books by ratingsCount first, then by averageRating
        books = sorted(books, key=lambda x: (x['ratingsCount'], x['averageRating']), reverse=True)


        st.success("Fetched top 100 books.")
        progress_bar.progress(0.33)

        st.markdown("<h2 style='color:Goldenrod;'>Top 100 Books:</h2>", unsafe_allow_html=True)
        display_books(books)

        # To find top 10 books from the list
        top_10_books = books[:10]
        st.success("Narrowed down to top 10 books.")
        progress_bar.progress(0.66)

        st.markdown(f"<h2 style='color:Goldenrod;'>Top 10 Books in {genre}:</h2>", unsafe_allow_html=True)
        display_books(top_10_books)

        # Finding the specific book based on user query using Hugging Face transformer
        best_match_book = find_best_match_book(top_10_books, specific_query, progress_bar)
        st.success("Found the best match book.")

        st.markdown("<h2 style='color:#4B8BBE;'>Best Match Book Found:</h2>", unsafe_allow_html=True)
        if best_match_book:
            st.markdown(
                f"<div style='background-color:#f0f8ff ; padding:10px; border-radius:10 px;'>"
                f"<h3 style='color:#4B8BBE;'>{best_match_book['title']}</h3>"
                f"<p style='color:#306998;'>by {best_match_book['author']}</p>"
                f"<p style='color:black;'>{rating_to_emoji(best_match_book['averageRating'])} ({best_match_book['ratingsCount']} reviews)</p>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown('---')
        else:
            st.markdown(
                "<div style='background-color:#f0f8ff; padding:2px; border-radius:1px;'>No match found</div>",
                unsafe_allow_html=True)
            st.markdown('---')
    else:
        st.write("No books found. Please check the genre or try again later.")

    # Concluding with a thank you message and balloons animation
    st.markdown(
        "<h3 style='background-color:yellow; padding:2px; border-radius:1px;color:black'>Thank you for using the Book Recommender!</h3>",
        unsafe_allow_html=True)
    time.sleep(3)
    st.balloons()
