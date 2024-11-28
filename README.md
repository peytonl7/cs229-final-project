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

SAMPLE SCRAPE: ENDING ON MEH (Playboi Carti, ROW 512)

Error fetching data for Herb Alpert & The Tijuana Brass - A Banda (Ah Bahn-da): Error: No results found for Herb Alpert & The Tijuana Brass - A Banda (Ah Bahn-da)
Error fetching data for Elvis Presley With The Jordanaires - A Big Hunk O' Love: Error: No results found for Elvis Presley With The Jordanaires - A Big Hunk O' Love
Error fetching data for Walter Murphy & The Big Apple Band - A Fifth Of Beethoven: Error: Could not find lyrics on the page https://genius.com/Walter-murphy-a-fifth-of-beethoven-lyrics
Error fetching data for The G-Clefs - A Girl Has To Know: Error: No results found for The G-Clefs - A Girl Has To Know
Error fetching data for Elvis Presley With The Jordanaires - A Little Less Conversation: Error: No results found for Elvis Presley With The Jordanaires - A Little Less Conversation
Error fetching data for The Chi-lites - A Lonely Man/The Man & The Woman (The Boy & The Girl): Error: No results found for The Chi-lites - A Lonely Man/The Man & The Woman (The Boy & The Girl)
Error fetching data for Runt-Todd Rundgren - A Long Time, A Long Way To Go: Error: No results found for Runt-Todd Rundgren - A Long Time, A Long Way To Go
Error fetching data for Engelbert Humperdinck - A Man Without Love (Quando M'innamoro): Error: No results found for Engelbert Humperdinck - A Man Without Love (Quando M'innamoro)
Error fetching data for Elvis Presley With The Jordanaires - A Mess Of Blues: Error: No results found for Elvis Presley With The Jordanaires - A Mess Of Blues
Error fetching data for Five Stairsteps & Cubie - A Million To One: Error: No results found for Five Stairsteps & Cubie - A Million To One
Error fetching data for Jimmy Charles and The Revelletts - A Million To One: Error: No results found for Jimmy Charles and The Revelletts - A Million To One
Error fetching data for The Shacklefords - A Stranger In Your Town: Error: No results found for The Shacklefords - A Stranger In Your Town
Error fetching data for Lenny Welch - A Sunday Kind Of Love: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
Error fetching data for Billy Vaughn And His Orchestra - A Swingin' Safari: Error: No results found for Billy Vaughn And His Orchestra - A Swingin' Safari
Error fetching data for Lou Johnson - A Time To Love-A Time To Cry (Petite Fleur): Error: No results found for Lou Johnson - A Time To Love-A Time To Cry (Petite Fleur)
Error fetching data for Horst Jankowski - A Walk In The Black Forest: Error: Could not find lyrics on the page https://genius.com/Horst-jankowski-a-walk-in-the-black-forest-lyrics
Error fetching data for Edwin Starr - Abyssinia Jones: Error: No results found for Edwin Starr - Abyssinia Jones
Error fetching data for Cannonball Adderley Orchestra - African Waltz: Error: No results found for Cannonball Adderley Orchestra - African Waltz
Error fetching data for Kongas - Africanism/Gimme Some Lovin': Error: No results found for Kongas - Africanism/Gimme Some Lovin'
Error fetching data for Bert Kaempfert And His Orchestra - Afrikaan Beat: Error: No results found for Bert Kaempfert And His Orchestra - Afrikaan Beat
Error fetching data for The Nite-Liters - Afro-Strut: Error: No results found for The Nite-Liters - Afro-Strut
Error fetching data for Quincy Jones - Ai No Corrida (I-No-Ko-ree-da): Error: No results found for Quincy Jones - Ai No Corrida (I-No-Ko-ree-da)
Error fetching data for The Five Stairsteps - Ain't Gonna Rest (Till I Get You): Error: No results found for The Five Stairsteps - Ain't Gonna Rest (Till I Get You)
Error fetching data for Chris Christian (with Amy Holland) - Ain't Nothing Like The Real Thing/You're All I Need To Get By: Error: No results found for Chris Christian (with Amy Holland) - Ain't Nothing Like The Real Thing/You're All I Need To Get By
Error fetching data for Vincent Bell - Airport Love Theme (Gwen And Vern): Error: No results found for Vincent Bell - Airport Love Theme (Gwen And Vern)
Error fetching data for Hudson and Landry - Ajax Airlines: Error: No results found for Hudson and Landry - Ajax Airlines
Error fetching data for Tommy Boyce & Bobby Hart - Alice Long (You're Still My Favorite Girlfriend): Error: No results found for Tommy Boyce & Bobby Hart - Alice Long (You're Still My Favorite Girlfriend)
Error fetching data for Jimmy McGriff - All About My Girl: Error: Could not find lyrics on the page https://genius.com/Jimmy-mcgriff-all-about-my-girl-lyrics
Error fetching data for Lisa Lisa And Cult Jam With Full Force Featuring Paul Anthony & Bow Legged Lou - All Cried Out: Error: No results found for Lisa Lisa And Cult Jam With Full Force Featuring Paul Anthony & Bow Legged Lou - All Cried Out
Error fetching data for Linda Ronstadt (Featuring Aaron Neville) - All My Life: Error: No results found for Linda Ronstadt (Featuring Aaron Neville) - All My Life
Error fetching data for Sandy Nelson - All Night Long: Error: Could not find lyrics on the page https://genius.com/Sandy-nelson-all-night-long-lyrics
Error fetching data for Elvis Presley With The Jordanaires - All That I Am: Error: No results found for Elvis Presley With The Jordanaires - All That I Am
Error fetching data for Lou Donaldson - Alligator Bogaloo: Error: Could not find lyrics on the page https://genius.com/Lou-donaldson-alligator-bogaloo-lyrics
Error fetching data for Elvis Presley With The Jordanaires - Almost In Love: Error: No results found for Elvis Presley With The Jordanaires - Almost In Love
Error fetching data for Mike Reno And Ann Wilson - Almost Paradise...Love Theme From Footloose: Error: No results found for Mike Reno And Ann Wilson - Almost Paradise...Love Theme From Footloose
Error fetching data for Roxette - Almost Unreal (From "Super Mario Bros."): Error: No results found for Roxette - Almost Unreal (From "Super Mario Bros.")
Error fetching data for Dunn & McCashen - Alright In The City: Error: No results found for Dunn & McCashen - Alright In The City
Error fetching data for Deodato - Also Sprach Zarathustra (2001): Error: Could not find lyrics on the page https://genius.com/Eumir-deodato-also-sprach-zarathustra-2001-lyrics
Error fetching data for Alvin Cash & The Registers - Alvin's Boo-Ga-Loo: Error: No results found for Alvin Cash & The Registers - Alvin's Boo-Ga-Loo
Error fetching data for Los Indios Tabajaras - Always In My Heart: Error: Could not find lyrics on the page https://genius.com/Los-indios-tabajaras-always-in-my-heart-lyrics
Error fetching data for Jacky Noguez And His Orchestra - Amapola: Error: No results found for Jacky Noguez And His Orchestra - Amapola
Error fetching data for The Pipes And Drums And The Military Band Of The Royal Scots Dragoon Guards - Amazing Grace: Error: Could not find lyrics on the page https://genius.com/The-pipes-and-drums-of-the-military-band-of-the-royal-scots-dragoon-guards-amazing-grace-lyrics
Error fetching data for Raymond Lefevre and His Orchestra - Ame Caline (Soul Coaxing): Error: No results found for Raymond Lefevre and His Orchestra - Ame Caline (Soul Coaxing)
Error fetching data for The Five Stairsteps - America/Standing/Because I Love You: Error: No results found for The Five Stairsteps - America/Standing/Because I Love You
Error fetching data for Jorgen Ingmann & His Guitar - Anna: Error: No results found for Jorgen Ingmann & His Guitar - Anna
Error fetching data for Hamilton, Joe Frank & Reynolds - Annabella: Error: No results found for Hamilton, Joe Frank & Reynolds - Annabella
Error fetching data for Ferrante & Teicher - Antony And Cleopatra Theme: Error: No results found for Ferrante & Teicher - Antony And Cleopatra Theme
Error fetching data for Elvis Presley With The Jordanaires - Anything That's Part Of You: Error: No results found for Elvis Presley With The Jordanaires - Anything That's Part Of You
Error fetching data for Jorgen Ingmann & His Guitar - Apache: Error: No results found for Jorgen Ingmann & His Guitar - Apache
Error fetching data for Rhinoceros - Apricot Brandy: Error: Could not find lyrics on the page https://genius.com/Rhinoceros-apricot-brandy-lyrics
Error fetching data for Elvis Presley With The Jordanaires - Are You Lonesome To-night?: Error: No results found for Elvis Presley With The Jordanaires - Are You Lonesome To-night?
Error fetching data for Elvis Presley With The Jordanaires - Ask Me: Error: No results found for Elvis Presley With The Jordanaires - Ask Me
Error fetching data for Harold Faltermeyer - Axel F: Error: Could not find lyrics on the page https://genius.com/Harold-faltermeyer-axel-f-lyrics
Error fetching data for Mulatto - B*tch From da Souf: Error: No results found for Mulatto - B*tch From da Souf
Error fetching data for Anna King-Bobby Byrd - Baby Baby Baby: Error: No results found for Anna King-Bobby Byrd - Baby Baby Baby
Error fetching data for Garnet Mimms & The Enchanters - Baby Don't You Weep: Error: No results found for Garnet Mimms & The Enchanters - Baby Don't You Weep
Error fetching data for ConFunkShun - Baby I'm Hooked: Error: No results found for ConFunkShun - Baby I'm Hooked
Error fetching data for Idina Menzel Duet With Michael Buble - Baby It's Cold Outside: Error: No results found for Idina Menzel Duet With Michael Buble - Baby It's Cold Outside
Error fetching data for Ray Charles and his Orchestra - Baby, Don't You Cry (The New Swingova Rhythm): Error: No results found for Ray Charles and his Orchestra - Baby, Don't You Cry (The New Swingova Rhythm)
Error fetching data for Mel And Tim - Backfield In Motion: Error: Could not find lyrics on the page https://genius.com/Mel-and-tim-backfield-in-motion-starting-all-over-again-live-at-the-summit-club-1972-lyrics
Error fetching data for Taylor Swift Featuring Kendrick Lamar - Bad Blood: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-bad-blood-8-bit-taylor-swift-and-kendrick-lammar-emulation-lyrics


