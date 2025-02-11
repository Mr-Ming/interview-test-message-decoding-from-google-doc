# Make sure to "pip3 install BeautifulSoup requests".
from bs4 import BeautifulSoup
import requests

def fetch_external_data(url):
    # Fetch the data from url.
    response = requests.get(url)

    # If its a success.
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup.
        raw_data = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the document content.
        parsed_data = raw_data.find('body').get_text(separator='\n', strip=True)

        # Clean and create a 2d array map.        
        coordinate_map = clean_parsed_data(parsed_data)
        max_cols, array_map = create_2d_array_map(coordinate_map)

        for i in range(len(array_map)):
            for j in range(len(array_map[i])):
                print(array_map[i][j], end="")

                # Every 6 items we perform a line break as that is the terminating point.
                if (j == max_cols):
                    print("")

    else:
        print(f"Unable to fetch data with status code: {response.status_code}")

# Clean the parsed data.
def clean_parsed_data(data):
    data_as_array = data.split('\n')

    # Strip out all words so we only have coordinate. Longest word is "Character" (length of 9)
    coordinate_map = [row for row in data_as_array if len(row) < 9]

    return coordinate_map
    
# Create the 2d Array. (2D is best since we won't need to do sorting).
def create_2d_array_map(data):
    max_rows = 0
    max_cols = 0

    # Find max rows and cols and initialize it.
    for i in range(0, len(data), 3):
        if max_rows < int(data[i]):
            max_rows = int(data[i])
        
        if max_cols < int(data[i+2]):
            max_cols = int(data[i+2])

    array_map = [[" "] * (max_cols+1) for _ in range(max_rows+1)]

    # Create a 2D Array map.
    for i in range(0, len(data), 3):
        # Get the slice of 3 items
        coordinate_x = int(data[i])
        coordinate_data = data[i+1]
        coordinate_y = int(data[i+2])

        array_map[coordinate_x][coordinate_y] = coordinate_data
    
    return max_cols, array_map
        
# Print the message from url.
def print_message_from_url(url):
    data = fetch_external_data(url)


## Main Process.
url = "https://docs.google.com/document/d/e/2PACX-1vTWqR8Ta9hDLj0vUXr3DyO470m1QMFbKdOGoTby36zjrZNpmSxAMzyPgW8NIFHBIAAeFjLwgWdHg2I8/pub"
print_message_from_url(url)