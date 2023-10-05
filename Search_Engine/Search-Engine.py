"""
###################################################################################

Harvard Art Museum API
- Get API Key: https://docs.google.com/forms/d/1Fe1H4nOhFkrLpaeBpLAnSrIMYvcAxnYWm0IU9a6IkFA/viewform
- API Docs: https://github.com/harvardartmuseums/api-docs
- Base URL: https://api.harvardartmuseums.org
- Image route: /image  
    - Docs: https://github.com/harvardartmuseums/api-docs/blob/master/sections/image.md
Example request: https://api.harvardartmuseums.org/image?apikey=API_KEY&q=cat&size=3

###################################################################################

Gutendex Book API
- Docs: https://gutendex.com/
Example Request: https://gutendex.com/books/?search=dickens

###################################################################################

News API
- Register: https://newsapi.org/register
- Get Started: https://newsapi.org/docs/get-started
- Base API URL: https://newsapi.org/v2
- Search route: /everything
Example request: https://newsapi.org/v2/everything?q=bitcoin&apiKey=API_KEY

###################################################################################
"""
from urllib.request import urlopen
from urllib.parse import urlencode
from json import loads, load, dump, dumps

# Function to retrieve artworks from the Harvard Art Museum API
def get_artworks(search_term, max_results):
    # Base API URL, endpoint, and API key for artworks
    BASE_API_URL = "https://api.harvardartmuseums.org"
    endpoint = "/image"
    API_KEY = "f83b19c6-9ac2-4e90-a2fa-f49e17f4f257"
    
    # Query parameters for the API request
    query_params = {
        "apikey": API_KEY,
        "q": search_term,
        "size": max_results,
    }
    # Encodes the query params into a URL that can be read
    encoded_query_params = urlencode(query_params)
    
    # Final API request URL
    request_url = f"{BASE_API_URL}{endpoint}?{encoded_query_params}"

    # Sends the API request and parses the response data
    with urlopen(request_url) as response:
        response_data = loads(response.read())

    # Returns the "records" JSON dict from the API
    return response_data["records"]

# Function to retrieve articles from the News API
def get_articles(search_term, max_results):
    # Base API URL, endpoint, and API key for articles
    BASE_API_URL = "https://newsapi.org/v2"
    endpoint = "/everything"
    API_KEY = "91cf9a43020d4980abf16073fc1ff0d3"
    
    # Parameters for the API request
    query_params = {
        "apikey": API_KEY,
        "q": search_term,
        "pageSize": max_results,
    }
    # Encodes the query params into a URL that can be read
    encoded_query_params = urlencode(query_params)
    
    # Final API request URL
    request_url = f"{BASE_API_URL}{endpoint}?{encoded_query_params}"

    # Sends the API request and parses the response data
    with urlopen(request_url) as response:
        response_data = loads(response.read())

    # Returns the "articles" JSON dict from the API
    return response_data["articles"]

# Function to retrieve books from the Book API
def get_books(search_term, max_results):
    # Base API URL and endpoint for books
    BASE_API_URL = "https://gutendex.com"
    endpoint = "/books"
    
    # Parameters for the API request
    query_params = {
        "search": search_term,
    }
    encoded_query_params = urlencode(query_params)
    request_url = f"{BASE_API_URL}{endpoint}?{encoded_query_params}"

    # Sends the API request and parses the response data
    with urlopen(request_url) as response:
        books_json = loads(response.read())

    # Returns the "results" JSON dict from the API, and limits the number of elements 
    # to be shown by the list to "max_results" from the user's input
    return books_json["results"][:max_results]

# Function to display articles
def display_articles(articles):
    # Displays article results
    print("\n************ Article results ************\n")
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Author: {article['author']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
    print("\n**********************************************\n")

# Function to display books
def display_books(books):
    # Displays book results
    print("\n************ Book results ************\n")
    for book in books:
        print(f"\nTitle: {book['title']}")
        print(f"Author(s): {book['authors']}")
        print(f"Subjects: {book['subjects']}")
    print("\n**********************************************\n")

# Function to display artworks
def display_artworks(artworks):
    # Displays artwork results
    print("\n********** Artwork results **********\n")
    for artwork in artworks:
        print(f"\nDescription: {artwork['description']}")
        print(f"URL: {artwork['baseimageurl']}")
    print("\n*********************************************\n")

# Function to save search results to a JSON file
def save_search_results(search_term, artworks, books, articles, username):
    # Loads existing search results from the JSON file
    search_results = load_search_results()

    # Checks if the username is in the search_results dictionary
    if search_results.get(username) is None:
        # Adds an empty dict to the username key
        search_results[username] = {}

    # Adds the search_term key to the username dict
    search_results[username][search_term] = {
        "artworks": artworks,
        "books": books,
        "articles": articles,
    }

    # Opens the json in write text mode, which replaces old data with new
    with open("search-results.json", mode="wt") as json_file:
        # Replaces old data in the search_results dict with new data
        dump(search_results, json_file, indent=4)

# Function to load search results from a JSON file
def load_search_results():
    # Opens the json file in read mode
    with open("search-results.json", mode="rt") as json_file:
        # Loads the JSON into the search_results dict
        search_results = load(json_file)

    # Returns the JSON dict with search results data in a variable to use
    return search_results

# Function to view all saved search results
def view_search_results():
    search_results = load_search_results()
    # Displays the search results for all users
    print(dumps(search_results, indent=4))

# Function to display the welcome banner
def display_welcome_banner():
    welcome_banner = """
            Welcome to your personal Search Engine!
        This app lets you provide a search term and then
        returns book/art/news results based on that
        search term.
        You can save selections that you enjoy to browse later!
    """
    print(welcome_banner)
    
# Options users can choose from
options = """
    1.) Search 2.) Save Search Results 3.) View Saved Search Results 4.) Exit
"""

# Constants for user options
SEARCH, SAVE, VIEW, EXIT = range(1,5)

# Default values
search_term = ""
artworks = []
books = []
articles = []

# Gets the username from the user
username = input("Enter username: ")

# Displays the welcome banner
display_welcome_banner()

# Main loop for user interaction
while True:
    user_choice = int(input(options))

    if user_choice == SEARCH:
        # Gets user input for search term and maximum results
        search_term = input("Enter your search term: ")
        max_results = int(input("How many results do you want? "))

        # Retrieves data from APIs based on the search term
        artworks = get_artworks(search_term, max_results)
        books = get_books(search_term, max_results)
        articles = get_articles(search_term, max_results)

        # Displays the search results
        display_artworks(artworks)
        display_books(books)
        display_articles(articles)

    elif user_choice == SAVE:
        # Saves the current search results for the user
        save_search_results(search_term, artworks, books, articles, username)

    elif user_choice == VIEW:
        # Views all saved search results for all users
        view_search_results()

    elif user_choice == EXIT:
        # Exits the program
        break
