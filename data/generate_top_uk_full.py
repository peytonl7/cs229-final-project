import pandas as pd

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

# Load the CSVs
lyrics_metadata_parts = [
    "data/processed-hot-100-with-lyrics-metadata-part-1.csv",
    "data/processed-hot-100-with-lyrics-metadata-part-2.csv",
    "data/processed-hot-100-with-lyrics-metadata-part-3.csv"
]
lyrics_metadata = pd.concat(
    [pd.read_csv(file) for file in lyrics_metadata_parts], 
    ignore_index=True
)

# Convert the list into a DataFrame for easier lookup
songs_df = pd.DataFrame(songs_artists, columns=["year", "song", "performer"])

# Merge and filter for matching songs and artists
matched_songs = lyrics_metadata.merge(
    songs_df,
    left_on=["song", "performer"],
    right_on=["song", "performer"],
    how="inner"
)

# Save the result to a new CSV
matched_songs.to_csv("data/top_uk_songs_lyrics_metadata.csv", index=False)

print(f"Filtered UK songs saved to 'top_uk_songs_lyrics_metadata.csv'.")