SCRAPE 1: ENDING ON BAD BOY THIS BAD BOY THAT (Bad Boy's Da Band, ROW 512 + 1762)

Error fetching data for The Astronauts - Baja: Error: Could not find lyrics on the page https://genius.com/The-astronauts-surf-rock-baja-lyrics
Error fetching data for The Marketts - Balboa Blue: Error: Could not find lyrics on the page https://genius.com/The-marketts-balboa-blue-lyrics
Error fetching data for David Sanborn - Bang Bang: Error: Could not find lyrics on the page https://genius.com/David-sanborn-bang-bang-lyrics
Error fetching data for George Harrison - Bangla-Desh/Deep Blue: Error: No results found for George Harrison - Bangla-Desh/Deep Blue
Error fetching data for Dorothy Collins - Banjo Boy: Error: No results found for Dorothy Collins - Banjo Boy
Error fetching data for Henry Mancini And His Orchestra - Banzai Pipeline: Error: No results found for Henry Mancini And His Orchestra - Banzai Pipeline
Error fetching data for Mason Williams - Baroque-A-Nova: Error: Could not find lyrics on the page https://genius.com/Mason-williams-baroque-a-nova-lyrics
Error fetching data for Andy Williams with the St. Charles Borromeo Choir - Battle Hymn Of The Republic: Error: No results found for Andy Williams with the St. Charles Borromeo Choir - Battle Hymn Of The Republic
Error fetching data for Fred Darian - Battle Of Gettysburg: Error: No results found for Fred Darian - Battle Of Gettysburg
Error fetching data for Cissy Houston - Be My Baby: Error: Could not find lyrics on the page https://genius.com/Cissy-houston-be-my-baby-lyrics
Error fetching data for Runt-Todd Rundgren - Be Nice To Me: Error: No results found for Runt-Todd Rundgren - Be Nice To Me
Error fetching data for Dave York and The Beachcombers - Beach Party: Error: No results found for Dave York and The Beachcombers - Beach Party
Error fetching data for Bobby Darin - Beachcomber: Error: Could not find lyrics on the page https://genius.com/Bobby-darin-beachcomber-lyrics
Error fetching data for Lloyd Banks Featuring Juelz Santana - Beamer, Benz, Or Bentley: Error: Could not find lyrics on the page https://genius.com/Dj-redo-beamer-benz-or-bentley-lloyd-banks-feat-juelz-santana-beamer-benz-or-bentlyinstrumental-lyrics
Error fetching data for Christina Aguilera & Beverly McClellan - Beautiful: Error: No results found for Christina Aguilera & Beverly McClellan - Beautiful
Error fetching data for Goo Goo Dolls - Before It's Too Late (Sam And Mikaela's Theme): Error: No results found for Goo Goo Dolls - Before It's Too Late (Sam And Mikaela's Theme)
Error fetching data for ¥$: Ye & Ty Dolla $ign - Beg Forgiveness: Error: No results found for ¥$: Ye & Ty Dolla $ign - Beg Forgiveness
Error fetching data for Louis Prima And Keely Smith - Bei Mir Bist Du Schön: Error: No results found for Louis Prima And Keely Smith - Bei Mir Bist Du Schön
Error fetching data for Billy Vaughn And His Orchestra - Berlin Melody: Error: No results found for Billy Vaughn And His Orchestra - Berlin Melody
Error fetching data for Puff Daddy Featuring Mario Winans & Hezekiah Walker & The Love Fe - Best Friend: Error: No results found for Puff Daddy Featuring Mario Winans & Hezekiah Walker & The Love Fe - Best Friend
Error fetching data for Saweetie Featuring Doja Cat - Best Friend: Error: Could not find lyrics on the page https://genius.com/Phix-best-friend-saweetie-and-doja-cat-remix-lyrics
Error fetching data for The Stylistics Featuring Russell Thompkins,Jr. - Betcha By Golly, Wow: Error: No results found for The Stylistics Featuring Russell Thompkins,Jr. - Betcha By Golly, Wow

