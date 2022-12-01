import pandas as pd
import csv


def make_list_of_all_people(df):
    artist = df['Artist'].dropna().tolist()
    featuring = df['Featuring'].dropna().tolist()
    writer1 = df['Writer 1'].dropna().tolist()
    writer2 = df['Writer 2'].dropna().tolist()
    all_people = [*artist, *featuring, *writer1, *writer2 ]
    
    return sorted(set(all_people))


# Find out if the person is listed under a shorter name. Like "John Johnsen Jr." is the same as "John Johnson" 

def find_list_of_interesting_pairs(all_people):
    interesting_pairs = []

    for x in all_people:
        for y in all_people:
            if(x in y and x != y):
                interesting_pairs.append([x,y])

    return interesting_pairs        


def scan_interesting_pairs(list):
    interesting_pairs = list
    ignoring_list = load_ignoring_list()
    approved_list = load_approved_list()
    
    
    for x in interesting_pairs.copy():
        if(x in ignoring_list):
            interesting_pairs.remove(x)
        elif(x in approved_list):
            interesting_pairs.remove(x)
        elif(x[0] == 'Brown'  or x[0] == 'Baby' or x[0] == 'Ahmad' or x[0] == 'Joe' or x[0] == 'Evan' or x[0] == 'Lloyd'):
            interesting_pairs.remove(x)
    
    return interesting_pairs


def manually_check_pairs(list):
    interesting_pairs = scan_interesting_pairs(list)
    ignoring_list = load_ignoring_list()
    approved_list = load_approved_list()

    print("Interesting pairs:",len(interesting_pairs))
    print("Approved Words list:",len(approved_list))
    print("Ignored Words list:",len(ignoring_list))

    print('y = yes, n = no, m = maybe')

    for pair in interesting_pairs.copy(): # Can't remove from the same list as we are iterating. So we make a copy
        answer = input(f'Is: {pair[0]} the same as: {pair[1]}?')
        if(answer.lower() == 'y'):
            approved_list.append(pair)
            interesting_pairs.remove(pair)
        elif(answer.lower() == 'n'):
            ignoring_list.append(pair)
            interesting_pairs.remove(pair) 
        elif(answer.lower() == 'm'):
            print('Maybe. Not implemented yet')
        else:
            print('Wrong input')
    
    # Suppose to save! But won't do that in the testing phase.

    return "OBS: List is not saved. Change the code!"


def manually_add_to_approved():
    approved_list = load_approved_list()

    keyword = input('Keyword to look for ?')
    replacement = input(f'Replace {keyword} with ?')

    entry = [replacement, keyword]
    answer = input(f'Save {entry} ? (y/n)')
    if(answer.lower() == 'y'):
        approved_list.append(entry)

    save_approved_list(approved_list)

    return "Added!"

# Approved list / Ignoring list

def load_approved_list():
    with open('data/similar/approved_list.csv', 'r') as f: 
        return list(csv.reader(f))[1:] # Skip header

def load_ignoring_list():
    with open('data/similar/ignoring_list.csv', 'r') as f: 
        return list(csv.reader(f))[1:] # Skip header

def save_approved_list(list):
    df = pd.DataFrame(list,columns=['Replacement','Key Word'])
    df.to_csv('data/similar/approved_list.csv', index = False, header=True)
    
def save_ignoring_list(list):
    df = pd.DataFrame(list,columns=['Replacement','Key Word'])
    df.to_csv('data/similar/ignoring_list.csv', index = False, header=True)


# Convert from song to artist data

def convert_artist_data_into_df(artists_list, df):
    approved_list = load_approved_list()


    data_list = []
    for name in artists_list:
        
        # Might be two names associated with a group. Like Sonny & Cher. They should both individually get credits.
        actual_name = check_approved_list(approved_list, name)
        
        
        main_artist = len(df[df['Artist'] == name])
        featuring_artist = len(df[df['Featuring'] == name])
        writer = len(df[df['Writer 1'] == name]) + len(df[df['Writer 2'] == name])
        
        for x in actual_name:
            data_list.append([x, main_artist, featuring_artist, writer])
    
    # groupby will merge the duplicates. So each artists only have one line, with all their accreditations
    new_df = pd.DataFrame(data_list, columns= ['Name', 'Main Artist' ,'Featuring Artist', 'Writer'] ) 
    return new_df.groupby(['Name']).sum().reset_index()


def check_approved_list(approved_list, name):
    name_list = [x[0] for x in approved_list if name == x[1]]
        
    if(len(name_list) == 0):
        name_list = [name]
            
    return name_list


# Save / Load

def save_as_csv(df, name):
    df.to_csv ('data/artists/' + name + '.csv', index = False, header=True)
    return name +".csv Saved!"

def load_from_csv(name):
    return pd.read_csv('data/artists/' + name + '.csv')