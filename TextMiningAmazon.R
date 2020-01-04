pacman::p_load(rvest, dplyr, tidyr, stringr)
url <- paste0("https://www.amazon.in/Test-Exclusive-746/dp/B07DJHXTLJ")
doc <- read_html(url)
prod <- html_nodes(doc, "#productTitle") %>% 
  html_text() %>% 
  gsub("\n", "", .) %>% 
  trimws()
prod

# Function to scrape elements from Amazon reviews
scrape_amazon <- function(url, throttle = 0){
  pacman::p_load(RCurl, XML, dplyr, stringr, rvest, purrr)
  sec = 0
  if(throttle < 0) warning("throttle was less than 0: set to 0")
  if(throttle > 0) sec = max(0, throttle + runif(1, -1, 1))
  doc <- read_html(url)
  title <- doc %>%
    html_nodes("#cm_cr-review_list .a-color-base") %>%
    html_text()
  author <- doc %>%
    html_nodes("#cm_cr-review_list .a-profile-name") %>%
    html_text()
  date <- doc %>%
    html_nodes("#cm_cr-review_list .review-date") %>%
    html_text() %>% 
    gsub(".*on ", "", .)
  review_format <- doc %>% 
    html_nodes(".review-format-strip") %>% 
    html_text() 
  stars <- doc %>%
    html_nodes("#cm_cr-review_list  .review-rating") %>%
    html_text() %>%
    str_extract("\\d") %>%
    as.numeric() 
  comments <- doc %>%
    html_nodes("#cm_cr-review_list .review-text") %>%
    html_text() 
  suppressWarnings(n_helpful <- doc %>%
                     html_nodes(".a-expander-inline-container") %>%
                     html_text() %>%
                     gsub("\n\n \\s*|found this helpful.*", "", .) %>%
                     gsub("One", "1", .) %>%
                     map_chr(~ str_split(string = .x, pattern = " ")[[1]][1]) %>%
                     as.numeric())
  df <- data.frame(title, author, date, review_format, stars, comments, n_helpful, stringsAsFactors = F)
  return(df)
}

pacman::p_load(DT)
url <- "https://www.amazon.in/product-reviews/B07DJHXTLJ"
reviews <- scrape_amazon(url)
head(reviews$comments)

library(syuzhet)
s_v <- get_sentences(reviews$comments)
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

poa_v <- reviews$comments
poa_sent <- get_sentiment(poa_v, method="bing")
ft_values <- get_transformed_values(poa_sent, low_pass_size = 3, x_reverse_len = 100, scale_vals = TRUE,scale_range = FALSE)
plot( ft_values, type ="h", main ="OnePlus7T using Transformed Values", xlab = "Narrative Time", ylab = "Emotional Valence", col = "red")

nrc_data <- get_nrc_sentiment(s_v)
positive_items <- which(nrc_data$positive > 0)
head(s_v[positive_items])
barplot(sort(colSums(prop.table(nrc_data[, 1:10]))),horiz = T,cex.names = 0.7,las = 1,main = "Emotions",xlab = "Percentage",col = 1:8)
