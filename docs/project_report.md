# Project report

## 1 Introduction

## 2 Data
Our model creator and generator currently support a total of three datasets. The marvel dataset consists of reviews of several Marvel movies scraped from [Rotten Tomatoes](https://www.rottentomatoes.com/) using our own webscraper. The hotel dataset is a [modified](https://data.world/jenka13all/lara-hotel-reviews/workspace/file?filename=7282_with_textcat_languagetags.csv) version of [Datafiniti's](https://data.world/datafiniti/hotel-reviews) hotel review dataset with language tags. The cell dataset is [Julian McAuley's](http://jmcauley.ucsd.edu/data/amazon/) Cell Phones and Accessories -dataset containing Amazon product reviews. The datasets used come with following sentences per rating distributions.

\# sentences| 1 | 2 | 3 | 4 | 5
--- | --- | --- | --- | --- | ---
marvel | 1811 | 5063 | 12634 | 17468 | 10973
hotel | 14529 | 13614 | 22504 | 35053 | 46347
cell | 74276 | 71545 | 134108 | 286311 | 648651

Support for other datasets is can also be implemented with small changes to the code.

## 3 Model creator
To use other models aside from the premade ones already in the repository, for example one with different state size, they have to be manually created using our model creator. The different phases for the pipeline of our model creator are described below.
1. In the 'load and normalize' -phase the dataset designaded by the user is loaded to memory and normalized by dropping unused columns, renaming the columns containing either the review rating or the review text itself and filtering reviews not in English.
1. In the preprocessing phase, only reviews with the rating given by the user are used. Firstly the reviews are lower-cased so that the model treats same words the same way. Then the reviews are processed so that all sentences end with a dot and some of the dots used inside sentences are replaced. Last common non-words such as html-tags are replaced.
1. In the 'to sentences' -phase, the reviews are split to sentences. This is done because the Markov model can only tell us about the relationship of words within sentences.
1. In the 'remove punctuation' -phase, most of the punctuation inside the sentences is removed. This is done so that the generator won't consider lone punctuations as words and won't for example generate a sentence starting with a dash. Only the percent-symbol and stuff like apostrophes and dashes within words are spared. The filtering is done using regex-based character replacement.
1. In the cleaning phase excess whitespaces are removed and useless or empty sentences are removed.
1. In the 'create model' -phase the actual Markov model is created from the sentences given by the previous phase. We use [Markovify](https://github.com/jsvine/markovify) as our Markov chain generator. Markovify allows us to easily create models with different state sizes and is also easily extensible. We chose to extend it with [spaCy's](https://github.com/explosion/spaCy) part-of-speech tagger. This allows us to generate sentences which obey sentence structure better. The following example shows the form in which the sentences are stored to the model.

    ```['it::PRON', 'could::VERB', "n't::ADV", 'be::VERB', 'helped::VERB']```
    
    As we can see the tagger is even able to recognize and seperate the adverb 'not' from base word. 
1. In the last phase the created model is saved to disk in json format. This approach was chosen because the bigger models can take a long time to create, while sentence-generation from a premade model loaded to memory is almost instant. So the user experience provided is quite snappy, but storing all the premade models can take even gigabytes of disk space.

## 4 Generator

## 5 Model statistics

### 5.1 Unique sentences
The following graph shows the number of unique sentences per 10000 generated sentences for different rating 5 models.

![Unique sentences](rating_5_unique.png)

## 6 Data gathering

The data for the project was gathered by using premade datasets such as Amazon product reviews from:
http://jmcauley.ucsd.edu/data/amazon/ and a premade hotel review dataset that consists of TripAdvisor hotel reviews. From the Amazon 
product reviews we used the Cell Phones and Accessories 5-core dataset with 194,439 reviews. 
The movie review dataset was made by web scraping audience reviews from several movies belonging in the Marvel Cinematic Universe from 
Rotten Tomatoes. The scraped reviews were 1000 most recent ones visible on the website. The web scraper was coded for the purposes of this project
and was created using the BeautifulSoup library for python. Originally we attempted to scrape more reviews from TripAdvisor but that proved to
be too diificult after a while of trying to get a web scraper to work on their website.

Other data used in the project consists of generated datasets created using the review generator

## 7 Sentiment analysis of data

The datasets and generated datasets were further used in sentiment analysis of the reviews. In the sentiment analysis the objectives were to find
what words were the most common in each review category, what words were contributing the most to positive and negative sentiments, how much different
sentiments such as negativity and anger were expressed by words in different review categories by negative and positive ratings, calculating tf-idf 
scores for different review categories to find words specific to them and then for each category to calculate tf-idf scores for reviews by ratings.

For the sentiment analysis the data was first processed by lemmatizing all review texts, so that words like movies and movie would be counted as one word
instead of two. This was done by utilising WordNetLemmatizer available in python library nltk. 

The sentiment analysis itself was done using R studio and libaries: tidytext, dplyr, stringr and visualisation by using: ggplot2 and gridExtra. Sentiment 
libraries used were 'bing', which offeres a positive or negative sentiment for each word, and 'nrc', which offers sentiments based on emotions such as anger or joy and
general negative and positive sentiments. Using a combination of tidytext, dplyr and stringr offers an easy way to analyse sentiments in texts.
However the limitations of this model was that the libraris do not recognise negation in sentences as it only analyses words. Thus "not good" will be counted
as positive since it contains the word "good". Other limitations are that the libraries do not take into account the context of a word thus in Marvel reviews
the word "stark" is considered negative even if it is the surname of a character and should be considered neutral.

Visualisation of the sentiment analysis results can be viewed fully in reviewsvisualisation.pdf .

### 7.1 Example graph of sentiment analysis results

In the following graph the first row shows most common words in generated Cell Phone and accessories reviews and in generated hotel reviews and shows the number of times the word is encountered (n). 
The second row shows which words contribute most to negative and positive sentiments in genrated Marvel movie reviews and real hotel reviews and the number of times the word is encountered (n).
The third row shows the sentiments expressed in real negative and positive hotel reviews and how many words in the reviews had such sentiment (n). Then negative reviews are reviews with rating of two or less and positive ones have rating 
above three. 

![Sentiment analysis results](sentimentanalysisvisualisationexample.png)

### 7.2 tf-idf scores of different review categories

The following graph shows tf-idf scores of different review categories.

![tf-idf reviews](tfidfreviews.png)