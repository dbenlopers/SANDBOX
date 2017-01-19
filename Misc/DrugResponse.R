library(drc)

df <- read.csv("/home/akopp/Documents/Boh/CS_FINAL_DATA.csv")
head(df)


conc <- c(0, 0.69897, 1.11394335, 1.49136169, 1.89762709,
          2.29446623, 2.6919651, 3.08955188, 3.48742121, 3.88536122,
          4.28330123, 4.68124124, 5.07918125, 5.47712125)

dr_data <- data.frame(Slope = double(), 
                      LowerLimit = double(), 
                      UpperLimit = double(),
                      EC50 = double())

for (i in 1:nrow(df)) {
  i = 15
  response <- t(as.matrix(df[i, 1:14]))
  elem <- as.character(paste(df[i, 15], df[i, 16]))
  dr <-
    drm(response ~ conc, fct = LL.4(names = c(
      "Slope", "LowerLimit", "UpperLimit", "EC50"
    )))
  dr_data[i, 1:4] <- dr$fit$par
  
  plot(dr,
      xlab = "Dose",
      ylab = "Viability",
      log = "",legend = TRUE, legendText = elem
      )
}

head(dr_data)

# write.csv(x = dr_data, file = "/home/akopp/Documents/Boh/CS_FINAL_DATA_EC50_byR.csv")
