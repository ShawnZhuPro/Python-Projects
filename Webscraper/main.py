# Import necessary modules
from urllib.request import urlopen  # For opening URLs
from urllib.error import URLError  # For handling URL errors
from pathlib import Path  # For working with file paths
from webscraper_utilities import get_image_urls  # Custom function to get image URLs
from shutil import make_archive, rmtree, move  # For working with directories and archives

# Define a function to download images
def download_images(image_urls, directory_name):
    # Create a temporary directory path for storing downloaded images
    temp_directory_path = image_path / directory_name
    temp_directory_path.mkdir()
    print(f"New directory created: {temp_directory_path}")
    
    # Iterate through image URLs and save them to the specified directory
    for image_url in image_urls:
        directory_path = temp_directory_path / Path(image_url).name
        save_file(image_url, directory_name)

# Define a function to create a ZIP archive of a directory
def zip_directory(directory_name):
    # Define the path to the ZIP archive directory
    zip_directory_path = Path("zip-archives") / directory_name
    # Define the path to the source directory to be zipped
    directory_path = Path("images") / directory_name
    
    # Create a ZIP archive of the source directory
    make_archive(zip_directory_path, "zip", directory_path)
    
    # Print a message indicating the ZIP archive creation
    print(f"{directory_name}.zip created!")
    print(f"You can find it at: {zip_directory_path}.zip")

# Define a function to remove a directory
def remove_directory(directory_name):
    # Define the path to the directory to be removed
    directory_path = image_path / Path(directory_name).name
    
    try: 
        # Try to remove the directory and its contents
        rmtree(directory_path)
    except FileNotFoundError:
        # Handle the case where the directory does not exist
        print(f"{directory_name} does not exist!")
        return
    
    print(f"{directory_name} removed!")

# Define a function to rename a directory
def rename_directory(original_directory_name, new_directory_name):
    # Define the paths to the original and new directories
    original_directory_path = image_path / Path(original_directory_name).name
    new_directory_path = image_path / Path(new_directory_name).name
    
    try:
        # Try to rename the directory
        move(original_directory_path, new_directory_path)
    except FileNotFoundError:
        # Handle the case where the original directory does not exist
        print(f"{original_directory_name} does not exist!")
        return
    
    print(f"{new_directory_name} directory created!")

# Define a function to create a new directory
def create_directory(directory_name):
    # Extract a safe directory name from the input to prevent path traversal attacks
    safe_directory_name = Path(directory_name).name
    # Define the path to the new directory
    directory_path = image_path / safe_directory_name

    # Create the new directory
    directory_path.mkdir()
    print(f"New directory created: {directory_path}")

# Define a function to save a file from a URL
def save_file(file_url, user_directory):
    # Extract the filename from the URL
    filename = Path(file_url).name
    # Define the full path to save the file
    file_path = image_path / user_directory / filename

    try:
        # Try to fetch the file data from the URL
        with urlopen(file_url) as response:
            raw_file_data = response.read()
    except URLError:
        # Handle URL errors
        print(f"Error fetching data at {file_url}.")
        return

    # Save the file to the specified path
    with open(file_path, mode="wb") as binary_file:
        binary_file.write(raw_file_data)
        print(f"Your file will be stored at {file_path}")

# Define a function to view files in a directory
def view_files(directory_name):
    # Define the local path to the directory you want to view
    directory_path = image_path / directory_name
    for file_path in directory_path.iterdir():
        print(file_path)

# Define a function to list directories in the base image directory
def list_directories():
    for directory in image_path.iterdir():
        print(directory.stem)

# Define user options and constants
options = """
    1.) Scrape images from a URL 
    2.) List directories 
    3.) View files in a directory
    4.) Create zip archive
    5.) Remove directory 
    6.) Rename directory
    7.) Exit
"""

SCRAPE = 1
LIST = 2
VIEW = 3
ZIP = 4
REMOVE = 5
RENAME = 6
EXIT = 7

# Define a username and the base image directory
image_path = Path("C:/Users/shawn/Documents/images")

# Main loop for user interaction
while True:
    user_choice = int(input(options))

    if user_choice == SCRAPE:
        url = input("Give me a URL to scrape: ")
        image_urls = get_image_urls(url)
        directory_name = input("Enter a directory name to store the images in: ")
        download_images(image_urls, directory_name)
    elif user_choice == LIST:
        list_directories()
    elif user_choice == VIEW:
        directory_name = input("Enter the directory name to view files from: ")
        view_files(directory_name)
    elif user_choice == ZIP:
        directory_name = input("Enter the directory to zip: ")
        zip_directory(directory_name)
    elif user_choice == REMOVE:
        directory_name = input("Enter the directory name to remove: ")
        remove_directory(directory_name)
    elif user_choice == RENAME:
        original_directory_name = input("Enter the directory name you want to rename: ")
        new_directory_name = input("Enter the new name: ")
        rename_directory(original_directory_name, new_directory_name)
    elif user_choice == EXIT:
        print("Goodbye!")
        break
