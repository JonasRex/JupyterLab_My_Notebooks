import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


def apply_lemmantization_to_df(df):
    """"Call this method to lemmantize and clean the lyrics"""
    df['Lemmantized Lyrics'] = df.apply(lambda row: lemmatized_lyrics(row['Lyrics']), axis=1)
    return df

def lemmatized_lyrics(text):
    tokens = tokenize_lyric(text)
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word=word,pos='v') for word in tokens]
    
    return ' '.join(lemmatized_words)

def tokenize_lyric(text):
    # Remove all unwanted characters. ' , : etc 
    text = scrub_words(text)
    
    # Breaks the text into tokens / single words
    tokens = word_tokenize(text)
    
    # Lowercasing and alphabetical order
    tokens = list(map(str.lower,tokens))
    
    # Some of the scraped lyrics have these descriptions in them. Better remove them to avoid 'noise'
    tokens = [x for x in tokens if x != 'chorus' and x != 'intro' and x != ""]
    
    tokens = remove_stop_words(tokens)
    
    return tokens
    
    
def scrub_words(text):
    """Basic cleaning of texts."""
    
    text = text.replace("\n"," ")

    # Walking, Loving etc
    text = text.replace("in'","ing")
    
    text = text.replace(","," ")
    text = text.replace(":"," ")
    
    # Removes all punctuation sign and numbers.
    text = "".join(re.findall("[a-z A-Z]",text))
    
    return text

def remove_stop_words(tokens):
    extra_words = {"cant","youre","youll","gon","na","wont",
                   "doesnt","ill","im","oh","ohh","ta","wan",
                   "yeah","aingt","ya","way","come","ever","dont",
                   "would","ive","bout","could","yo","em","one"}
    
    # OBS changed this. The real stop words process starts in the next section
    stop_words = set(stopwords.words('english'))
    stop_words = stop_words.union(extra_words)
    return [w for w in tokens if not w in stop_words]

def get_stop_words():
    stop_words = set(stopwords.words('english'))
    return stop_words


# TF-IDF section

def get_topic_values(df, n_components = 6):
    """TF-IDF (term frequency - inverse document frequency)"""
    vectorizer = TfidfVectorizer(stop_words = get_stop_words(), min_df = 0.1 ) # min_df is the minimum frequency
    
    tfidf = vectorizer.fit_transform(df['Lemmantized Lyrics'])

    nmf = NMF(n_components =  n_components)

    topic_values = nmf.fit_transform(tfidf)

    for topic_num, topic in enumerate(nmf.components_):
        message = "Topic #{}: ".format(topic_num + 1)
        message += " ".join([vectorizer.get_feature_names()[i] for i in topic.argsort()[:-11 :-1]])
        print(message)

    return topic_values


def get_topics_before_edit(df, topic_values, topic_labels):
    df_topics = pd.DataFrame(topic_values, columns = topic_labels)
    return df.join(df_topics)

def get_topics_final_data(df, topic_labels):
    # Change to either 0 or 1. So we can plot the data.
    df_lyrics = df.copy() 
    min_value = 0.09
    for label in topic_labels:
        df_lyrics.loc[df_lyrics[label] >= min_value, label] = 1
        df_lyrics.loc[df_lyrics[label] < min_value, label] = 0

    df_lyrics.drop(['Place'], axis = 1, inplace=True) 

    # Group by year
    return df_lyrics.groupby('Year').sum().reset_index()
    

def make_plot(year_topics, topic_labels):
    years = year_topics['Year'].tolist()
    plt.figure(figsize=(20,10))
    for label in topic_labels:
        plt.plot(year_topics['Year'], year_topics[label], label = label, linewidth=7)

    plt.xticks(np.arange(min(years), max(years)+1, 1))
    plt.xlabel('Year',  fontsize=16)
    plt.ylabel('Counts', fontsize=16)
    plt.title('Topic Trend 1989 - 2008', fontsize=25)
    plt.legend(fontsize=20)


def get_genre_count_top10(df_lyrics):
    result = df_lyrics.groupby(['Genre 1']).size().reset_index(name='Counts').sort_values(by=['Counts'],ascending=False).reset_index(drop =True)
    return result[:10]

def get_topic_genre(topic_label, df_lyrics):
    topic = df_lyrics[df_lyrics[topic_label] >= 0.1]
    topic = topic.groupby(['Genre 1']).size().reset_index(name='Counts').sort_values(by=['Counts'],ascending=False).reset_index(drop =True)
    return topic.head()


def make_wordcloud(text):
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    

