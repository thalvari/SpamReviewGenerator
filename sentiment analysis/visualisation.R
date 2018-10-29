library(tidytext)
library(dplyr)
library(stringr)
library(ggplot2)
library(gridExtra)


reviews <- read.csv(file="cleanedagain2.csv")
reviews$text <- as.character(reviews$text)


reviewsbycategory <- reviews %>%
  group_by(category) %>%
  ungroup()

tidy_reviews <- reviewsbycategory %>%
  unnest_tokens(word,text)

data(stop_words)


tidy_reviews <- tidy_reviews %>%
  anti_join(stop_words)

#most common words in each review category
a <- tidy_reviews %>%
  filter(category == "generated cellphone & accessory reviews") %>%
  count(word, sort = T) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n))
  
pa <- ggplot(a, aes(word, n)) + geom_col(fill = 'blue') + coord_flip() + labs(title ="generated cellphone & accessory reviews")

b <- tidy_reviews %>%
  filter(category == "generated hotel reviews") %>%
  count(word, sort = T) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n))

pb <- ggplot(b, aes(word, n)) + geom_col(fill = 'red') + coord_flip() + labs(title = "generated hotel reviews")

c <- tidy_reviews %>%
  filter(category == "generated marvel movie reviews") %>%
  count(word, sort = T) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n)) 
pc <- ggplot(c, aes(word, n)) + geom_col(fill = 'green') + coord_flip() + labs(title = "generated marvel movie reviews")


d <- tidy_reviews %>%
  filter(category == "real hotel reviews") %>%
  count(word, sort = T) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n))

pd <- ggplot(d, aes(word, n)) + geom_col(fill = 'magenta') + coord_flip() + labs(title = "real hotel reviews")


e <- tidy_reviews %>%
  filter(category == "real marvel movie reviews") %>%
  count(word, sort = T) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n))

pe <- ggplot(e, aes(word, n)) + geom_col(fill = 'yellow') + coord_flip() + labs(title = "real marvel movie reviews")


f <- tidy_reviews %>%
  filter(category == "real cellphone & accessories reviews") %>%
  count(word, sort = T) %>%
  top_n(10) %>%
  mutate(word = reorder(word, n))
pf <- ggplot(f, aes(word, n)) + geom_col(fill = 'cyan') + coord_flip() + labs(title = "real cellphone & accessories reviews")

grid.arrange(pa,pf,pb,pd,pc,pe)

#most positive and negative words using bing sentiments

gencellposneg <- tidy_reviews %>%
  filter(category == "generated cellphone & accessory reviews") %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = T) %>%
  ungroup()

a <- gencellposneg %>%
  group_by(sentiment) %>%
  top_n(10) %>%
  ungroup() %>%
  mutate(word = reorder(word,n))

pa <- ggplot(a, aes(word, n, fill=sentiment)) + geom_col() + facet_wrap(~sentiment, scales = "free_y")+ labs(title = "generated cellphone & accessory reviews") + coord_flip()

genhotelposneg <- tidy_reviews %>%
  filter(category == "generated hotel reviews") %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = T) %>%
  ungroup()

b <- genhotelposneg %>%
  group_by(sentiment) %>%
  top_n(10) %>%
  ungroup() %>%
  mutate(word = reorder(word,n))

pb <- ggplot(b, aes(word, n, fill=sentiment)) + geom_col() + facet_wrap(~sentiment, scales = "free_y")+ labs(title = "generated hotel reviews") + coord_flip()


genmarvelposneg <- tidy_reviews %>%
  filter(category == "generated marvel movie reviews") %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = T) %>%
  ungroup()

c <- genmarvelposneg %>%
  group_by(sentiment) %>%
  top_n(10) %>%
  ungroup() %>%
  mutate(word = reorder(word,n))

pc <- ggplot(c, aes(word, n, fill=sentiment)) + geom_col() + facet_wrap(~sentiment, scales = "free_y")+ labs(title = "generated marvel reviews") + coord_flip()


marvelposneg <- tidy_reviews %>%
  filter(category == "real marvel movie reviews") %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = T) %>%
  ungroup()

d <- marvelposneg %>%
  group_by(sentiment) %>%
  top_n(10) %>%
  ungroup() %>%
  mutate(word = reorder(word,n))

