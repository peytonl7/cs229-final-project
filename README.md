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
Anika's Note: Ran into errors parsing these songs for processed-hot-100-with-lyrics-metadata.csv:
Error fetching data for Inez & Charlie Foxx - (1-2-3-4-5-6-7) Count The Days: Error: No results found for Inez & Charlie Foxx - (1-2-3-4-5-6-7) Count The Days
Error fetching data for Maxine Nightingale - (Bringing Out) The Girl In Me: Error: Could not find lyrics on the page https://genius.com/Maxine-nightingale-bringing-it-out-the-girl-in-me-lyrics
Error fetching data for Duane Eddy and the Rebelettes - (Dance With The) Guitar Man: Error: No results found for Duane Eddy and the Rebelettes - (Dance With The) Guitar Man
Error fetching data for Nat Kendrick And The Swans - (Do The) Mashed Potatoes (Part 1): Error: No results found for Nat Kendrick And The Swans - (Do The) Mashed Potatoes (Part 1)
Error fetching data for Ramrods - (Ghost) Riders In The Sky: Error: Could not find lyrics on the page https://genius.com/The-ramrods-ghost-riders-in-the-sky-lyrics
Error fetching data for Cheech & Chong - (How I Spent My Summer Vacation) Or A Day At The Beach With Pedro & Man - P: Error: No results found for Cheech & Chong - (How I Spent My Summer Vacation) Or A Day At The Beach With Pedro & Man - P
Error fetching data for Bill Doggett - (Let's Do) The Hully Gully Twist: Error: No results found for Bill Doggett - (Let's Do) The Hully Gully Twist
Error fetching data for Ferrante & Teicher - (Love Theme From) One Eyed Jacks: Error: No results found for Ferrante & Teicher - (Love Theme From) One Eyed Jacks
Error fetching data for George Torrence & The Naturals - (Mama Come Quick, and Bring Your) Lickin' Stick: Error: No results found for George Torrence & The Naturals - (Mama Come Quick, and Bring Your) Lickin' Stick
Error fetching data for The B.C. 52's - (Meet) The Flintstones (From "The Flintstones"): Error: No results found for The B.C. 52's - (Meet) The Flintstones (From "The Flintstones")
Error fetching data for Elvis Presley With The Jordanaires - (Now and Then There's) A Fool Such As I: Error: No results found for Elvis Presley With The Jordanaires - (Now and Then There's) A Fool Such As I
Error fetching data for Elton John - (Sartorial Eloquence) Don't Ya Wanna Play This Game No More?: Error: No results found for Elton John - (Sartorial Eloquence) Don't Ya Wanna Play This Game No More?
Error fetching data for Elvis Presley With The Jordanaires - (Such An) Easy Question: Error: No results found for Elvis Presley With The Jordanaires - (Such An) Easy Question
Error fetching data for Mantovani & His Orchestra - (Theme From) The Sundowners: Error: No results found for Mantovani & His Orchestra - (Theme From) The Sundowners
Error fetching data for Perry Como With Mitchell Ayers And His Orchestra - (There's No Place Like) Home For The Holidays (1954): Error: No results found for Perry Como With Mitchell Ayers And His Orchestra - (There's No Place Like) Home For The Holidays (1954)
Error fetching data for Perry Como With Mitchell Ayers And His Orchestra - (There's No Place Like) Home For The Holidays (1959): Error: No results found for Perry Como With Mitchell Ayers And His Orchestra - (There's No Place Like) Home For The Holidays (1959)
Error fetching data for Jerry Butler & Brenda Lee Eager - (They Long To Be) Close To You: Error: No results found for Jerry Butler & Brenda Lee Eager - (They Long To Be) Close To You
Error fetching data for Mary J. Blige - (You Make Me Feel Like) A Natural Woman (From "New York Undercover"): Error: No results found for Mary J. Blige - (You Make Me Feel Like) A Natural Woman (From "New York Undercover")
Error fetching data for Elvis Presley With The Jordanaires - (You're the) Devil In Disguise: Error: No results found for Elvis Presley With The Jordanaires - (You're the) Devil In Disguise
Error fetching data for Mitch Ryder - (You've Got) Personality And Chantilly Lace: Error: No results found for Mitch Ryder - (You've Got) Personality And Chantilly Lace
Error fetching data for Sandy Nelson - ...And Then There Were Drums: Error: Could not find lyrics on the page https://genius.com/Sandy-nelson-and-then-there-were-drums-lyrics
Error fetching data for East Coast Family - 1-4-All-4-1: Error: Could not find lyrics on the page https://genius.com/East-coast-family-1-4-all-4-1-lyrics
Error fetching data for A Boogie Wit da Hoodie Featuring Lil Durk - 24 Hours: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-24-hours-8-bit-a-boogie-wit-da-hoodie-and-lil-durk-emulation-lyrics
Error fetching data for Redhead Kingpin & The F.B.I. - 3-2-1 Pump: Error: Could not find lyrics on the page https://genius.com/Redhead-kingpin-and-the-fbi-3-2-1-pump-lyrics
Error fetching data for Willie Mitchell - 30-60-90: Error: No results found for Willie Mitchell - 30-60-90
Error fetching data for Herb Alpert & The Tijuana Brass - 3rd Man Theme: Error: Could not find lyrics on the page https://genius.com/Herb-alpert-and-the-tijuana-brass-3rd-man-theme-lyrics
Error fetching data for Wilson Pickett - 634-5789 (Soulsville, U.S.A.): Error: No results found for Wilson Pickett - 634-5789 (Soulsville, U.S.A.)
Error fetching data for Gary Toms Empire - 7-6-5-4-3-2-1 (Blow Your Whistle): Error: No results found for Gary Toms Empire - 7-6-5-4-3-2-1 (Blow Your Whistle)