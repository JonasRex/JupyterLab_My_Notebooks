# Music / Lyric analyzer
## Python / Machine learning Project  4. Semester

## Idea:
My project is about music and lyrics from the past 30 something years (1989-2021). First I build some webscraping software, that provided me with all the necessary data i needed for my project, including the original lyrics for each song(if they were available). I am using the official Billboard top 100 list, which started in 1959 and seems to be the most comprehensive list available online. (See description of Billboard further down).

### Part 1 (Scraping):
I wanted 99 % of my data to come from web scraping and NOT from datasets/csv-files that's already out there. I used the BeautifulSoup library.
1. Fetching all the lists via: https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2021 (Just change the 4 last digits)
2. 99% of the songs have a url which leads to a page with additional data: Released Date, Length, Genres, Label, Songwriter, Youtube Link. I scraped all of that aswell.
3. The final part of my project is about the lyrics of all these songs. I made a webscraper that fetches the lyrics from  https://www.mldb.org/. They did'nt have any bot detection technology. Which some of the other sites (With more lyrics available) had. mldb.org didnt have much of the lyrics from 2009 and forwarded. So I decided to focus on 1989 - 2008 (20 years). Approx. 70 % songs was available in that periode.  

### Part 2 (Artists): 
Turned the scraped data into Pandas dataframes.
- Tried to find trends and tendencies over the years and made some graphical representations of it:
    - Who's the greatest bands/artists of all time
    - Bar plot with the big names
- Made MeanShift Clustering of the Dataset. With elbow and silhouette plots.


### Part 3 (Lyrics):
Topic analyzed all the lyrics. Tried to divide it into 6 different topics. Music/Lyrics is a bit different from traditional litterature, so It's not 100 % accurate. But i tried to play a few of the songs after and i could hear the specific topics in some.
Topic analyzes needs a lot of tweaking and if I had more time, I might have comed up with a even better result.
- Clustered the Textual Data like we did in the class exercise 09, with the 'RELIGION_abstracts.csv' file.  
    - Lemmatization the data
    - TF-IDF Vectorization
    - Applyed DBSCAN Clustering on the data
    - Made a conclusion on the result.
- Used wordcloud to present a song from each topic. (The ones with the highest compatible score).

### Technologies
- Pandas
- Numpy
- BeautifulSoup
- NLTK
- sklearn.cluster (MeanShift)
- Keras / Tensorflow
- matplotlib.pyplot

### What is Billboard Top 100
The Billboard Hot 100 is a chart that ranks the best-performing singles of the United States. Its data, published by Billboard magazine and compiled by Nielsen SoundScan, is based collectively on each single's weekly physical and digital sales, as well as airplay and streaming. At the end of a year, Billboard will publish an annual list of the 100 most successful songs throughout that year on the Hot 100 chart based on the information.


## Running the project.
You'll need a jupyter Notebook to use the project. Fork the folder into your own Notebook. It consist of 5 .ipynb files and 4 folders. Data, Modules, Notes, Pictures.

#### Order of pages: 
1. Presentation
2. Artists
3. Clustering Artists
4. Lyrics
5. Lyrics Topic Analyze

## Need to install:
yellowbrick is needed for the SilhouetteVisualizer in the lyrics parts:
`pip install yellowbrick`

# List of Challenges
- Scraping all the data from 1959-2021 from wikipedia, was a big challenge. And i ended up not using most of it.. But it gave me some valuable skills for the future
- Would have used selenium instead of beautifulSoup, if i could change it.  


# List of Highlights
- I scraped all of the data myself
- Learned so much from the Topic analyze part. Definitely something I'll work more with in the near future.
- Fetching all the lyrics and saved them into indiviuel txt files. Then made a function that could load them into a pandas dataframe with ease.

# Status
I am done, but could easily have expanded the project if i had the time. I wanted to some more graphical presentation. So I am afraid it's a little heavy on the data side.
I also wanted to spend more time on the Python Modules i build. Make them CLI executable and better documentation. There is some documentation, but not for everything.
But i made a lot of notes and testing over the time of the projects. (See the 'Notes' folder).