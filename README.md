## Facebook NLP Project
#### The Research Question
###### The goal of this project is to use natural language processing (NLP) to score the sentiment for posts on the [National Geographic Facebook Page](https://www.facebook.com/natgeo), and use this feature along with other information about each post to predict its popularity.

###### There are a few interesting applications for this project: a Facebook group admin could use this model to choose between publishing multiple posts (by comparing the popularity of one pending post to another), or a competing Facebook groups could run the model on the competitor’s content, and try to create content that competes for popularity with the other group's posts.

#### Data Collection
###### In order to obtain the text for each post, as well as the relevant metrics for popularity (number of likes, number of comments, number of shares), I used Kevin Zuniga's library to scrape public facebook pages without an API key [2] , and retreived the first 100 pages worth of posts from the National Geographic Facebook Page to use as a training set. 

###### Running getPosts.py stores the scraped data in a file called 'raw_train_df.csv' under the /data folder

#### Data Preprocessing
###### I applied several preprocessing/normalizing steps to each post in the raw dataframe [1]: removing punctuation, expanding contractions, replacing numbers with text. Lemmatizing can be performed, but might hurt the performance of the AFinn Sentiment Lexicon used later to score the sentiment of each individual post.

#### Exploratory Data Analysis
###### After all the posts were normalized, they were scored using the AFinn Sentiment Lexicon. However, I created an *overall score* that takes the mention of animals into account. To do this, I created a lexicon of animal names by scraping a [webpage](https://a-z-animals.com/animals/) listing common animals. Any neutral or already positive Facebook posts that also mentioned animals were assigned additional points, and any already negative Facebook posts that also mentioned animals were docked additional points. This is based on my assumption that a post with an already negative sentiment (i.e. I hate something) would be even more negative if they also mentioned animals (i.e. I hate small kittens).

###### With scoring out of the way, how to measure popularity? Likes sound good, but they are unreliable because they do not account for the full range of reacts on Facebook posts (like, love, haha, wow, sad, angry): a post with 1,000 like and 9,000 love reacts is in reality more popular than a post with 5,000 like and 1,000 love reacts. 

###### Therefore, I will use the number of shares as a measure of popularity.

###### Interactive Plotly Diagrams can be viewed on the [project section of my webpage](https://www.derekoconn.com/projects/predicting-facebook-post-popularity).

###### Currently, there seems to be a small inverse relationship between the score and the distribution of shares. A preliminary boxplot indicates that Facebook posts with negative sentiment (score < -1.0) get more shares than relatively neutral sentiment (-1.0 ≤ score ≤ 1.0), which get more shares than posts with positive sentiment (score > 1.0).

![boxplot image](https://github.com/merillium/Facebook-NLP-Project/blob/master/images/boxplot_score_shares.png)

###### However, the trend changes when looking at the *overall score*: Facebook posts with relatively neutral scores (-1.0 ≤ score ≤ 1.0) are shared less than Facebook posts with negative (score < -1.0) or positive (score > -1.0) overall scores. This is more in line with what we would expect intuitively, but we also need to be careful about remaining unbiased in our analysis. 
![boxplot image](https://github.com/merillium/Facebook-NLP-Project/blob/master/images/boxplot_overall_score_shares.png)

##### *Work in progress, check back for updates!*

##### This project was made possible by all of the helpful NLP resources out there!
###### [1] DJ Sarkar's article: [**A Practitioner's Guide to Natural Language Processing (Part I) — Processing & Understanding Text**](https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72) 
###### [2] Kevin Zuniga's respository and library: [Facebook Scraper](https://github.com/kevinzg/facebook-scraper)
##### [3] An encyclopedic resource for animal names/information: [A-Z Animals](https://a-z-animals.com/animals/)