SCRAPE 2: ENDING ON BETTER AS A MEMORY (Kenny Chesney, ROW 512 + 1762 + 505)

Error fetching data for The Dovells - Betty In Bermudas: Error: No results found for The Dovells - Betty In Bermudas
Error fetching data for L.B.C. Crew Feat. Tray D & South Sentrell - Beware Of My Crew (From "A Thin Line Between Love And Hate"): Error: No results found for L.B.C. Crew Feat. Tray D & South Sentrell - Beware Of My Crew (From "A Thin Line Between Love And Hate")
Error fetching data for Herb Alpert - Beyond: Error: Could not find lyrics on the page https://genius.com/Herb-alpert-beyond-lyrics
Error fetching data for Foxy Brown Featuring Dru Hill - Big Bad Mamma (From "Def Jam's How To Be A Player"): Error: No results found for Foxy Brown Featuring Dru Hill - Big Bad Mamma (From "Def Jam's How To Be A Player")
Error fetching data for Israel "Popper Stopper" Tolbert - Big Leg Woman (With A Short Short Mini Skirt): Error: No results found for Israel "Popper Stopper" Tolbert - Big Leg Woman (With A Short Short Mini Skirt)
Error fetching data for Joe Henderson - Big Love: Error: Could not find lyrics on the page https://genius.com/Joe-henderson-gospel-big-love-lyrics
Error fetching data for The 4 Seasons Featuring the "Sound of Frankie Valli" - Big Man In Town: Error: No results found for The 4 Seasons Featuring the "Sound of Frankie Valli" - Big Man In Town
Error fetching data for Teddy Randazzo - Big Wide World: Error: No results found for Teddy Randazzo - Big Wide World
Error fetching data for 2 Chainz, Drake & Quavo - Bigger > You: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-bigger-than-you-8-bit-2-chainz-drake-and-quavo-emulation-lyrics
Error fetching data for B.J. Thomas And The Triumphs - Billy And Sue: Error: No results found for B.J. Thomas And The Triumphs - Billy And Sue
Error fetching data for Barry DeVorzon and Perry Botkin, Jr. - Bless The Beasts And Children: Error: No results found for Barry DeVorzon and Perry Botkin, Jr. - Bless The Beasts And Children
Error fetching data for Uriah Heep - Blind Eye/Sweet Lorraine: Error: No results found for Uriah Heep - Blind Eye/Sweet Lorraine
Error fetching data for Bill Doggett - Blip Blop: Error: No results found for Bill Doggett - Blip Blop
Error fetching data for Billy Vaughn And His Orchestra - Blue Hawaii: Error: No results found for Billy Vaughn And His Orchestra - Blue Hawaii
Error fetching data for New Order - Blue Monday 1988: Error: Could not find lyrics on the page https://genius.com/New-order-blue-monday-1982-writing-session-recording-lyrics
Error fetching data for The Ventures - Blue Moon: Error: Could not find lyrics on the page https://genius.com/The-ventures-blue-moon-lyrics
Error fetching data for Mitch Miller and his Orchestra and Chorus - Bluebell: Error: No results found for Mitch Miller and his Orchestra and Chorus - Bluebell
Error fetching data for Anita Baker - Body & Soul: Error: Could not find lyrics on the page https://genius.com/Smooth-jazz-all-stars-body-and-soul-anita-baker-lyrics
Error fetching data for Al Caiola And His Orchestra - Bonanza: Error: No results found for Al Caiola And His Orchestra - Bonanza
Error fetching data for Preston Epps - Bongo Bongo Bongo: Error: Could not find lyrics on the page https://genius.com/Preston-epps-bongo-bongo-bongo-lyrics
Error fetching data for The Incredible Bongo Band - Bongo Rock: Error: Could not find lyrics on the page https://genius.com/The-incredible-bongo-band-bongo-rock-lyrics
Error fetching data for Duane Eddy His Twangy Guitar And The Rebels - Bonnie Came Back: Error: No results found for Duane Eddy His Twangy Guitar And The Rebels - Bonnie Came Back
Error fetching data for Chet Atkins - Boo Boo Stick Beat: Error: Could not find lyrics on the page https://genius.com/Chet-atkins-boo-boo-stick-beat-lyrics
Error fetching data for Tom and Jerrio - Boo-Ga-Loo: Error: No results found for Tom and Jerrio - Boo-Ga-Loo
Error fetching data for Stan Robinson - Boom-A-Dip-Dip: Error: No results found for Stan Robinson - Boom-A-Dip-Dip
Error fetching data for Booker T. & The MG's - Boot-Leg: Error: Could not find lyrics on the page https://genius.com/Booker-t-and-the-mgs-boot-leg-lyrics
Error fetching data for Duane Eddy and the Rebelettes - Boss Guitar: Error: No results found for Duane Eddy and the Rebelettes - Boss Guitar
Error fetching data for Elvis Presley With The Jordanaires - Bossa Nova Baby: Error: No results found for Elvis Presley With The Jordanaires - Bossa Nova Baby
Error fetching data for The Dave Brubeck Quartet - Bossa Nova U.S.A.: Error: Could not find lyrics on the page https://genius.com/The-dave-brubeck-quartet-bossa-nova-usa-live-lyrics
Error fetching data for The String-A-Longs - Brass Buttons: Error: No results found for The String-A-Longs - Brass Buttons
Error fetching data for Tracey Ullman - Break-A-Way: Error: No results found for Tracey Ullman - Break-A-Way
Error fetching data for Zac Efron, Andrew Seeley & Vanessa Anne Hudgens - Breaking Free: Error: No results found for Zac Efron, Andrew Seeley & Vanessa Anne Hudgens - Breaking Free
Error fetching data for The Partridge Family Starring Shirley Jones Featuring David Cassidy - Breaking Up Is Hard To Do: Error: No results found for The Partridge Family Starring Shirley Jones Featuring David Cassidy - Breaking Up Is Hard To Do
Error fetching data for Bridgit Mendler, Adam Hicks, Naomi Scott & Hayley Kiyoko - Breakthrough: Error: No results found for Bridgit Mendler, Adam Hicks, Naomi Scott & Hayley Kiyoko - Breakthrough
Error fetching data for Lawrence Welk And His Orchestra - Breakwater: Error: No results found for Lawrence Welk And His Orchestra - Breakwater
Error fetching data for George Benson - Breezin': Error: Could not find lyrics on the page https://genius.com/George-benson-breezin-lyrics
Error fetching data for Michel Legrand - Brian's Song: Error: Could not find lyrics on the page https://genius.com/Michel-legrand-brians-song-lyrics
Error fetching data for Tiny Tim - Bring Back Those Rockabye Baby Days: Error: No results found for Tiny Tim - Bring Back Those Rockabye Baby Days
Error fetching data for Jo Dee Messina With Tim McGraw - Bring On The Rain: Error: No results found for Jo Dee Messina With Tim McGraw - Bring On The Rain
Error fetching data for The Piltdown Men - Brontosaurus Stomp: Error: Could not find lyrics on the page https://genius.com/The-piltdown-men-brontosaurus-stomp-lyrics
Error fetching data for Megan Thee Stallion Featuring Latto - Budget: Error: Could not find lyrics on the page https://genius.com/Polskie-tumaczenia-genius-megan-thee-stallion-budget-ft-latto-polskie-tumaczenie-lyrics
Error fetching data for The Fireballs - Bulldog: Error: Could not find lyrics on the page https://genius.com/The-fireballs-bulldog-lyrics
Error fetching data for Cyclones - Bullwhip Rock: Error: Could not find lyrics on the page https://genius.com/The-cyclones-rockabilly-bullwhip-rock-lyrics
Error fetching data for B. Bumble & The Stingers - Bumble Boogie: Error: Could not find lyrics on the page https://genius.com/B-bumble-and-the-stingers-bumble-boogie-lyrics
Error fetching data for Dooley Silverspoon - Bump Me Baby Part 1: Error: No results found for Dooley Silverspoon - Bump Me Baby Part 1
Error fetching data for ¥$: Ye & Ty Dolla $ign - Burn: Error: No results found for ¥$: Ye & Ty Dolla $ign - Burn
Error fetching data for The Busters - Bust Out: Error: Could not find lyrics on the page https://genius.com/The-busters-bust-out-lyrics
Error fetching data for Jordan Davis Featuring Luke Bryan - Buy Dirt: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-buy-dirt-8-bit-jordan-davis-and-luke-bryan-emulation-lyrics
Error fetching data for Shwayze Featuring Cisco Adler - Buzzin': Error: No results found for Shwayze Featuring Cisco Adler - Buzzin'
Error fetching data for Bert Kaempfert And His Orchestra - Bye Bye Blues: Error: No results found for Bert Kaempfert And His Orchestra - Bye Bye Blues
Error fetching data for The 4 Seasons Featuring the "Sound of Frankie Valli" - Bye, Bye, Baby (Baby, Goodbye): Error: No results found for The 4 Seasons Featuring the "Sound of Frankie Valli" - Bye, Bye, Baby (Baby, Goodbye)
Error fetching data for Coolio Featuring 40 Thevz - C U When U Get There (From "Nothing To Lose"): Error: No results found for Coolio Featuring 40 Thevz - C U When U Get There (From "Nothing To Lose")
Error fetching data for D-Mob Introducing Cathy Dennis - C'mon And Get My Love: Error: No results found for D-Mob Introducing Cathy Dennis - C'mon And Get My Love
Error fetching data for The 4 Seasons Featuring the "Sound of Frankie Valli" - C'mon Marianne: Error: No results found for The 4 Seasons Featuring the "Sound of Frankie Valli" - C'mon Marianne
Error fetching data for Herb Alpert & The Tijuana Brass - Cabaret: Error: No results found for Herb Alpert & The Tijuana Brass - Cabaret
Error fetching data for Spyro Gyra - Cafe Amore: Error: Could not find lyrics on the page https://genius.com/Spyro-gyra-cafe-amore-lyrics
Error fetching data for James Brown And His Orchestra - Caldonia: Error: No results found for James Brown And His Orchestra - Caldonia
Error fetching data for The Chainsmokers & Bebe Rexha - Call You Mine: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

