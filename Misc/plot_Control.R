## SandBox for plotting
options("width" = 220)


if (!suppressPackageStartupMessages(require(ggplot2)))
  stop("Require ggplot2 package")
if (!suppressPackageStartupMessages(require(reshape2)))
  stop("Require reshape2 package")



# ##lecture fichier csv
data <- read.csv("/home/arnaud/Desktop/HDV/DATA/FINAL_ANALYSE_3/HDV_removed.csv", header = T, check.names = F)
# print(head(data))

# ## extrait les controls
xdata <- subset(data, GeneName == "Neg infecté" | GeneName == "SiNTCP infecté"  )

xdata <- xdata[,c('GeneName','Plate','PositiveCells')]

ggplot(xdata, aes(x=Plate, y=PositiveCells, group=GeneName, shape=GeneName)) + geom_point() + theme(axis.text.x = element_text(angle = 70, hjust = 1)) + geom_line(aes(color=GeneName))

ggsave(filename="HDV_control_removed.pdf", plot=last_plot(), path="/home/arnaud/Desktop/HDV/DATA/FINAL_ANALYSE_3/", width=16, height=12, dpi=500)



## lecture fichier

# data <- read.csv("/home/arnaud/Desktop/Toulouse_12_2014/ROI_A/Plate1/ssmd_tstat.csv", header=F)
# print(head(data))
# xdata <- data[,c('V1', 'V3', 'V4', 'V5')]
# control <- subset(xdata, V1 == 'Neg' |  V1 == 'F1 ATPase A'| V1 == 'F1 ATPase B')
#
# #xdata <- factor(xdata$V1)
# print(control)
#
# control <- melt(control, id.vars='V1')
#
# print(control)
#
# p <- ggplot(control, aes(variable, value))
# p + geom_jitter(aes(colour = V1), position = position_jitter(width = .1))



library(ggplot2)

path = "/home/akopp/Documents/Dux4Juin2016"
lst <- c("CTRL_BGRemovedB2.csv", "CTRL_BGRemovedB2_RatioNeg1NT.csv", "CTRL_BGRemovedB2_RatioNeg1withoutE23G23.csv", "CTRL_RawData.csv", "CTRL_BGRemovedB2_RatioNeg1NTwithoutE23G23.csv")

for (file in lst){
    df = read.csv(paste(path, file, sep="/"))
    ggplot(df) + geom_point(aes(x=PlateName, y=Well.Mean, group=PlateName, color=PlateMap)) + theme(axis.text.x = element_text(angle = 70, hjust = 1))
    ggsave(filename=paste(unlist(strsplit(file, "[.]"))[1], "pdf", sep="."), plot=last_plot(), path=path, width=16, height=12, dpi=500)
}
