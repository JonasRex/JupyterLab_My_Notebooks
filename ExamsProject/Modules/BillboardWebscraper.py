import bs4
import requests
import pandas as pd

# Fetch one page (1 year)

def get_top100_song_year(year=2021):
    """This function will return a dictionary with any of the official Billboard American top 100 end of the year lists.
    The top 100 list was introduced in 1959. Before that it was a top 50 only. Returns by default 2021.
    link: https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2021"""
    result_dict = dict()
    
    url = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_" + str(year)
    
    r = requests.get(url)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    
    table = soup.select('.wikitable > tbody > tr')
    
    for el in table:
        td = el.select('td')
        if(len(td) > 0):
            number = td[0].text.rstrip('\n')
            title = td[1].text.rstrip('\n')
            artist = extract_artists(td[2])
            title_url = extract_title_url(td[1])
            result_dict[number] = [title[1:-1], artist[0], artist[1], title_url]
    
    return result_dict
    

def extract_artists(element):
    """This function will return a list of the artists that have made the song. Only 2 artists will be applied,
    if more than two artists have collaborated. 
    """
    list_of_artists = [x.text.rstrip('\n') for x in element]
            
    result_list = split_featuring(list_of_artists)  
    
    # Need to add a blank spot if there is no featuring artist.
    if(len(result_list) < 2):
        result_list.append("")
        
    # Some featurings starts with ' & ' and some ends with 'and'. Quick fix:
    if(' and ' in result_list[1][-5:]):
        result_list[1] = result_list[1][:-5]
    if(' & ' in result_list[1][:3]):
        result_list[1] = result_list[1][3:]
        
    return [artist for artist in result_list][:2]


def split_featuring(list):
        """Many of the songs have featuring artists, sometimes even an additional ' and ' artist.
        This function splits them and returns a new list.
        
        Examples:
        1. Blackstreet featuring Mýa, Mase and Blinky Blink   # featuring + and + ,
        2. Silk Sonic (Bruno Mars and Anderson .Paak)         # Tuples
        3. SpotemGottem featuring Pooh Shiesty or DaBaby      # featuring + or
        4. Gerry and the Pacemakers                           # ' and the ' was a common band name in the old days
        5. Puff Daddy & the Family featuring The Notorious B.I.G.  # & the Family.. Gave some troubles.. 
        """
        
        new_list = []
        
        ## TODO: Refactor this code. With all the stuff I learned in the next part!
        
        for artist in list:
            if(' featuring ' in artist):
                [new_list.append(x) for x in artist.split(' featuring ')]
            elif(' and ' in artist and ' and the ' and 'Tones and I' and 'Monsters and Men' not in artist ):
                [new_list.append(x) for x in artist.split(' and ')]
            elif(' or ' in artist and 'Do or Die' not in artist):
                [new_list.append(x) for x in artist.split(' or ')] 
            else:
                new_list.append(artist)
                
        return [x for x in new_list if
                x != ' and ' and x != '' and x != ' (' and x != ')' and 
                x != ', ' and x != ' & 'and x != ' with ' and x != ' & the Family']
            

def extract_title_url(element):
    """This function will return the url for the song. This will be used later on to extract more data about each song."""
    
    if(element.find('a')):
        return element.select('a')[0].get('href')
    else:
        return ""

# Get a specific period:

def get_all_top100_song_period(start=1959, end=2021):
    """This function will return..."""
    result_dict = dict()
    for i in range(start, end + 1):
        result_dict[i] = get_top100_song_year(i)
    
    return make_data_into_dataframe(result_dict)

# Loading/Saving as a Dataframe

def make_data_into_dataframe(billboard_data):
    data_list = []
    for year, value in billboard_data.items():
        for place, song in value.items():
            list_song = [year, place, song[0], song[1], song[2], song[3]]
            data_list.append(list_song)
    return pd.DataFrame(data_list, columns=['Year', 'Place', 'Title', 'Artist', 'Featuring','Title_url'])

def save_billboard_raw_data(data, save_as):
    file = make_data_into_dataframe(data)
    file.to_csv ('data/'+save_as, index = False, header=True)


def load_billboard_raw_data(name):
    return pd.read_csv('data/'+name)


# Different masks

def find_title(df, name):
    return df[df['Title'] == name]

def find_artist(df, name):
    return df[df['Artist'] == name]

def find_featuring(df, name):
    return df[df['Featuring'] == name]

def find_year(df, year):
    return df[df['Year'] == year]

def find_place(df, place):
    return df[df['Place'] == place]