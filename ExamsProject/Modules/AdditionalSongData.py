import bs4
import requests
import re
import pandas as pd



# Fetching the data for the whole Billboard Dataframe.

def get_all_additional_data(dataframe):
    new_dict = dict()
    
    # Can't use NaN link. Breaks the build
    df = pd.DataFrame(dataframe['Title_url'].fillna(""))
    
    for index, row in df.iterrows():
        data = get_additional_song_data(row['Title_url'])
        
        # Testing. Want to be able to find out where it goes wrong
        print('Fetcing:',row['Title_url'])
        
        new_dict[index] = data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]

    new_df = convert_additional_data_into_df(new_dict)

    return merge_dataframes(dataframe, new_df)


def convert_additional_data_into_df(song_data):
    data_list = []
    #for index, value in song_data.items():
    for index , data in song_data.items():
        list_song = [data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]]
        data_list.append(list_song)
    return pd.DataFrame(data_list, columns= ['Released', 'Genre 1' ,'Genre 2', 'Genre 3', 'Length', 'Label', 'Total Labels', 'Writer 1', 'Writer 2', 'Youtube'] )
   

def merge_dataframes(left, right):
    return pd.merge(left , right, left_index=True, right_index=True)




# Everything to do with fetching just one song

def get_additional_song_data(link):
    #result_dict = dict()
    
    
    #print("==================")
    #print(link)
    #print("==================")

    
    # All the data we want to extract (Will convert it into an Object!)
    released = ""
    genres = ["","",""]
    length = ""
    label = ""
    total_labels = ""
    writer = ["",""]
    youtube = ""
    
    if(link != ''):
    
        url = "https://en.wikipedia.org"+link

        try:
            r = requests.get(url)
            r.raise_for_status()
        except Exception as e:
            print(e)
            return ["ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"]
        
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        # Some songs have more than one infobox. We only want the first.
        if(soup.select('.infobox')):
            infobox = soup.select('.infobox')
            table = infobox[0].select('tbody > tr')


            for el in table:


                if(el.find('th')):
                    th = el.select('th')
                    td = el.select('td')
                    if(len(td) > 0):
                        #print(th[0].text, td[0].text)
                        match th[0].text:
                            case "Released":
                                released =  extract_released_year(td[0])
                                #print("Released", extract_released_year(td[0]))
                            case "Genre":
                                genres = extract_genre(td[0])
                                #print("Genre:", extract_genre(td[0]))
                            case "Length":
                                length = extract_length(td[0])
                                #print("Length", extract_length(td[0]))
                            case "Label":
                                label_data = extract_label(td[0])
                                label = label_data[0]
                                total_labels = label_data[1]
                                #print("Label", extract_label(td[0]))
                            case "Songwriter(s)":
                                writer = extract_songwriter(td[0])
                                #print("Songwriter(s)", extract_songwriter(td[0]))

                # Search for YT link
                if(el.find('a', {'title': 'YouTube'})):
                    youtube = el.find('a', {'class': 'external'}).get('href')
                    #print(el.find('a', {'class': 'external'}).get('href'))


    # Make sure the lists have the correct size. NaN will be handle when converted to df.
    if(len(genres) < 3 ):
        genres.append('')
        genres.append('')
    if(len(writer) < 2):
        writer.append('')
                
    return [released, genres[0], genres[1], genres[2], length, label, total_labels, writer[0], writer[1], youtube]
    
    

def extract_released_year(element):
    """This function will return the year the song was released. But tests shows that is different scenarios. 
    1. Multiple release days, release etc., 
    2. Sometimes only the Year and Month(or Just the year), 
    
    I am using regex and split to make a list of 4 digit numbers and only returns index 0(Incase there was a rerelease later)
    """    
    text = element.text
    
    result_list = re.findall("\d{4}", text)
    
    
    #print("Extracted released year!")
    
    return(min(result_list))
    
    #years_reg = re.compile(r"\b(19|20)\d{2}\b")
        
    #return [year for year in element.text.split() if re.search(years_reg, year)][0]
    
                        
