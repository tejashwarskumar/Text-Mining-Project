import requests as rq
from bs4 import BeautifulSoup as bs
import re as re
from nltk.corpus import stopwords

amazon_reviews = [];

for i in range(1,20):
    ip=[];
    url='https://www.amazon.in/OnePlus-Mirror-Grey-128GB-Storage/product-reviews/B07HGBMJT6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(i);
    response = rq.get(url)
    soup = bs(response.content)
    reviews = soup.findAll("span",attrs={"class","a-size-base review-text review-text-content"})# Extracting the content under specific tags  
    for i in range(len(reviews)):
     ip.append(reviews[i].text)  
    amazon_reviews=amazon_reviews+ip

with open("C:/My Files/Excelr/10 - Text Mining/Assignment/amazon_oneplus.txt","w",encoding='utf8') as output:output.write(str(amazon_reviews))

review_string = "".join(amazon_reviews)
review_string_con = re.sub("[^A-Za-z" "]+"," ",review_string).lower() # Removing unwanted symbols incase if exists
review_string_con = re.sub("[0-9" "]+"," ",review_string_con)
review_string_con = review_string_con.split(" ")
stop_words=[];
with open('C:/My Files/Excelr/11 - Text Mining/Assignment/stop.txt') as f:stop_words = f.read()
stop_words = stop_words.split("\n")
stop_words = stopwords.words('English')
review_string_con = [w for w in review_string_con if not w in stop_words]
review_string_final = " ".join(review_string_con)

import matplotlib.pyplot as plt
from wordcloud import WordCloud
wordcloud_am = WordCloud(background_color='black',width=1800,height=1500).generate(review_string_final)
plt.imshow(wordcloud_am)

#remove unique words 
unique_words = ["smartphone","OnePlus","oneplus","7T","Oneplus","phone","camera","display","one","plus","pro","screen","will","battery"]
review_string_con = [i for i in review_string_con if not i in unique_words]
review_string_final_2 = " ".join(review_string_con)
wordcloud_am_2 = WordCloud(background_color='black',width=1800,height=1500).generate(review_string_final_2)
plt.imshow(wordcloud_am_2)

#sentiment Analysis
with open("C:/My Files/Excelr/10 - Text Mining/Assignment/positive-words.txt","r") as pos:poswords = pos.read().split("\n")
with open("C:/My Files/Excelr/10 - Text Mining/Assignment/negative-words.txt","r") as neg:negwords = neg.read().split("\n")
  
#choosing only words which are in positive words
pos_review_string_con = [i for i in review_string_con if i in poswords]
pos_review_string_final = " ".join(pos_review_string_con)
wordcloud_am_pos = WordCloud(background_color='black',width=1800,height=1500).generate(pos_review_string_final)
plt.imshow(wordcloud_am_pos)

#choosing only words which are in negative words
neg_review_string_con = [i for i in review_string_con if i in negwords]
neg_review_string_final = " ".join(neg_review_string_con)
wordcloud_am_neg = WordCloud(background_color='black',width=1800,height=1500).generate(neg_review_string_final)
plt.imshow(wordcloud_am_neg)
