import pandas as pd
import tweepy as twt
import re
from nltk.corpus import stopwords

#Twitter API credentials
consumer_key = "Kq4mCtnOSPiNwA9ArvYq03DE7"
consumer_secret = "aWBfVbrJWppmEy3mAbrjUHa6Y8AKU6qkCBZwA6ZpAO8BEFaoC2"
access_key = "529590041-eZXHHkluorWkdRZRWiVYW3GVBuvr3VXt84cZcDYA"
access_secret = "rqlG8jzmKTPU3bZoCwgRnOUoD5UYOx8KDjhoXySPrR3mI"

all_tweets = [];

def get_all_tweets_fn(screen_name):
    auth = twt.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key,access_secret)    
    api = twt.API(auth)
    new_twts = api.user_timeline(screen_name = screen_name,count=200)
    all_tweets.extend(new_twts)
    
    oldest = all_tweets[-1].id - 1
    while len(new_twts) > 0:
        new_twts = api.user_timeline(screen_name= screen_name,count=200,max_id=oldest)
        all_tweets.extend(new_twts)
        oldest = all_tweets[-1].id - 1
    
    outtweets = [[tweet.created_at,tweet.entities["hashtags"],tweet.entities["user_mentions"],tweet.favorite_count,
                  tweet.geo,tweet.id_str,tweet.lang,tweet.place,tweet.retweet_count,tweet.retweeted,tweet.source,tweet.text,
                  tweet._json["user"]["location"],tweet._json["user"]["name"],tweet._json["user"]["time_zone"],
                  tweet._json["user"]["utc_offset"]] for tweet in all_tweets]
    
    tweets_df = pd.DataFrame(columns = ["time","hashtags","user_mentions","favorite_count",
                                    "geo","id_str","lang","place","retweet_count","retweeted","source",
                                    "text","location","name","time_zone","utc_offset"])
    tweets_df["time"]  = pd.Series([str(i[0]) for i in outtweets])
    tweets_df["hashtags"] = pd.Series([str(i[1]) for i in outtweets])
    tweets_df["user_mentions"] = pd.Series([str(i[2]) for i in outtweets])
    tweets_df["favorite_count"] = pd.Series([str(i[3]) for i in outtweets])
    tweets_df["geo"] = pd.Series([str(i[4]) for i in outtweets])
    tweets_df["id_str"] = pd.Series([str(i[5]) for i in outtweets])
    tweets_df["lang"] = pd.Series([str(i[6]) for i in outtweets])
    tweets_df["place"] = pd.Series([str(i[7]) for i in outtweets])
    tweets_df["retweet_count"] = pd.Series([str(i[8]) for i in outtweets])
    tweets_df["retweeted"] = pd.Series([str(i[9]) for i in outtweets])
    tweets_df["source"] = pd.Series([str(i[10]) for i in outtweets])
    tweets_df["text"] = pd.Series([str(i[11]) for i in outtweets])
    tweets_df["location"] = pd.Series([str(i[12]) for i in outtweets])
    tweets_df["name"] = pd.Series([str(i[13]) for i in outtweets])
    tweets_df["time_zone"] = pd.Series([str(i[14]) for i in outtweets])
    tweets_df["utc_offset"] = pd.Series([str(i[15]) for i in outtweets])
    tweets_df.to_csv(screen_name+"_tweets_mahesh.csv")
    return tweets_df

mahesh_Twiiter = get_all_tweets_fn("urstrulyMahesh")
mahesh_Twiiter.columns
miningData = mahesh_Twiiter.iloc[:,11] #Only considering the Messages
miningData = ''.join(miningData)

miningData_con = re.sub("[^A-Za-z" "]+"," ",miningData).lower() #converting to lowercase
miningData_con = re.sub("[0-9" "]+"," ",miningData_con) #removing Numbers
miningData_con = miningData_con.split(" ")
stop_words=[];
with open('C:/My Files/Excelr/10 - Text Mining/Assignment/stop.txt') as f:stop_words = f.read()
stop_words = stop_words.split("\n")
stop_words = stopwords.words('English') #import stop words from stopwords library
miningData_con = [w for w in miningData_con if not w in stop_words] #remove stopwords
miningData_con_final = " ".join(miningData_con) #join the filtered values

import matplotlib.pyplot as plt
from wordcloud import WordCloud
wordcloud_mb = WordCloud(background_color='black',width=1800,height=1500).generate(miningData_con_final)
plt.imshow(wordcloud_mb)

# from word cloud https co we can remove
remove_words = ['https', 'co']
miningData_con = [w for w in miningData_con if not w in remove_words]
miningData_con_final_2 = " ".join(miningData_con)
wordcloud_mb_2 = WordCloud(background_color='black', width=1800,height=1500).generate(miningData_con_final_2)
plt.imshow(wordcloud_mb_2)

#sentiment Analysis
with open("C:/My Files/Excelr/10 - Text Mining/Assignment/positive-words.txt","r") as pos:poswords = pos.read().split("\n")
with open("C:/My Files/Excelr/10 - Text Mining/Assignment/negative-words.txt","r") as neg:negwords = neg.read().split("\n")

#choosing only words which are in positive words
pos_miningData_con = [i for i in miningData_con if i in poswords]
pos_miningData_con_final = " ".join(pos_miningData_con)
wordcloud_mb_pos = WordCloud(background_color='black',width=1800,height=1500).generate(pos_miningData_con_final)
plt.imshow(wordcloud_mb_pos)

#choosing only words which are in negative words
neg_miningData_con = [i for i in miningData_con if i in negwords]
neg_miningData_con_final = " ".join(neg_miningData_con)
wordcloud_mb_neg = WordCloud(background_color='black',width=1800,height=1500).generate(neg_miningData_con_final)
plt.imshow(wordcloud_mb_neg)
