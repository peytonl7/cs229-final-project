import os
import requests
import csv
from bs4 import BeautifulSoup

# Set your Genius API credentials here
GENIUS_ACCESS_TOKEN = "dwbhA7NCxpYyEhrWGEaEgujR_vUoaRJjbFaQI8lwUnuL294EprKXKs6-aEmgZdMK"

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


# Function to fetch the metadata from the Genius lyrics page
def fetch_song_metadata(url, song_title, artist):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Define the metadata structure with initial values
    metadata = {
        'Title': song_title,
        'Artist': artist,
        'Producer': 'N/A',
        'Writers': 'N/A',
        'Mastered At': 'N/A',
        'Publishers': 'N/A',
        'Mastering Engineer': 'N/A',
        'Video Animator': 'N/A',
        'Label': 'N/A',
        'Copyright': 'N/A',
        'Phonographic Copyright': 'N/A',
        'Keyboards': 'N/A',
        'Recording Engineer': 'N/A',
        'Mixing Engineer': 'N/A',
        'Release Date': 'N/A',
        'Tags': 'N/A',
        'Filename': 'N/A'
    }

    producer = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Producer")) a')
    metadata['Producer'] = producer.get_text(strip=True) if producer else 'N/A'

    writers = soup.select('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Writers")) a')
    metadata['Writers'] = ', '.join([writer.get_text(strip=True) for writer in writers]) if writers else 'N/A'

    mastered_at = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Mastered At")) a')
    metadata['Mastered At'] = mastered_at.get_text(strip=True) if mastered_at else 'N/A'

    publishers = soup.select('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Publisher")) a')
    metadata['Publishers'] = ', '.join([publisher.get_text(strip=True) for publisher in publishers]) if publishers else 'N/A'

    mastering_engineer = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Mastering Engineer")) a')
    metadata['Mastering Engineer'] = mastering_engineer.get_text(strip=True) if mastering_engineer else 'N/A'

    video_animator = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Video Animator")) a')
    metadata['Video Animator'] = video_animator.get_text(strip=True) if video_animator else 'N/A'

    label = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Label")) a')
    metadata['Label'] = label.get_text(strip=True) if label else 'N/A'

    copyright_info = soup.select('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Copyright ©")) a')
    metadata['Copyright'] = ', '.join([copyright.get_text(strip=True) for copyright in copyright_info]) if copyright_info else 'N/A'

    phonographic_copyright = soup.select('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Phonographic Copyright ℗")) a')
    metadata['Phonographic Copyright'] = ', '.join([phonograph.get_text(strip=True) for phonograph in phonographic_copyright]) if phonographic_copyright else 'N/A'

    keyboards = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Keyboards")) a')
    metadata['Keyboards'] = keyboards.get_text(strip=True) if keyboards else 'N/A'

    recording_engineer = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Recording Engineer")) a')
    metadata['Recording Engineer'] = recording_engineer.get_text(strip=True) if recording_engineer else 'N/A'

    mixing_engineer = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Mixing Engineer")) a')
    metadata['Mixing Engineer'] = mixing_engineer.get_text(strip=True) if mixing_engineer else 'N/A'

    release_date = soup.select_one('.SongInfo__Container-nekw6x-0 .SongInfo__Credit-nekw6x-3:has(.SongInfo__Label-nekw6x-4:-soup-contains("Released on"))')
    metadata['Release Date'] = release_date.get_text(strip=True).replace("Released on", "").strip() if release_date else 'N/A'

    tags = soup.select('.SongTags__Tag-nekw6x-5 a')
    metadata['Tags'] = ', '.join([tag.get_text(strip=True) for tag in tags]) if tags else 'N/A'

    file_name = f"{artist}-{song_title}.txt".replace(' ', '_').lower()
    metadata['Lyrics file name'] = file_name
    
    return metadata


# Function to get and save song metadata
def save_metadata(artist, song_title):
    try:
        song_id = search_song(artist, song_title)
        lyrics_url = get_song_lyrics_url(song_id)
        metadata = fetch_song_metadata(lyrics_url, song_title, artist)

        csv_filename = './../../data/song-metadata/song-metadata-eval.csv'
        # Save metadata to song-metadata.txt
        with open(csv_filename, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=metadata.keys())
            writer.writerow(metadata)
        
        print(f"Metadata saved for {artist} - {song_title}")
    
    except Exception as e:
        # Log the error into error.txt
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.write(f"{artist} - {song_title}: {str(e)}\n")
        print(f"Error: {e}")


if __name__ == '__main__':
    songs = [
        # Train
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

        # Evaluate
        ("Nelly", "Just a Dream"),
        ("Bruno Mars", "Marry You"),
        ("Post Malone", "Congratulations"),
        ("Dua Lipa", "New Rules"),
        ("Halsey", "Without Me")
    ]
    
    for artist, song in songs:
        save_metadata(artist, song)