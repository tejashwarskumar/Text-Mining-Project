library(rtweet)
library(tm)
library(dplyr)

donald_tweets <- search_tweets(q = "@realDonaldTrump", n = 5000,lang = "en",include_rts = FALSE)
head(donald_tweets$text)

library(syuzhet)
s_v <- get_sentences(donald_tweets$text)
class(s_v)
str(s_v)
head(s_v)

sentiment_vector <- get_sentiment(s_v, method = "bing")
head(sentiment_vector)

sum(sentiment_vector)
mean(sentiment_vector)
summary(sentiment_vector)

plot(sentiment_vector, type = "l", main = "Plot Trajectory",xlab = "Narrative Time", ylab = "Emotional Valence")

positive <- s_v[which.max(sentiment_vector)]
positive

negative <- s_v[which.min(sentiment_vector)]
negative

poa_v <- donald_tweets$text
poa_sent <- get_sentiment(poa_v, method="bing")
ft_values <- get_transformed_values(poa_sent, low_pass_size = 3, x_reverse_len = 100, scale_vals = TRUE,scale_range = FALSE)
plot( ft_values, type ="h", main ="Donald using Transformed Values", xlab = "Narrative Time", ylab = "Emotional Valence", col = "red")

nrc_data <- get_nrc_sentiment(s_v)
sad_items <- which(nrc_data$sadness > 0)
head(s_v[sad_items])

barplot(sort(colSums(prop.table(nrc_data[, 1:10]))),horiz = T,cex.names = 0.7,las = 1,main = "Emotions",xlab = "Percentage",col = 1:8)
