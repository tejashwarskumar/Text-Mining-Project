reviews<-readLines(file.choose())
library(syuzhet)
s_v <- get_sentences(reviews)
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

poa_v <- reviews
poa_sent <- get_sentiment(poa_v, method="bing")
ft_values <- get_transformed_values(poa_sent, low_pass_size = 3, x_reverse_len = 100, scale_vals = TRUE,scale_range = FALSE)
plot( ft_values, type ="h", main ="Venom reviews using Transformed Values", xlab = "Narrative Time", ylab = "Emotional Valence", col = "red")

nrc_data <- get_nrc_sentiment(s_v)
positive_items <- which(nrc_data$positive > 0)
head(s_v[positive_items])
barplot(sort(colSums(prop.table(nrc_data[, 1:10]))),horiz = T,cex.names = 0.7,las = 1,main = "Emotions",xlab = "Percentage",col = 1:8)
