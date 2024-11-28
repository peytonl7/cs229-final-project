import os
import requests
import csv
from bs4 import BeautifulSoup

# Set your Genius API credentials here
GENIUS_ACCESS_TOKEN = "3IrbfUKApru5Ps6aHT3jQR9yGh0d6xSweOE52ogogZJb331vmRbs62Z7yKnDB9-e"

# Base URL for the Genius API
GENIUS_API_URL = "https://api.genius.com"

# Function to search for a song on Genius and get its ID
def search_song(artist, song_title):
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    search_url = f"{GENIUS_API_URL}/search"
    query = f"{song_title} {artist}"
    params = {"q": query}
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Error: Failed to fetch song data for {artist} - {song_title}")

    hits = response.json().get("response", {}).get("hits", [])
    if not hits:
        raise Exception(f"Error: No results found for {artist} - {song_title}")
    
    song_id = hits[0]["result"]["id"]
    return song_id

# Function to get song lyrics URL by song ID
def get_song_lyrics_url(song_id):
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    song_url = f"{GENIUS_API_URL}/songs/{song_id}"
    response = requests.get(song_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error: Failed to fetch song data for song ID {song_id}")
    
    song_data = response.json().get("response", {}).get("song", {})
    return song_data.get("url")

# Function to fetch the raw lyrics from the Genius lyrics page
def fetch_raw_lyrics(lyrics_url):
    response = requests.get(lyrics_url)
    
    if response.status_code != 200:
        raise Exception(f"Error: Genius lyrics page not found at {lyrics_url}")
    
    # Parse the HTML page to extract the lyrics
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Lyrics are typically inside <div> with a data-lyrics-container attribute
    lyrics_div = soup.find_all('div', {'data-lyrics-container': 'true'})
    
    if not lyrics_div:
        raise Exception(f"Error: Could not find lyrics on the page {lyrics_url}")
    
    # Concatenate the lyrics without line breaks between lines
    lyrics = ''.join([div.get_text(separator=' / ') for div in lyrics_div])
    
    return lyrics.strip()


# Function to fetch metadata from Genius song page
def fetch_song_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    metadata = {
        'Producer': 'N/A',
        'Writers': 'N/A',
        'Release Date': 'N/A',
        'Tags': 'N/A'
    }
    # Extract metadata elements
    metadata['Producer'] = soup.select_one('.SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Producer")) a').get_text(strip=True) if soup.select_one('.SongInfo__Label-nekw6x-4:-soup-contains("Producer")') else 'N/A'
    metadata['Writers'] = ', '.join([writer.get_text(strip=True) for writer in soup.select('.SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Writers")) a')])
    metadata['Release Date'] = soup.select_one('.SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Released on"))').get_text(strip=True).replace("Released on", "").strip() if soup.select_one('.SongInfo__Label-nekw6x-4:-soup-contains("Released on")') else 'N/A'
    
    
    tags = []
    tags_container = soup.find('div', class_='SongTags__Container-xixwg3-1')
    if tags_container:
        tag_elements = tags_container.find_all('a', class_='SongTags__Tag-xixwg3-2')
        tags = [tag.get_text(strip=True) for tag in tag_elements]
    metadata['Tags'] = tags

    return metadata

# Main function to update the CSV with lyrics and metadata
def update_csv_with_lyrics_metadata(input_csv, output_csv):
    with open(input_csv, 'r', encoding='utf-8') as csv_file, open(output_csv, 'w', encoding='utf-8', newline='') as output_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames + ['lyrics', 'metadata']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            artist = row['performer']
            song_title = row['song']
            try:
                song_id = search_song(artist, song_title)
                lyrics_url = get_song_lyrics_url(song_id)
                lyrics = fetch_raw_lyrics(lyrics_url)
                metadata = fetch_song_metadata(lyrics_url)
                row['lyrics'] = lyrics
                row['metadata'] = metadata  # Storing metadata as a dictionary

            except Exception as e:
                print(f"Error fetching data for {artist} - {song_title}: {e}")
                row['lyrics'] = 'Error'
                row['metadata'] = 'Error'

            writer.writerow(row)
        print(f"Updated CSV saved as {output_csv}")

# Usage
input_csv = '../../data/remaining-processed-hot-100.csv'
output_csv = '../../data/processed-hot-100-with-lyrics-metadata-8.csv'
update_csv_with_lyrics_metadata(input_csv, output_csv)