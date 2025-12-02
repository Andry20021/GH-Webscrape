import numpy as np
import requests
from bs4 import BeautifulSoup

# Fetching page
url = 'https://guitarhero.fandom.com/wiki/Guitar_Hero_II/Setlist'
page = requests.get(url, verify=True)
soup = BeautifulSoup(page.text, 'lxml')

# Selecting tables
tables = soup.select('table.ghtable.sortable')
base_game_table = tables[0]
bonus_song_table = tables[1]


# Function to fetch data from any table
def fetch_data_from_table(table):
    artist_names = []
    song_names = []
    header = table.find('tr').find_all('th')

    # Find column indices for artist and song title
    artist_column_index = None
    song_names_column_index = None
    for i, th in enumerate(header):
        if 'Artist'.lower() in th.text.strip().lower():
            artist_column_index = i
        if 'Song title'.lower() in th.text.strip().lower():
            song_names_column_index = i

    # If both indices are found, collect data
    if artist_column_index is not None and song_names_column_index is not None:
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if columns:
                artist_name = columns[artist_column_index].text.strip()
                song_title = columns[song_names_column_index].text.strip()
                artist_names.append(artist_name)
                song_names.append(song_title)
    else:
        print("Artist or Song title not found")
    return artist_names, song_names


# Combine artist and song names
def combine_data(artist_names, song_names):
    if artist_names and song_names:
        return np.array(list(zip(artist_names, song_names)), dtype=object)
    else:
        return np.array([])


# Output combined data to a text file
def output_to_file(table, filename='output.txt'):
    with open(filename, 'w') as file:
        for row in table:
            line = ', '.join(row)
            file.write(line + '\n')
    print(f"Data written to {filename}")


# Fetch data from both tables
base_game_artists, base_game_songs = fetch_data_from_table(base_game_table)
bonus_artists, bonus_songs = fetch_data_from_table(bonus_song_table)

# Combine all artist and song data
all_artists = base_game_artists + bonus_artists
all_songs = base_game_songs + bonus_songs

# Create combined data array
combined_data = combine_data(all_artists, all_songs)

# Output combined data to file
output_to_file(combined_data)
