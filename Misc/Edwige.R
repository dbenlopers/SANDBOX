library(ggplot2)
library(magrittr)
library(dplyr)
library(reshape2)

df = read.csv("/home/akopp/Documents/Edwige/DATA/Edwige FISH TJ0-J2-Edwige analyse V2.csv")


ggplot() + geom_density(data = filter(df, Well %in% c("F7", "F8", "F9")),
                        aes(SpotFiberCountCh3),
                        color = 'red') +
  geom_density(data = filter(df, Well %in% c("F4", "F5", "F6")),
               aes(SpotFiberCountCh3),
               color = "blue")


ggplot() + geom_histogram(data = filter(df, Well %in% c("F7", "F8", "F9")),
                          aes(SpotFiberCountCh3),
                          bins = 150)