## Facebook NLP Project
#### The Research Question
###### The goal of this project is to use natural language processing (NLP) to score the sentiment for posts on the [National Geographic Facebook Page](https://www.facebook.com/natgeo), and use this feature along with other information about each post to predict its popularity.

###### There are a few interesting applications for this project: a Facebook group admin could use this model to choose between publishing multiple posts (by comparing the popularity of one pending post to another), or a competing Facebook groups could run the model on the competitor’s content, and try to create content that competes for popularity with the other group's posts.

#### Data Collection
###### In order to obtain the text for each post, as well as the relevant metrics for popularity (number of likes, number of comments, number of shares), I used Kevin Zuniga's library to scrape public facebook pages without an API key [2] , and retreived the first 100 pages worth of posts from the National Geographic Facebook Page to use as a training set. 

###### Running getPosts.py stores the scraped data in a file called 'raw_train_df.csv' under the /data folder

#### Data Preprocessing
###### I applied several preprocessing/normalizing steps to each post in the raw dataframe [1]: removing punctuation, expanding contractions, replacing numbers with text. Lemmatizing can be performed, but might hurt the performance of the AFinn Sentiment Lexicon used later to score the sentiment of each individual post.

#### Data Analysis
###### After all the posts were normalized, they were scored using the AFinn Sentiment Lexicon. The goal is to determine what relationship exists between the scores of each post and its popularity. Based on the scraped data, (number of likes, number of comments, and number of shares) are the measures of popularity, but since *only* likes could be extracted and not the full range of possible reactions (like, love, haha, sad, angry, wow), then using likes to measure popularity could be misleading (i.e. a post with 1000 like reacts and 5000 love reacts would be more popular than a post with 2000 like reacts and 1000 love reacts, but the number of likes alone would not reflect this).

###### Therefore, I will use the number of shares as a measure of popularity.

#### Metrics
###### Work in progress, check back for updates! 

##### This project was made possible by all of the helpful NLP resources out there!
###### [1] DJ Sarkar's article: [**A Practitioner's Guide to Natural Language Processing (Part I) — Processing & Understanding Text**](https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72) 
###### [2] Kevin Zuniga's respository and library: [Facebook Scraper](https://github.com/kevinzg/facebook-scraper)
