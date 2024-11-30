# Modeling Universal Sentiment in Culture (MUSIC)
### Anika Fuloria, Peyton Lee, Janelle Rudolph

(Title in progress.)

This model seeks to better understand the social psychology behind music. By analyzing lyrics, genre trends, and other song metadata, MUSIC seeks to dive deeper into how and why pop culture reflects the sociopolitical environment it's created in.

To set up the codebase, you will need a Genius API Token. Get one here: https://genius.com/api-clients.

### Setup
Install miniconda3. Run `sh setup.sh` then activate the conda environment with `conda activate cs229`.

### Data files
Deprecated files:
hot-100.csv
 - This is not ours, found online.
 - SCHEMA: chart_position,chart_date,song,performer,song_id,instance,time_on_chart,consecutive_weeks,previous_week,peak_position,worst_position,chart_debut,chart_url

song-lyrics folder
 - Lyrics of ~20 songs scraped directly from Genius
 - Saved as separate files

song-metadata.csv
 - Metadata for ~20 songs saved in CSV

Current files:
processed-hot-100.csv
 - Transformed version of hot-100.csv which has the columns that we want.
 - SCHEMA: song,performer,chart_instances,time_on_chart,peak_position,worst_position
 - Here, time_on_chart is a list of values that has pairs of date/position

sample-processed-hot-100.csv
 - Copy of the first 500ish datapoints from the processed-hot-100.csv. Using this to train before we get cluster access.
 - Same schema as above.

processed-hot-100-with-lyrics-metadata.csv
 - SCHEMA: song,performer,chart_instances,time_on_chart,peak_position,worst_position,lyrics,metadata
 - Here, lyrics are a single string, with line breaks being denoted by "/".
 - Here, metadata is a dictionary with keys of 'Producer', 'Writers' (list), 'Release Date', and 'Tags' (list).

### Other stuff
SAMPLE SCRAPE: ENDING ON MEH (Playboi Carti, ROW 512)
SCRAPE 1: ENDING ON BAD BOY THIS BAD BOY THAT (Bad Boy's Da Band, ROW 512 + 1762)
SCRAPE 2: ENDING ON BETTER AS A MEMORY (Kenny Chesney, ROW 512 + 1762 + 505)
SCRAPE 3: ENDING ON Callin' Doctor Casey (John D. Loudermilk, ROW 512 + 1762 + 505 + 1093)
SCRAPE 4: ENDING ON DOIN' THIS (Luke Combs, ROW 512 + 1762 + 505 + 1093 + 2235)
SCRAPE 5: ENDING ON DRINK IN MY HAND (Eric Church, ROW 512 + 1762 + 505 + 1093 + 2235 + 614)
SCRAPE 6: ENDING ON EYES CLOSED (Ed Sheeran, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656)
SCRAPE 7: ENDING ON GETTING AWAY WITH IT (Electronic, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307)
SCRAPE 8: ENDING ON HEAT OF THE MOMENT (Asia, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307 + 1371)
SCRAPE 9: ENDING ON INSIDE A DREAM (Jane Wiedlin, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307 + 1371 + 3413)
SCRAPE 10: ENDING ON LOVE SOMEBODY (Maroon 5, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307 + 1371 + 3413 + 2970)
SCRAPE 11: ENDING ON SUPERMODEL (Rupaul, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307 + 1371 + 3413 + 2970 + 8227)
SCRAPE 12: ENDING ON ALL SONGS SCRAPED (ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307 + 1371 + 3413 + 2970 + 8227 + 6616)

SPLIT INTO 3 FILES TO MATCH GITHUB FILE LIMIT!