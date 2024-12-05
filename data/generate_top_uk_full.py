import csv
import requests
from bs4 import BeautifulSoup

# Set your Genius API credentials here
GENIUS_ACCESS_TOKEN = "3IrbfUKApru5Ps6aHT3jQR9yGh0d6xSweOE52ogogZJb331vmRbs62Z7yKnDB9-e"
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
    
    soup = BeautifulSoup(response.content, 'html.parser')
    lyrics_div = soup.find_all('div', {'data-lyrics-container': 'true'})
    
    if not lyrics_div:
        raise Exception(f"Error: Could not find lyrics on the page {lyrics_url}")
    
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
def update_csv_with_lyrics_metadata(songs_artists, output_csv):
    fieldnames = ['song', 'artist', 'lyrics', 'metadata']
    with open(output_csv, 'a', encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if output_file.tell() == 0:
            writer.writeheader()

        for year, song_title, artist in songs_artists:
            try:
                song_id = search_song(artist, song_title)
                lyrics_url = get_song_lyrics_url(song_id)
                lyrics = fetch_raw_lyrics(lyrics_url)
                metadata = fetch_song_metadata(lyrics_url)
                row = {
                    'song': song_title,
                    'artist': artist,
                    'lyrics': lyrics,
                    'metadata': metadata
                }
            except Exception as e:
                print(f"Error fetching data for {song_title} by {artist}: {e}")
                row = {
                    'song': song_title,
                    'artist': artist,
                    'lyrics': 'Error',
                    'metadata': 'Error'
                }

            writer.writerow(row)
            print(f"Processed: {song_title} by {artist}")

# Define the list of songs and artists
songs_artists = [
    (1952, "Singin' In The Rain", "Gene Kelly"),
    (1953, "That's Amore", "Dean Martin"),
    (1954, "I've Got A Woman", "Ray Charles"),
    (1955, "Tutti Frutti", "Little Richard"),
    (1956, "I Walk The Line", "Johnny Cash"),
    (1957, "Jailhouse Rock", "Elvis Presley"),
    (1958, "Johnny B. Goode", "Chuck Berry"),
    (1959, "Put Your Head On My Shoulder", "Paul Anka"),
    (1960, "At Last", "Etta James"),
    (1961, "Stand By Me", "Ben E King"),
    (1962, "Cry To Me", "Solomon Burke"),
    (1963, "Be My Baby", "Ronettes"),
    (1964, "My Girl", "The Temptations"),
    (1965, "I Can't Help Myself", "Four Tops"),
    (1966, "Paint It Black", "Rolling Stones"),
    (1967, "Ain't No Mountain High Enough", "Marvin Gaye & Tammi Terrell"),
    (1968, "(Sittin' On The) Dock Of The Bay", "Otis Redding"),
    (1969, "Here Comes The Sun", "Beatles"),
    (1970, "Your Song", "Elton John"),
    (1971, "Take Me Home Country Roads", "John Denver"),
    (1972, "Tiny Dancer", "Elton John"),
    (1973, "Jolene", "Dolly Parton"),
    (1974, "Sweet Home Alabama", "Lynyrd Skynyrd"),
    (1975, "Bohemian Rhapsody", "Queen"),
    (1976, "Go Your Own Way", "Fleetwood Mac"),
    (1977, "Dreams", "Fleetwood Mac"),
    (1978, "September", "Earth Wind & Fire"),
    (1979, "Don't Stop Me Now", "Queen"),
    (1980, "Another One Bites The Dust", "Queen"),
    (1981, "Don't Stop Believin'", "Journey"),
    (1982, "Africa", "Toto"),
    (1983, "Sweet Dreams (Are Made Of This)", "Eurythmics"),
    (1984, "Wake Me Up Before You Go Go", "Wham"),
    (1985, "Summer Of '69", "Bryan Adams"),
    (1986, "Livin' On A Prayer", "Bon Jovi"),
    (1987, "I Wanna Dance With Somebody", "Whitney Houston"),
    (1988, "Everywhere", "Fleetwood Mac"),
    (1989, "We Didn't Start The Fire", "Billy Joel"),
    (1990, "Thunderstruck", "AC/DC"),
    (1991, "Smells Like Teen Spirit", "Nirvana"),
    (1992, "Creep", "Radiohead"),
    (1993, "What Is Love?", "Haddaway"),
    (1994, "Juicy", "The Notorious B.I.G"),
    (1995, "Wonderwall", "Oasis"),
    (1996, "No Diggity", "Blackstreet Ft. Dr Dre"),
    (1997, "Bitter Sweet Symphony", "The Verve"),
    (1998, "Iris", "Goo Goo Dolls"),
    (1999, "No Scrubs", "TLC"),
    (2000, "Dancing In The Moonlight", "Toploader"),
    (2001, "How You Remind Me", "Nickelback"),
    (2002, "Lose Yourself", "Eminem"),
    (2003, "Mr Brightside", "The Killers"),
    (2004, "Let Me Love You", "Mario"),
    (2005, "I Bet You Look Good On The Dancefloor", "Arctic Monkeys"),
    (2006, "Naïve", "The Kooks"),
    (2007, "Fluorescent Adolescent", "Arctic Monkeys"),
    (2008, "I'm Yours", "Jason Mraz"),
    (2009, "Party In The USA", "Miley Cyrus"),
    (2010, "Love The Way You Lie", "Eminem Ft. Rihanna"),
    (2011, "Someone Like You", "Adele"),
    (2012, "Let Her Go", "Passenger"),
    (2013, "Riptide", "Vance Joy"),
    (2014, "Thinking Out Loud", "Ed Sheeran"),
    (2015, "Cheap Thrills", "Sia"),
    (2016, "Say You Won't Let Go", "James Arthur"),
    (2017, "Shape Of You", "Ed Sheeran"),
    (2018, "Someone You Loved", "Lewis Capaldi"),
    (2019, "Dance Monkey", "Tones & I"),
    (2020, "Head & Heart", "Joel Corry Ft. MNEK"),
    (2021, "Bad Habits", "Ed Sheeran"),
    (2022, "As It Was", "Harry Styles")
]

output_csv = "data/top_uk_songs_lyrics_metadata.csv"
update_csv_with_lyrics_metadata(songs_artists, output_csv)