def extract_genre(element):
    """This function will return a list of up to 3 genres. But tests shows that is different scenarios. 
    1. Only one Genre, 
    2. Multiple genres in an unordered list(ul), 
    3. Multiple genres with a bookmark like this. Pop[1], Rock[2].
    
    Which is handle but simple if statements.
    """
    letters_reg = re.compile(r"[a-zA-Z]")
        

    if(element.find('a')):
        result_list = [x.text for x in element.select('a')]
    else:
        result_list = element.text.split()
    
    
    #print("Extracted genres!")
    
    return [genre.capitalize() for genre in result_list if re.search(letters_reg, genre)][:3]
    
    
def extract_length(element):
    """This function will return the length of the song. In some cases there is a single and an album version etc.,
    but i decided to return just the longest version. 
    1. The function splits the text elements into a list if it contains ':'.
    2. It cleans up the result for any letters or symbols(not ':' obviously).
    3. Return the max value."""

    result_list = []
    
    if(element.find('li')):
        lengths = [x.text for x in element.select('li')]
    else:
        lengths = [x for x in element.text.split() if ":" in x]
        
    for item in lengths:
        if(item != ""):
            split_time = item.split(':')
            minutes = split_time[0]
            seconds = split_time[1][:2] # Only 2 digits
            time = "".join([char for char in minutes+':'+seconds if int(char.isnumeric()) or char == ":"])
            result_list.append(time)    

        
    return max(result_list)
    
def extract_label(element):
    """This function will return only the first mentioned Label. Some singers/song change labels for whatever reason.
    Sometimes up tp two or three times. For simplicity I only return the first mentioned and the amount of different
    labels that the song have had. Maybe we can use that information for something interresting."""
    
    if(element.find('a')):
        result_list = [x.text for x in element.select('a')]
    elif(element.find('li')):
        result_list = [x.text for x in element.select('li')]
    else:
        result_list = element.text.split()
    
    
    #print("Extracted Labels!")
    
    # Returning originale label and the amount of different labels.
    return [[label for label in result_list][0], len(result_list)]

def extract_songwriter(element):
    """This function will return only the first mentioned songwriter. Some singers/song change labels for whatever reason.
    Sometimes up tp two or three times. For simplicity I only return the first mentioned and the amount of different
    labels that the song have had. Maybe we can use that information for something interresting."""
    
    result_list = []
    #list_of_writers = []
    
    #print(element)
    
    if(element.select('li')):
        result_list = [x.text for x in element.select('li')]
    elif(element.select('a')):
        result_list = [x.text for x in element.select('a')]
    else:
        result_list = [x.text for x in element if '<br' not in str(x)]

    
    #if(len(list_of_writers) > 0):
    #    for x in list_of_writers:
    #        if(x.find('a')):
    #            result_list.append(x.find('a').text)
    #            print("Also here")
    #        else:
    #            writer = x.text
    #            if(writer != '1'):
    #                result_list.append(writer)

                    
    #print(result_list)


    
    # Mighht still need this!!
    # Sometimes the songwriters are listed a bit weird. Ends up with: '[4]'.
    #for w in result_list[:2]:
    #    if(re.search('\[|,', str(w)) or w == ""):
            #result_list = [ x for x in element.text.split(', ')]
            #result_list = [ x for x in re.split(' & |, |,|\n',element.text) if x != ""]
    

    
    result_list = [writer[:-3] if re.search('\[', str(writer)) else writer for writer in result_list]
    result_list = [x for x in result_list if x != "" and x != '1'][:2]
    
     # Change ', Jr.' to ' Jr.' and ', Sr.' to ' Sr.':
    result_list = [ x[:-5]+x[-4:] if re.search(', Jr.|, Sr.', str(x)) else x for x in result_list]
    
    

            
    result_list = split_comma_separated_names(result_list)
    
    # Need to add a blank spot if there is only one writer.
    if(len(result_list) < 2):
        result_list.append("")
    
    #print(result_list[:2])
    
    return result_list

def split_comma_separated_names(names):
    new_list = []
    
    for name in names:
        if(', ' in name):
            splitted_names = [x for x in name.split(', ')]
            for s in splitted_names:
                new_list.append(s)
        else:
            new_list.append(name)
    return new_list




# Loading / Saving

def save_as_csv(df, name):
    df.to_csv ('data/' + name + '.csv', index = False, header=True)
    return name +".csv Saved!"

def load_from_csv(name):
    return pd.read_csv('data/' + name + '.csv')