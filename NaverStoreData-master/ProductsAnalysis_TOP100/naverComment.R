library(ggplot2)

setwd("C:\\Users\\acorn\\Documents\\acornproject")
baby_data <- read.csv("baby_data.csv", header = T, quote = ",")
beauty_data <- read.csv("beauty_data.csv", header = T, quote = ",")
digital_data <- read.csv("digital_data.csv", header = T, quote = ",")
fashion_a_data <- read.csv("fashion_a_data.csv", header = T, quote = ",")
fashion_c_data <- read.csv("fashion_c_data.csv", header = T, quote = ",")
food_data <- read.csv("food_data.csv", header = T, quote = ",")
health_data <- read.csv("health_data.csv", header = T, quote = ",")
living_data <- read.csv("living_data.csv", header = T, quote = ",")
sports_data <- read.csv("sports_data.csv", header = T, quote = ",")

comment_data <- rbind(baby_data, beauty_data, digital_data, fashion_a_data, fashion_c_data, food_data, health_data, living_data, sports_data)

write.csv(comment_data, file="C:\\Users\\acorn\\Documents\\acornproject\\comment_data.csv", row.names = FALSE, quote = FALSE)

comment_nouns <- read.csv("comment_nouns.csv", header = T, stringsAsFactors = F, fileEncoding = "UTF-8")
top30 <- comment_nouns %>% arrange(desc(빈도수합계)) %>% head(30)
top30
order <- arrange(top30, 빈도수합계)$단어
ggplot(data=top30, aes(x=단어, y=빈도수합계, fill=단어)) +
  ylim(0,75000) +
  geom_col() +
  coord_flip() +
  scale_x_discrete(limit = order) + 
  geom_text(aes(label=빈도수합계), hjust=-0.3)
  
