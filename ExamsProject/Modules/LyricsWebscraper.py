import pandas as pd
import bs4
import requests
import re


def load_dataframe():
    file = "data_1989_2008"
    print(file, "Loaded")
    return pd.read_csv(f'data/{file}.csv')

def get_year_from_df(df, year):
    return df[df['Year'] == year].reset_index(drop=True)

def fetch_all_lyrics_from_df(df):
    df['Lyrics'] = df.apply(lambda row: fetch_lyric(row), axis=1)
    
    for index, row in df.iterrows():
        # Only try to save, if not null
        if(row['Lyrics'] != ""):
            save_lyrics(row['Title'], row['Artist'], row['Year'], row['Lyrics'])
    
    return df

def fetch_lyric(row):  
    title = row['Title']
    artist = row['Artist']
    
    return get_lyrics_via_search(title, artist)

def apply_lyrics_to_df(df):
    """Reads the txt files in the data/lyrics folder and Applys them to the dataframe."""
    df['Lyrics'] = df.apply(lambda row: load_lyrics(row), axis=1)
    return df[["Year","Place","Title","Artist","Genre 1","Lyrics"]]

def save_lyrics(title, artist, year, lyrics):
    name = get_storing_name(title, artist)
    try:
        with open(f'data/lyrics/{year}/{name}.txt', 'w') as f:
            f.write(lyrics)
    except FileNotFoundError:
        print("The 'docs' directory does not exist")


def load_lyrics(row):
    text = ""

    year = row['Year']
    title = row['Title']
    artist = row['Artist']

    name = get_storing_name(title, artist)

    try:    
        with open (f'data/lyrics/{year}/{name}.txt', "r") as myfile:
            data = myfile.read().splitlines()
            for line in data:
                if('[' not in line and '(' not in line):
                    #print(line)
                    text += line + '\n'

        return text

    except Exception as e:
        return text

def underscore_title_artist(title, artist):
    return f'{title} {artist}'.replace(" ", "_")

def get_storing_name(title, artist):
    title = check_title(title) # Some title contains '/'
    artist = check_artist(artist)

    # Removes all punctuation sign and numbers.
    title = "".join(re.findall("[a-z A-Z 0-9 -]",title))

    # Removes all punctuation sign and numbers.
    artist = "".join(re.findall("[a-z A-Z 0-9 -]",artist))


    return underscore_title_artist(title, artist)

def fetch_lyrics_year(df, year): 
    df_lyrics = df[df['Year'] == year].reset_index(drop=True)
    df_lyrics = df_lyrics[['Year', 'Place', 'Title', 'Artist', 'Genre 1']]
    
    
    result = fetch_all_lyrics_from_df(df_lyrics)
    print(f'Songs without or too short lyrics in {year}:', result[result['Lyrics'] == ''].shape[0])
    
    return result

def get_lyrics_via_search(title, artist):
    '''Searching for the lyrics via mldb.org. If there is only one clear result'''
    result = ''
    
    title = check_title(title)
    artist = check_artist(artist)

    search_string = f'{title} {artist}'.replace(" ", "+")    
    
    url =  "https://www.mldb.org/search?mq=" + search_string

    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception as e:
        print(e)
        return 'ERROR'
        
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    if(soup.select('.songtext')):
        
        songtext = soup.select('.songtext')
        for line in songtext:
            result += line.text
        
    elif(soup.find(id='thelist')):
        table = soup.find(id='thelist')
        links = table.select('.ft > a')
        link = links[0].get('href')
        result = get_lyrics_via_link(link)
    else:
        if(re.search('\(', title)):
            new_title = title.split('(')
            result = get_lyrics_via_search(new_title[0], artist)
    
    # Some lyrics are incomplete. One song was only one verse. http://www.mldb.org/song-233265-when-i-look-into-your-eyes.html
    if(len(result) <= 500):
        result = ""
    
    return result
    
    
def get_lyrics_via_link(link):                   
    result = ''

    try:
        r = requests.get('https://www.mldb.org/'+link)
        r.raise_for_status()
    except Exception as e:
        print(e)
        return 'ERROR'
        
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    
    if(soup.select('.songtext')):
        
        songtext = soup.select('.songtext')
        
        for line in songtext:
            result += line.text
            
    return result

def check_title(title):
    # Some titles contains '/' because the song might have two titles. Can't search those titles, so we have to split
    # and only search on the first. Two songs is called '7/11' and '24/7' if we change the '/' to '%2F' it should still work.
    if(title == '7/11' or title == '24/7'):
        title = title.replace("/","%2F")

    elif('" /' in title):
        splitted = title.split('" /')
        title = splitted[0]

    elif('"/' in title):
        splitted = title.split('" /')
        title = splitted[0]

    elif('/' in title):
        splitted = title.split('/')
        title = splitted[0]

    # Remove tuples
    if("(" in title):
        splitted = title.split('(')
        title = splitted[0]
    
    title = title.replace("??","e")
    title = title.replace("??","y")
    

    
    return title.lower()

def check_artist(artist):
    
    artist = artist.replace("??","e")
    artist = artist.replace("??","y")
    
    return artist.lower()

def remove_line_breaks(text):
    splitted = [x for x in text.split('\n') if '[' not in x ]
    return ' '.join(splitted)


# Load / Save

def save_as_csv(df, name):
    df.to_csv ('data/lyrics/dataframes/' + name + '.csv', index = False, header=True)
    return name +".csv Saved!"

def load_from_csv(name):
    return pd.read_csv('data/lyrics/dataframes/' + name + '.csv')