pd <- ggplot(d, aes(word, n, fill=sentiment)) + geom_col() + facet_wrap(~sentiment, scales = "free_y")+ labs(title = "real marvel reviews") + coord_flip()


hotelposneg <- tidy_reviews %>%
  filter(category == "real hotel reviews") %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = T) %>%
  ungroup()

e <- hotelposneg %>%
  group_by(sentiment) %>%
  top_n(10) %>%
  ungroup() %>%
  mutate(word = reorder(word,n))

pe <- ggplot(e, aes(word, n, fill=sentiment)) + geom_col() + facet_wrap(~sentiment, scales = "free_y")+ labs(title = "real hotel reviews") + coord_flip()


cellposneg <- tidy_reviews %>%
  filter(category == "real cellphone & accessories reviews") %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = T) %>%
  ungroup()

f <- cellposneg %>%
  group_by(sentiment) %>%
  top_n(10) %>%
  ungroup() %>%
  mutate(word = reorder(word,n))

pf <- ggplot(f, aes(word, n, fill=sentiment)) + geom_col() + facet_wrap(~sentiment, scales = "free_y")+ labs(title = "real cellphone & accessory reviews") + coord_flip()

grid.arrange(pa,pf,pb,pe,pc,pd)

#td_idf for review types

review_words <- reviewsbycategory %>%
  unnest_tokens(word,text) %>%
  count(category, word, sort = T) %>%
  ungroup()

review_words <- review_words %>%
  bind_tf_idf(word, category, n)

review_words %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(category) %>%
  top_n(10) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = category)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf") +
  facet_wrap(~category, ncol = 2, scales = "free") +
  coord_flip()

gencell <- reviewsbycategory %>%
  filter(category == "generated cellphone & accessory reviews") %>%
  unnest_tokens(word,text) %>%
  count(rating, word, sort = T) %>%
  ungroup()

gencell <- gencell %>%
  bind_tf_idf(word, rating, n)

gencell %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(rating) %>%
  top_n(6) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = rating)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf", label = "generated cellphone & accessory reviews") +
  facet_wrap(~rating, ncol = 2, scales = "free") +
  coord_flip()

realcell <- reviewsbycategory %>%
  filter(category == "real cellphone & accessories reviews") %>%
  unnest_tokens(word,text) %>%
  count(rating, word, sort = T) %>%
  ungroup()

realcell <- realcell %>%
  bind_tf_idf(word, rating, n)

realcell %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(rating) %>%
  top_n(6) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = rating)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf") +
  facet_wrap(~rating, ncol = 2, scales = "free") +
  coord_flip()

genhotel <- reviewsbycategory %>%
  filter(category == "generated hotel reviews") %>%
  unnest_tokens(word,text) %>%
  count(rating, word, sort = T) %>%
  ungroup()

genhotel <- genhotel %>%
  bind_tf_idf(word, rating, n)

genhotel %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(rating) %>%
  top_n(6) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = rating)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf") +
  facet_wrap(~rating, ncol = 2, scales = "free") +
  coord_flip()

realhotel <- reviewsbycategory %>%
  filter(category == "real hotel reviews") %>%
  unnest_tokens(word,text) %>%
  count(rating, word, sort = T) %>%
  ungroup()

realhotel <- realhotel %>%
  bind_tf_idf(word, rating, n)

realhotel %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(rating) %>%
  top_n(6) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = rating)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf") +
  facet_wrap(~rating, ncol = 2, scales = "free") +
  coord_flip()

genmarvel <- reviewsbycategory %>%
  filter(category == "generated marvel movie reviews") %>%
  unnest_tokens(word,text) %>%
  count(rating, word, sort = T) %>%
  ungroup()

genmarvel <- genmarvel %>%
  bind_tf_idf(word, rating, n)

genmarvel %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(rating) %>%
  top_n(6) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = rating)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf") +
  facet_wrap(~rating, ncol = 2, scales = "free") +
  coord_flip()

realmarvel <- reviewsbycategory %>%
  filter(category == "real marvel movie reviews") %>%
  unnest_tokens(word,text) %>%
  count(rating, word, sort = T) %>%
  ungroup()

realmarvel <- realmarvel %>%
  bind_tf_idf(word, rating, n)

