library(drc)
library(ggplot2)

df <- read.csv("/home/akopp/Documents/Boh/AC_Trastuzinab_DATA.csv")
outfilepath <- "/home/akopp/Documents/Boh/AC_Trastuzinab_DATA_EC50.csv"
outDirpath <- "/home/akopp/Documents/Boh/Graph"

concDil = 10000

# # concentration for cetuximab * 100000
# conc <- c(0, 0.981862765594676, 1.37980277426671, 1.77774278293875, 2.17568279161079,
#           2.57362280028283, 2.97156280895486, 3.3695028176269, 3.76744282629894,
#           4.16538283497098, 4.56332284364301, 4.96126285231505, 5.35920286098709, 5.75714286965913 )
# concentration for trastuzimab * 10000
conc <- c(0, 0.605834976645399, 1.00377498531744, 1.40171499398947, 1.79965500266151,
          2.19759501133355,2.59553502000559, 2.99347502867762, 3.39141503734966, 3.7893550460217,
          4.18729505469374, 4.58523506336578, 4.98317507203781, 5.38111508070985)
# #concentration for chemical compound * 10000
# conc <- c(0, 0.69897, 1.11394335, 1.49136169, 1.89762709,
#           2.29446623, 2.6919651, 3.08955188, 3.48742121, 3.88536122,
#           4.28330123, 4.68124124, 5.07918125, 5.47712125)

dr_data <- data.frame(
  Slope = double(nrow(df)),
  LowerLimit = double(nrow(df)),
  UpperLimit = double(nrow(df)),
  EC50 = double(nrow(df)),
  EC50_µM = double(nrow(df)),
  Fitting = double(nrow(df)),
  AUC = double(nrow(df))
)

# df[, 1:14] <- df[, 1:14] / df[, 1]


for (i in seq(1, nrow(df), 3)) {
  df[i:(i + 2), 1:14] <- df[i:(i + 2), 1:14] / mean(df[i:(i + 2), 1])
  temp <- df[i:(i + 2), 1:14]
  response <- data.matrix(colMeans(temp))
  sd_data <- data.matrix(apply(temp, 2, sd))
  # print(response)
  # print(mean(response))
  
  elem <- as.character(paste(df[i, 15], df[i, 16]))
  drmc(errorm = TRUE)
  dr <- drm(response ~ conc, fct = LL.4(names = c("Slope", "LowerLimit", "UpperLimit", "EC50")))
  dr_data[i, 1:4] <- dr$fit$par
  dr_data[i, 6] <- dr$fit$value
  
  dose_response <- function(conc) {
    res <- predict(dr, data.frame(conc = conc))
    res
  }
  AUC <- integrate(dose_response, lower = min(conc), upper = max(conc))
  dr_data[i, 7] <- AUC$value
  
  # ggplot2 plotting part
  newdata <- expand.grid(conc = seq(min(conc), max(conc), length = 100))
  pm <- predict(dr, newdata = newdata, interval = "confidence")
  newdata$p <- pm[,1]
  newdata$pmin <- pm[,2]
  newdata$pmax <- pm[,3]
  input <- as.data.frame(conc)
  input$meanResponse <- response
  input$sdResponse <- sd_data

  ggplot() +
    geom_point(data = input, aes(x = conc, y = meanResponse)) +
    geom_errorbar(data = input, aes(x = conc, ymin = meanResponse - sdResponse, ymax = meanResponse + sdResponse), width = 0.1, alpha = 0.4) +
    geom_ribbon(data = newdata, aes(x = conc, ymin = pmin, ymax = pmax), alpha = 0.2) +
    geom_line(data = newdata, aes(x = conc, y = p)) +
    xlab('Dose concentration') + ylab('Viability') + ylim(c(-0.2, 1.4))
  FilePath <- file.path(outDirpath, c(elem, '.pdf'))
  ggsave(FilePath, plot = last_plot(), device = "pdf")

  
  # FilePath <- file.path("/home/akopp/Documents/Boh/Graph R mean", c(elem, '.pdf'))
  # pdf(FilePath)
  # plot(dr,
  #     xlab = "Dose",
  #     ylab = "Viability",
  #     log = '', legend = TRUE, legendText = elem, ylim = c(-0.1, 1.2)
  #     )
  # dev.off()
}

dr_data <- cbind(dr_data, df[, 15:16])
dr_dataF <- dr_data[dr_data$Slope != 0,]
dr_dataF$EC50_µM <- (10 ** dr_dataF$EC50) / concDil
head(dr_dataF)

write.csv(x = dr_dataF, file = outfilepath)
