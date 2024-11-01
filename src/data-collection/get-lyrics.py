import os
import requests
from bs4 import BeautifulSoup

# Set your Genius API credentials here
GENIUS_ACCESS_TOKEN = "ACCESS_TOKEN"

# Base URL for the Genius API
GENIUS_API_URL = "https://api.genius.com"

# Function to search for a song on Genius and get its ID
def search_song(artist, song_title):
    headers = {
        "Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"
    }
    
    search_url = f"{GENIUS_API_URL}/search"
    query = f"{song_title} {artist}"
    
    params = {"q": query}
    
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error: Failed to fetch song data for {artist} - {song_title}")
    
    response_data = response.json()
    hits = response_data["response"]["hits"]
    
    if len(hits) == 0:
        raise Exception(f"Error: No results found for {artist} - {song_title}")
    
    song_id = hits[0]["result"]["id"]
    return song_id


# Function to get song lyrics URL by song ID
def get_song_lyrics_url(song_id):
    headers = {
        "Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"
    }
    
    song_url = f"{GENIUS_API_URL}/songs/{song_id}"
    response = requests.get(song_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Error: Failed to fetch lyrics for song ID {song_id}")
    
    song_data = response.json()["response"]["song"]
    lyrics_url = song_data["url"]
    return lyrics_url


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
    
    # Combine all parts of the lyrics
    lyrics = '\n'.join([div.get_text(separator='\n') for div in lyrics_div])
    
    return lyrics.strip()


# Function to get and save song lyrics
def save_lyrics(artist, song_title):
    try:
        # Search for the song to get its Genius ID
        song_id = search_song(artist, song_title)
        
        # Get the song's Genius lyrics URL
        lyrics_url = get_song_lyrics_url(song_id)
        
        # Fetch the raw lyrics from the lyrics page
        lyrics = fetch_raw_lyrics(lyrics_url)

        # Move to the data/song-lyrics directory
        directory = 'data/song-lyrics'
        os.makedirs(directory, exist_ok=True)
        
        # Save the lyrics in a text file within the specified directory
        file_name = f"{artist}-{song_title}.txt".replace(' ', '_').lower()
        file_path = os.path.join(directory, file_name)
        
        # Save the lyrics in a text file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(lyrics)
        
        print(f"Lyrics saved to {file_name}")
    
    except Exception as e:
        # Log the error into error.txt
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.write(f"{artist} - {song_title}: {str(e)}\n")
        print(f"Error: {e}")


if __name__ == '__main__':
    songs = [
        ("Sabrina Carpenter", "emails i can't send"),
        ("Taylor Swift", "tis' the damn season"),
        ("Taylor Swift", "Bad Blood"),
        ("Olivia Rodrigo", "drivers license"),
        ("Ed Sheeran", "Shape of You"),
        ("Adele", "Hello"),
        ("The Weeknd", "Blinding Lights"),
        ("Billie Eilish", "bad guy"),
        ("Dua Lipa", "Levitating"),
        ("Harry Styles", "Watermelon Sugar"),
        ("Drake", "God's Plan"),
        ("Bruno Mars", "Uptown Funk"),
        ("Doja Cat", "Say So"),
        ("Lorde", "Royals"),
        ("Beyoncé", "Halo"),
        ("Ariana Grande", "thank u, next"),
        ("Sam Smith", "Stay With Me"),
        ("Katy Perry", "Firework"),
        ("Lady Gaga", "Shallow"),
        ("Charli xcx", "Sympathy is a knife")
    ]
    
    for artist, song in songs:
        save_lyrics(artist, song)