realmarvel %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>%
  group_by(rating) %>%
  top_n(6) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = rating)) +
  geom_col(show.legend = F) +
  labs(x = NULL, y = "tf_idf") +
  facet_wrap(~rating, ncol = 2, scales = "free") +
  coord_flip()

#sentiment barcharts

marvelneg <- tidy_reviews %>%
  filter(category == "real marvel movie reviews") %>%
  filter(rating < 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

marvelpos <- tidy_reviews %>%
  filter(category == "real marvel movie reviews") %>%
  filter(rating > 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

marvelneg2 <- tidy_reviews %>%
  filter(category == "generated marvel movie reviews") %>%
  filter(rating < 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

marvelpos2 <- tidy_reviews %>%
  filter(category == "generated marvel movie reviews") %>%
  filter(rating > 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

hotelneg <- tidy_reviews %>%
  filter(category == "real hotel reviews") %>%
  filter(rating < 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

hotelpos <- tidy_reviews %>%
  filter(category == "real hotel reviews") %>%
  filter(rating > 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

hotelneg2 <- tidy_reviews %>%
  filter(category == "generated hotel reviews") %>%
  filter(rating < 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

hotelpos2 <- tidy_reviews %>%
  filter(category == "generated hotel reviews") %>%
  filter(rating > 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

cellneg <- tidy_reviews %>%
  filter(category == "real cellphone & accessories reviews") %>%
  filter(rating < 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

cellpos <- tidy_reviews %>%
  filter(category == "real cellphone & accessories reviews") %>%
  filter(rating > 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

cellneg2 <- tidy_reviews %>%
  filter(category == "generated cellphone & accessory reviews") %>%
  filter(rating < 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

cellpos2 <- tidy_reviews %>%
  filter(category == "generated cellphone & accessory reviews") %>%
  filter(rating > 3) %>%
  inner_join(get_sentiments("nrc")) %>%
  count(sentiment, sort = TRUE) %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ungroup()

pa11 <- ggplot(marvelneg, aes(sentiment, n)) + geom_col(fill = 'blue') + coord_flip() + labs(title ="real negative marvel reviews")
pa12 <- ggplot(marvelpos, aes(sentiment, n)) + geom_col(fill = 'blue') + coord_flip() + labs(title ="real positive marvel reviews")
pa21 <- ggplot(marvelneg2, aes(sentiment, n)) + geom_col(fill = 'blue') + coord_flip() + labs(title ="generated negative marvel reviews")
pa22 <- ggplot(marvelpos2, aes(sentiment, n)) + geom_col(fill = 'blue') + coord_flip() + labs(title ="generated positive marvel reviews")
pb11 <- ggplot(hotelneg, aes(sentiment, n)) + geom_col(fill = 'cyan') + coord_flip() + labs(title ="real negative hotel reviews")
pb12 <- ggplot(hotelpos, aes(sentiment, n)) + geom_col(fill = 'cyan') + coord_flip() + labs(title ="real positive hotel reviews")
pb21 <- ggplot(hotelneg2, aes(sentiment, n)) + geom_col(fill = 'cyan') + coord_flip() + labs(title ="generated negative hotel reviews")
pb22 <- ggplot(hotelpos2, aes(sentiment, n)) + geom_col(fill = 'cyan') + coord_flip() + labs(title ="generated positive hotel reviews")
pc11 <- ggplot(cellneg, aes(sentiment, n)) + geom_col(fill = 'lightblue') + coord_flip() + labs(title ="real negative cellphone & accessories reviews")
pc12 <- ggplot(cellpos, aes(sentiment, n)) + geom_col(fill = 'lightblue') + coord_flip() + labs(title ="real positive cellphone & accessories reviews")
pc21 <- ggplot(cellneg2, aes(sentiment, n)) + geom_col(fill = 'lightblue') + coord_flip() + labs(title ="generated negative cellphone & accessories reviews")
pc22 <- ggplot(cellpos2, aes(sentiment, n)) + geom_col(fill = 'lightblue') + coord_flip() + labs(title ="generated positive cellphone & accessories reviews")

grid.arrange(pa11,pa12,pa21,pa22, pb11,pb12,pb21,pb22, pc11,pc12,pc21,pc22, ncol = 4)
