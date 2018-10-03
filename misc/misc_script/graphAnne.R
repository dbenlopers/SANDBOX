library(ggplot2)
library(magrittr)
library(dplyr)
library(reshape2)

df = read.csv("/home/akopp/Documents/Anne/Heidi/CellHealthProfiling.V4_02-09-17_04;55;24/170209 Heidi-170209 Heidi.csv")

df$Condition <- "No virus"
df[df$Well %in% c("B2", "B3", "B4"),]$Condition <- "DMSO 10k"
df[df$Well %in% c("C2", "C3", "C4"),]$Condition <- "C1 10k"
df[df$Well %in% c("D2", "D3", "D4"),]$Condition <- "C24 10k"
df[df$Well %in% c("B8", "B9", "B10"),]$Condition <- "DMSO 15k"
df[df$Well %in% c("C8", "C9", "C10"),]$Condition <- "C1 15k"
df[df$Well %in% c("D8", "D9", "D10"),]$Condition <- "C24 15k"

df[df$Well %in% c("B5", "C5", "D5"),]$Condition <- "no virus 10k"
df[df$Well %in% c("B11", "C11", "D11"),]$Condition <- "no virus 15k"

only <- c("DMSO 10k", "C1 10k", "C24 10k", "DMSO 15k", "C1 15k", "C24 15k")

ggplot(data = filter(df, Condition %in% only)) + 
  geom_density(aes(AvgIntenCh2, group=Condition, color=Condition)) + ylim(c(0, 0.05)) + 
  xlim(c(0, 750))
