# Design Document for Book Recommender

## Objective
The primary objective is to create a user-friendly application that helps users find the best book in a specific genre based on their query.

## Approach
1. **Fetching Books**:
   - Use Google Books API to fetch a list of books based on the genre.
   - Fetch up to 120 books in batches of 40 to ensure diversity and relevance.
   
2. **Filtering and Sorting**:
   - Filter and sort the fetched books based on the number of ratings and average ratings.
   - Select the top 100 books and then narrow down to the top 10 books.

3. **Finding the Best Match**:
   - Use Hugging Face's `zero-shot-classification` pipeline to determine the best match book among the top 10 based on a user query.
   
4. **User Interface**:
   - Implement a Streamlit application for the user interface.
   - Display books in a grid layout and use a progress bar to indicate the progress of fetching, filtering, and finding the best match.
   - Use emojis to represent book ratings for better visual appeal.

## Reason for Approach
- **Streamlit**: Chosen for its simplicity in creating interactive web applications with Python.
- **Google Books API**: Provides a comprehensive database of books, allowing for diverse and relevant book recommendations.
- **Hugging Face Transformers**: Utilized for their state-of-the-art natural language processing capabilities to find the best match based on user queries.
- **Progress Bar and Emojis**: Enhances user experience by providing visual feedback and making the interface more engaging.