SCRAPE 3: ENDING ON Callin' Doctor Casey (John D. Loudermilk, ROW 512 + 1762 + 505 + 1093)

Error fetching data for Jay-Z Featuring Amil (Of Major Coinz) & Ja - Can I Get A...: Error: No results found for Jay-Z Featuring Amil (Of Major Coinz) & Ja - Can I Get A...
Error fetching data for Zac Efron & Vanessa Hudgens - Can I Have This Dance: Error: No results found for Zac Efron & Vanessa Hudgens - Can I Have This Dance
Error fetching data for Mona Lisa Featuring Lost Boyz - Can't Be Wasting My Time (From "Don't Be A Menace..."): Error: No results found for Mona Lisa Featuring Lost Boyz - Can't Be Wasting My Time (From "Don't Be A Menace...")
Error fetching data for UB40 - Can't Help Falling In Love (From "Sliver"): Error: No results found for UB40 - Can't Help Falling In Love (From "Sliver")
Error fetching data for Elvis Presley With The Jordanaires - Can't Help Falling In Love: Error: No results found for Elvis Presley With The Jordanaires - Can't Help Falling In Love
Error fetching data for Dan Hill (Duet With Vonda Shepard) - Can't We Try: Error: No results found for Dan Hill (Duet With Vonda Shepard) - Can't We Try
Error fetching data for Etta Jones - Canadian Sunset: Error: No results found for Etta Jones - Canadian Sunset
Error fetching data for Duane Eddy His Twangy Guitar And The Rebels - Cannonball: Error: No results found for Duane Eddy His Twangy Guitar And The Rebels - Cannonball
Error fetching data for Santo & Johnny - Caravan: Error: Could not find lyrics on the page https://genius.com/Santo-and-johnny-caravan-lyrics
Error fetching data for Herb Alpert & The Tijuana Brass - Carmen: Error: Could not find lyrics on the page https://genius.com/Herb-alpert-and-the-tijuana-brass-carmen-lyrics
Error fetching data for Pharrell Williams Featuring 21 Savage & Tyler, The Creator - Cash In Cash Out: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-cash-in-cash-out-8-bit-pharrell-williams-21-savage-and-tyler-the-creator-emulation-lyrics
Error fetching data for Herb Alpert & The Tijuana Brass - Casino Royale: Error: Could not find lyrics on the page https://genius.com/Herb-alpert-and-the-tijuana-brass-casino-royale-lyrics
Error fetching data for Vince Guaraldi Trio - Cast Your Fate To The Wind: Error: Could not find lyrics on the page https://genius.com/Vince-guaraldi-trio-cast-your-fate-to-the-wind-lyrics
Error fetching data for Spyro Gyra - Catching The Sun: Error: Could not find lyrics on the page https://genius.com/Spyro-gyra-catching-the-sun-lyrics
Error fetching data for Bert Kaempfert And His Orchestra - Cerveza: Error: No results found for Bert Kaempfert And His Orchestra - Cerveza
Error fetching data for Boots Brown And His Blockbusters - Cerveza: Error: No results found for Boots Brown And His Blockbusters - Cerveza
Error fetching data for Herbie Hancock - Chameleon: Error: Could not find lyrics on the page https://genius.com/Herbie-hancock-chameleon-lyrics
Error fetching data for Sammy Kaye And His Orchestra - Charade: Error: No results found for Sammy Kaye And His Orchestra - Charade
Error fetching data for Chuck Mangione - Chase The Clouds Away: Error: Could not find lyrics on the page https://genius.com/Chuck-mangione-chase-the-clouds-away-lyrics
Error fetching data for Giorgio Moroder - Chase: Error: Could not find lyrics on the page https://genius.com/Giorgio-moroder-chase-lyrics
Error fetching data for Ernie Fields & Orch. - Chattanooga Choo Choo: Error: No results found for Ernie Fields & Orch. - Chattanooga Choo Choo
Error fetching data for Floyd Cramer - Chattanooga Choo Choo: Error: Could not find lyrics on the page https://genius.com/Floyd-cramer-chattanooga-choo-choo-lyrics
Error fetching data for Tuxedo Junction - Chattanooga Choo Choo: Error: No results found for Tuxedo Junction - Chattanooga Choo Choo
Error fetching data for Potliquor - Cheer: Error: No results found for Potliquor - Cheer
Error fetching data for Jerry Murad's Harmonicats - Cherry Pink And Apple Blossom White: Error: No results found for Jerry Murad's Harmonicats - Cherry Pink And Apple Blossom White
Error fetching data for Robert Miles - Children: Error: Could not find lyrics on the page https://genius.com/Robert-miles-children-lyrics
Error fetching data for Kyu Sakamoto - China Nights (Shina No Yoru): Error: No results found for Kyu Sakamoto - China Nights (Shina No Yoru)
Error fetching data for Booker T. & The MG's - Chinese Checkers: Error: Could not find lyrics on the page https://genius.com/Booker-t-and-the-mgs-chinese-checkers-lyrics
Error fetching data for Banzaii - Chinese Kung Fu: Error: No results found for Banzaii - Chinese Kung Fu
Error fetching data for Jack Harlow Featuring Drake - Churchill Downs: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-churchill-downs-8-bit-jack-harlow-and-drake-emulation-lyrics
Error fetching data for Jacky Noguez And His Musette Orchestra - Ciao, Ciao Bambina: Error: No results found for Jacky Noguez And His Musette Orchestra - Ciao, Ciao Bambina
Error fetching data for Billy Vaughn And His Orchestra - Cimarron (Roll On): Error: No results found for Billy Vaughn And His Orchestra - Cimarron (Roll On)
Error fetching data for Esther & Abi Ofarim - Cinderella Rockefella: Error: No results found for Esther & Abi Ofarim - Cinderella Rockefella
Error fetching data for The Meters - Cissy Strut: Error: Could not find lyrics on the page https://genius.com/The-meters-cissy-strut-lyrics
Error fetching data for Mason Williams - Classical Gas: Error: Could not find lyrics on the page https://genius.com/Mason-williams-classical-gas-lyrics
Error fetching data for Jr. Walker & The All Stars - Cleo's Mood: Error: Could not find lyrics on the page https://genius.com/Junior-walker-and-the-all-stars-cleos-mood-lyrics
Error fetching data for Lita Ford (Duet With Ozzy Osbourne) - Close My Eyes Forever: Error: No results found for Lita Ford (Duet With Ozzy Osbourne) - Close My Eyes Forever
Error fetching data for Vanessa Williams - Colors Of The Wind (From "Pocahontas"): Error: No results found for Vanessa Williams - Colors Of The Wind (From "Pocahontas")
Error fetching data for H.E.R. Featuring Chris Brown - Come Through: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-come-through-8-bit-her-and-chris-brown-emulation-lyrics
Error fetching data for Yellow Magic Orchestra - Computer Game "Theme From The Circus": Error: Could not find lyrics on the page https://genius.com/Yellow-magic-orchestra-computer-game-theme-from-the-circus-lyrics
Error fetching data for Ric-A-Che Featuring Darija - Coo-Coo Chee: Error: No results found for Ric-A-Che Featuring Darija - Coo-Coo Chee
Error fetching data for The Kingston Trio - CooCoo-U: Error: No results found for The Kingston Trio - CooCoo-U
Error fetching data for Al Hirt - Cotton Candy: Error: Could not find lyrics on the page https://genius.com/Al-hirt-cotton-candy-lyrics
Error fetching data for Whitney Houston & CeCe Winans - Count On Me (From "Waiting To Exhale"): Error: No results found for Whitney Houston & CeCe Winans - Count On Me (From "Waiting To Exhale")
Error fetching data for The Jets - Cross My Broken Heart (From "Beverly Hills Cop II"): Error: No results found for The Jets - Cross My Broken Heart (From "Beverly Hills Cop II")
Error fetching data for Johnny And The Hurricanes - Crossfire: Error: Could not find lyrics on the page https://genius.com/Johnny-and-the-hurricanes-crossfire-lyrics
Error fetching data for Elvis Presley With The Jordanaires - Crying In The Chapel: Error: No results found for Elvis Presley With The Jordanaires - Crying In The Chapel
Error fetching data for Steve Allen and His Orchestra with The Copacabana Trio - Cuando Calienta El Sol (When The Sun Is Hot): Error: No results found for Steve Allen and His Orchestra with The Copacabana Trio - Cuando Calienta El Sol (When The Sun Is Hot)
Error fetching data for James Walsh Gypsy Band - Cuz It's You, Girl: Error: No results found for James Walsh Gypsy Band - Cuz It's You, Girl
Error fetching data for MC Luscious Featuring Kinsui - Da' Dip: Error: No results found for MC Luscious Featuring Kinsui - Da' Dip
Error fetching data for Jimmy Gilmer And The Fireballs - Daisy Petal Pickin': Error: No results found for Jimmy Gilmer And The Fireballs - Daisy Petal Pickin'
Error fetching data for Pitbull x El Chombo x Karol G Featuring Cutty Ranks - Dame Tu Cosita: Error: No results found for Pitbull x El Chombo x Karol G Featuring Cutty Ranks - Dame Tu Cosita
Error fetching data for Paula Abdul & Randy Jackson - Dance Like There's No Tomorrow: Error: No results found for Paula Abdul & Randy Jackson - Dance Like There's No Tomorrow
Error fetching data for The Bobbettes - Dance With Me Georgie: Error: No results found for The Bobbettes - Dance With Me Georgie
Error fetching data for Cozy Powell - Dance With The Devil: Error: Could not find lyrics on the page https://genius.com/Cozy-powell-dance-with-the-devil-lyrics
Error fetching data for Flash Cadillac And The Continental Kids - Dancin' (On A Saturday Night): Error: No results found for Flash Cadillac And The Continental Kids - Dancin' (On A Saturday Night)
Error fetching data for Teri DeSario With K.C. - Dancin' In The Streets: Error: No results found for Teri DeSario With K.C. - Dancin' In The Streets
Error fetching data for Disco Tex & The Sex-O-Lettes Featuring Sir Monti Rock III - Dancin' Kid: Error: No results found for Disco Tex & The Sex-O-Lettes Featuring Sir Monti Rock III - Dancin' Kid
Error fetching data for Ramsey Lewis - Dancing In The Street: Error: Could not find lyrics on the page https://genius.com/Ramsey-lewis-dancing-in-the-street-lyrics
Error fetching data for The Knockouts - Darling Lorraine: Error: No results found for The Knockouts - Darling Lorraine
Error fetching data for Electric Light Orchestra - Daybreaker: Error: Could not find lyrics on the page https://genius.com/Electric-light-orchestra-daybreaker-lyrics
Error fetching data for Vicki Sue Robinson - Daylight: Error: No results found for Vicki Sue Robinson - Daylight
Error fetching data for Keith Hampshire - Daytime Night-Time: Error: No results found for Keith Hampshire - Daytime Night-Time
Error fetching data for Powersource (Solo...Sharon) - Dear Mr. Jesus: Error: No results found for Powersource (Solo...Sharon) - Dear Mr. Jesus
Error fetching data for Flip Cartridge - Dear Mrs. Applebee: Error: No results found for Flip Cartridge - Dear Mrs. Applebee
Error fetching data for The 5 Stairsteps - Dear Prudence: Error: No results found for The 5 Stairsteps - Dear Prudence
Error fetching data for Mos Def & Kweli Are Black Star - Definition: Error: No results found for Mos Def & Kweli Are Black Star - Definition
Error fetching data for Pop Smoke Featuring Dua Lipa - Demeanor: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-demeanor-8-bit-pop-smoke-and-dua-lipa-emulation-lyrics
Error fetching data for Pat Thomas - Desafinado (Slightly Out Of Tune): Error: No results found for Pat Thomas - Desafinado (Slightly Out Of Tune)
Error fetching data for Stan Getz/Charlie Byrd - Desafinado: Error: Could not find lyrics on the page https://genius.com/Stan-getz-and-charlie-byrd-desafinado-lyrics
Error fetching data for Jose Feliciano - Destiny/Susie-Q: Error: No results found for Jose Feliciano - Destiny/Susie-Q
Error fetching data for Bridgit Mendler, Adam Hicks, Naomi Scott & Hayley Kiyoko - Determinate: Error: No results found for Bridgit Mendler, Adam Hicks, Naomi Scott & Hayley Kiyoko - Determinate
Error fetching data for Pratt & McClain - Devil With A Blue Dress: Error: No results found for Pratt & McClain - Devil With A Blue Dress
Error fetching data for The Ventures - Diamond Head: Error: Could not find lyrics on the page https://genius.com/The-ventures-diamond-head-lyrics
Error fetching data for Tim McGraw With Catherine Dunn - Diamond Rings And Old Barstools: Error: No results found for Tim McGraw With Catherine Dunn - Diamond Rings And Old Barstools
Error fetching data for The Stairsteps - Didn't It Look So Easy: Error: No results found for The Stairsteps - Didn't It Look So Easy
Error fetching data for Sleepy Hallow Featuring 347aidan - Die Young: Error: Could not find lyrics on the page https://genius.com/8-bit-arcade-die-young-8-bit-sleepy-hallow-and-347aidan-emulation-lyrics
Error fetching data for The Adventures Of Stevie V - Dirty Cash (Money Talks): Error: Could not find lyrics on the page https://genius.com/Pawsa-and-the-adventures-of-stevie-v-dirty-cash-money-talks-lyrics
Error fetching data for Rick Dees & His Cast Of Idiots - Dis-Gorilla (Part 1): Error: No results found for Rick Dees & His Cast Of Idiots - Dis-Gorilla (Part 1)
Error fetching data for Wilton Place Street Band - Disco Lucy (i Love Lucy Theme): Error: Could not find lyrics on the page https://genius.com/Wilton-place-street-band-disco-lucy-i-love-lucy-theme-lyrics
Error fetching data for Houston Person - Disco Sax/for The Love Of You: Error: No results found for Houston Person - Disco Sax/for The Love Of You
Error fetching data for Etta James & Sugar Pie DeSanto - Do I Make Myself Clear: Error: No results found for Etta James & Sugar Pie DeSanto - Do I Make Myself Clear
Error fetching data for Freak Nasty Featuring Crazy Mike - Do It Just Like A Rockstar: Error: Could not find lyrics on the page https://genius.com/Freak-nasty-do-it-just-like-a-rockstar-lyrics
Error fetching data for Michael Zager's Moon Band/Peabo Bryson - Do It With Feeling: Error: No results found for Michael Zager's Moon Band/Peabo Bryson - Do It With Feeling
Error fetching data for Elvis Presley With The Jordanaires, Jubilee Four & Carol Lombard Trio - Do The Clam: Error: No results found for Elvis Presley With The Jordanaires, Jubilee Four & Carol Lombard Trio - Do The Clam
Error fetching data for Steve Dahl And Teenage Radiation - Do You Think I'm Disco?: Error: No results found for Steve Dahl And Teenage Radiation - Do You Think I'm Disco?
Error fetching data for Lonnie Donegan And His Skiffle Group - Does Your Chewing Gum Lose It's Flavor (On The Bedpost Over Night): Error: No results found for Lonnie Donegan And His Skiffle Group - Does Your Chewing Gum Lose It's Flavor (On The Bedpost Over Night)
Error fetching data for The Partridge Family Starring Shirley Jones Featuring David Cassidy - Doesn't Somebody Want To Be Wanted: Error: No results found for The Partridge Family Starring Shirley Jones Featuring David Cassidy - Doesn't Somebody Want To Be Wanted
Error fetching data for Heart - Dog + Butterfly: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))

SCRAPE 4: ENDING ON DOIN' THIS (Luke Combs, ROW 512 + 1762 + 505 + 1093 + 2235)

SCRAPE 5: ENDING ON DRINK IN MY HAND (Eric Church, ROW 512 + 1762 + 505 + 1093 + 2235 + 614)

SCRAPE 6: ENDING ON EYES CLOSED (Ed Sheeran, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656)

SCRAPE 7: ENDING ON GETTING AWAY WITH IT (Electronic, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307)

SCRAPE 7: ENDING ON HEAT OF THE MOMENT (Asia, ROW 512 + 1762 + 505 + 1093 + 2235 + 614 + 656 + 1307 + 1371)