library(ggplot2)
library(magrittr) 
library(dplyr)
library(reshape2)

# df = read.csv("/home/akopp/Documents/Anagenesis/Test_3novembre/Resultat.csv")
# 
# head(df)
# 
# ## Normalization
# # df[c(4,5,6)] = df[c(4,5,6)] / colMeans(df[c(4,5,6)])
# 
# # cor(df[c(4,5,6)])
# 
# # ggplot(data = df)  + geom_point(aes(y = TotalTubeAreaCh1.4x.Angio.TubeFormation.Mean, x = Well, color = PlateMap)) 
# ggplot(data = df)  +  geom_point(aes(y = TotalTubeAreaCh1.10x.Angio.TubeFormation.Mean, x = PlateMap, color = PlateMap))
# # ggplot(data = df)  +  geom_point(aes(y = TotalTubeAreaCh1.10x.Morphology.Mean, x = PlateMap , color = PlateMap))
# 
# # ggsave("Anagenesis.pdf", path="/home/akopp/Documents/Anagenesis/Test_3novembre/", plot=last_plot())
# 
# df1 = read.csv("/home/akopp/Documents/Anagenesis/TEST_3nov bis/CellandDrug.csv")
# df2 = read.csv("/home/akopp/Documents/Anagenesis/TEST_3nov bis/CellpuisDrug.csv")
# 
# 
# by_PlateMap <- group_by(df1, PlateMap)
# res1 <- summarise(by_PlateMap,
#                   mean1.1 = mean(TotalTubeAreaCh1.1.1.Mean, na.rm = TRUE),
#                   sd1.1 = sd(TotalTubeAreaCh1.1.1.Mean, na.rm = TRUE),
#                   mean1.2 = mean(TotalTubeAreaCh1.1.2.Mean, na.rm = TRUE),
#                   sd1.2 = sd(TotalTubeAreaCh1.1.2.Mean, na.rm = TRUE))
# 
# by_PlateMap <- group_by(df2, PlateMap)
# res2 <- summarise(by_PlateMap,
#                   mean1.1 = mean(TotalTubeAreaCh1.1.1.Mean, na.rm = TRUE),
#                   sd1.1 = sd(TotalTubeAreaCh1.1.1.Mean, na.rm = TRUE),
#                   mean1.2 = mean(TotalTubeAreaCh1.1.2.Mean, na.rm = TRUE),
#                   sd1.2 = sd(TotalTubeAreaCh1.1.2.Mean, na.rm = TRUE))
# 
# cellanddrug <- as.data.frame(res1)
# cellpuisdrug <- as.data.frame(res2)
# write.csv(x = cellanddrug, file = "/home/akopp/Documents/Anagenesis/TEST_3nov bis/cellanddrug.csv")
# write.csv(x = cellpuisdrug, file = "/home/akopp/Documents/Anagenesis/TEST_3nov bis/cellpuisdrug.csv")

df = read.csv("/home/akopp/Documents/Anagenesis/TEST_9dec/4X/Resultat V2.csv")

head(df)

dfmelt <- melt(df)

# scatter plot
ggplot(
  data = df,
  aes(
    y = TotalTubeAreaCh1.rep1.Mean,
    x = PlateName,
    color = PlateMap,
    group = PlateName
  )
) + geom_jitter() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

DF <- dfmelt[dfmelt$PlateMap != "Ctrl 2",]

# box plot
ggplot(
  data = dfmelt,
  aes(
    y = value,
    x = PlateName,
    fill = PlateMap
  )
) + geom_boxplot() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

res <-
  df %>% group_by(PlateMap, PlateName) %>% summarise(
    mean = mean(TotalTubeAreaCh1.rep1.Mean),
    sd = sd(TotalTubeAreaCh1.rep1.Mean)
  )

ggplot(res) + geom_point(aes(
  x = PlateName,
  y = mean,
  group = PlateMap,
  color = PlateMap
)) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))
write.csv(as.data.frame((res)), file = "/home/akopp/Documents/Anagenesis/Test_16novembre/Compil/ResultatMean.csv")