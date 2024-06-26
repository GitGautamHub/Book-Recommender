# Book Recommender

Book Recommender is a Streamlit web application that helps users find the best book in a specific genre based on their query. The application fetches books from the Google Books API, narrows down the top 10 books by ratings and reviews, and uses a Hugging Face transformer model to find the best match book.

![Book Image](book.jpg)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/GitGautamHub/book-recommender.git
   cd Book-Recommender
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the application:
   ```bash
   streamlit run "BookRecommender.py"

## Usage
- Enter a genre in the input field.
- Enter your specific query.
- Click on the "Find Books" button.
- The application will display the top 100 books, narrow down to the top 10, and finally show the best match book based on your query.