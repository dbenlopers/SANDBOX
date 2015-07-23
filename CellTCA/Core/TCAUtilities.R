
plot_scramble_percent <- function(d, data_file, wd, ht) {
  main <- "Proportion of positive cells for positive control over the screening"
  xlab <- "Proportions"
  ylab <- "Likelihood values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d), type="l", main=main, col="darkred", xlab=xlab, ylab=ylab)
  dev.off()
}  

plot_infection_index <- function(d, data_file, wd, ht) {
  main <- "Percent of positive control over the screening"
  xlab <- "Percent of control"
  ylab <- "Likelihood values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d), type="l", main=main, col="darkred", xlab=xlab, ylab=ylab)
  dev.off()
}   


plot_toxicity_index <- function(d, data_file, wd, ht) {
  main <- "Toxicity Index over the screening"
  xlab <- "Toxicity Index"
  ylab <- "Likelihood values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d), type="l", main=main, col="darkred", xlab=xlab, ylab=ylab)
  dev.off()
}   


calculate_cutoffs <- function(values, percentile1, percentile2) {
  qqvalues <- qqnorm(values[!is.na(values)], plot.it=FALSE)
  qvals <- quantile(values[!is.na(values)], c(percentile1, percentile2))
  qnrms <- qnorm(c(percentile1, percentile2))
  slope <- diff(qvals)/diff(qnrms)
  int <- qvals[1] - slope * qnrms[1]
  x <- sort(qqvalues$x)
  y <- sort(qqvalues$y)
  distance <- abs(slope * x - y + int)/sqrt(1+slope*slope)
  
  n <- length(distance)
  z <- qt(0.975, df=n-1)
  s2 <- sd(log(distance))^2
  s4 <- s2^2
  delta <- z*sqrt((s2/n)+(s4/(2*(n-1))))
  avg <- mean(log(distance))+(s2/2)
  conf_int <- exp(c(avg-delta, avg+delta))
  mdistance <- conf_int[1]
  
  #mdistance <- mean(distance)
  #sdistance <- sd(distance)/sqrt(length(distance))
  #delta_max <- mdistance + sdistance 
  #delta_min <- mdistance - sdistance        
  idx_beg <- which(y <= qvals[1])
  idx_end <- which(y >= qvals[2])
  begs_x <- x[idx_beg]
  begs_y <- y[idx_beg]
  ends_x <- x[idx_end]
  ends_y <- y[idx_end]
  dist_beg <- abs((slope * begs_x - begs_y + int)/sqrt(1+slope*slope))
  dist_end <- abs((slope * ends_x - ends_y + int)/sqrt(1+slope*slope))
  if (length(which(dist_beg >= mdistance))) {
    M <- max(which(dist_beg >= mdistance))
    i_beg <- idx_beg[M]
  }
  else {
    i_beg <- idx_beg[1]
  }
  if (length(which(dist_end >= mdistance))) {  
    m <- min(which(dist_end >= mdistance))
    i_end <- idx_end[m]
  }
  else {
    i_end <- idx_end[length(idx_end)]
  }
  return(c(x[i_beg], y[i_beg], x[i_end], y[i_end]))
} 



plot_infection_index_cutoff <- function(values, data_file, wd, ht) {
  values <- values[!is.na(values)]
  dd <- density(values)
  maxVal <- max(dd$y)
  xVal <- dd$x[max(which(abs(dd$y-maxVal) < 1e-10))]
  cdFunction <- ecdf(values)
  refPercentile <- cdFunction(xVal)
  percentile1 <- refPercentile - 0.25
  percentile2 <- refPercentile + 0.25
  if (percentile1 < 0) {
    percentile1 <- 0
  }
  if (percentile2 > 1) {
    percentile2 <- 1
  }
  cutoffs <- calculate_cutoffs(values, percentile1, percentile2)
  pdf(file=data_file, width=wd, height=ht)
  qqnorm(values)
  qqline(values, col="red", lwd=2)
  abline(h=cutoffs[2], col="darkred")
  abline(h=cutoffs[4], col="darkred")
  text((cutoffs[1]+cutoffs[3])/2, cutoffs[2]+0.07, paste("Low cutoff = ", round(cutoffs[2], digits=3), sep=""), col="darkred", cex=0.8)
  text((cutoffs[1]+cutoffs[3])/2, cutoffs[4]+0.07, paste("High cutoff = ", round(cutoffs[4], digits=3), sep=""), col="darkred", cex=0.8)
  dev.off()
  return(cutoffs)
}   


plot_toxicity_index_cutoff <- function(values, data_file, wd, ht) {
  values <- values[!is.na(values)]
  dd <- density(values)
  maxVal <- max(dd$y)
  xVal <- dd$x[max(which(abs(dd$y-maxVal) < 1e-10))]
  cdFunction <- ecdf(values)
  refPercentile <- cdFunction(xVal)
  percentile1 <- refPercentile - 0.25
  percentile2 <- refPercentile + 0.25
  if (percentile1 < 0) {
    percentile1 <- 0
  }
  if (percentile2 > 1) {
    percentile2 <- 1
  }
  cutoffs <- calculate_cutoffs(values, percentile1, percentile2)
  pdf(file=data_file, width=wd, height=ht)
  qqnorm(values)
  qqline(values, col="red", lwd=2)
  abline(h=cutoffs[4], col="darkred")
  text((cutoffs[1]+cutoffs[3])/2, cutoffs[4]+0.07, paste("Cutoff = ", round(cutoffs[4], digits=3), sep=""), col="darkred", cex=0.8)
  dev.off()
  return(cutoffs)
}   

### Save plate in boxplot format, different function for different output style 
###   -geneBasedData
###   -file_name : "test.pdf"
###   -file_path : "/home/me/Desktop"


save_plate_boxplot_without_outliers <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (! require("reshape2"))
    stop("Require reshape2 package")
  data <- melt(getGeneBasedData(geneBasedData))
  p <- ggplot(data, aes(factor(GeneName), value)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  p + geom_boxplot(outlier.shape = NA) + scale_y_continuous(limits = quantile(data$value, c(0,0.993))) + facet_wrap(~variable, scale="free") 
  ggsave(filename=file_name, plot=last_plot(), path=file_path, width=25, height=20, dpi=400)
}


save_plate_boxplot <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (!require(reshape2))
    stop("Require reshape2 package")
  data <- melt(getGeneBasedData(geneBasedData))
  p <- ggplot(data, aes(factor(GeneName), value)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  p + geom_boxplot() + scale_y_continuous(limits = quantile(data$value, c(0,0.993))) + facet_wrap(~variable, scale="free")
  ggsave(filename=file_name, plot = last_plot(), path=file_path, width=25, height=20, dpi=400) 
}


save_plate_boxplot_brut <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (!require(reshape2))
    stop("Require reshape2 package")
  data <- melt(getGeneBasedData(geneBasedData))
  p <- ggplot(data, aes(factor(GeneName), value)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  p + geom_boxplot() + facet_wrap(~variable, scale="free")
  ggsave(filename=file_name, plot = last_plot(), path=file_path, width=25, height=20, dpi=400)
}

### Save plate in boxplot format, different function for different output style
### These function are only for replicate geneBasedData format !!!
###   -geneBasedData
###   -file_name : "test.pdf"
###   -file_path : "/home/me/Desktop"

replicatBoxplot <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (!require(reshape2))
    stop("Require reshape2 package")
  data <- getGeneBasedData(geneBasedData)
  data$GeneName <- factor(data$GeneName)
  data <- melt(data, id.vars=c("wellIds","GeneName"))
  data$wellIds <- NULL
  data$value <- as.numeric(data$value)
  p <- ggplot(data, aes(factor(GeneName), value)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  p + geom_boxplot(outlier.shape = NA) + scale_y_continuous(limits = quantile(data$value, c(0,0.993))) + facet_wrap(~variable, scale="free") 
  ggsave(filename=file_name, plot=last_plot(), path=file_path, width=25, height=20, dpi=400)
}


replicatBoxplotAll <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (!require(reshape2))
    stop("Require reshape2 package")
  data <- getGeneBasedData(geneBasedData)
  data$GeneName <- factor(data$GeneName)
  data <- melt(data, id.vars=c("wellIds","GeneName"))
  data$wellIds <- NULL
  data$value <- as.numeric(data$value)
  p <- ggplot(data, aes(factor(GeneName), value)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  p + geom_boxplot() + facet_wrap(~variable, scale="free") 
  ggsave(filename=file_name, plot=last_plot(), path=file_path, width=25, height=20, dpi=400)
}


##plot score in plate format by input data
plotScore <- function (data, file, column, type, plateSetup) {
  plateS <- getContent(plateSetup)
  pdf(file)
  plate <- matrix(, nrow(plateS), ncol(plateS))
  plate[,] <- data[match(plateS, names(data))]
  tit <- paste(c(type, " Score for ", column), collapse="")
  plotPlate(as.vector(t(plate)), ncol=ncol(plate), nrow(plate), col=brewer.pal(11, "Spectral"), main=tit, na.action="xout")
  dev.off()
}

### dev
## get Bscore normalized toxicity value 
toxBscore <- function(toxData, plateSetup) {
  plateS <- getContent(plateSetup)
  plate <- matrix(, nrow(plateS), ncol(plateS))
  plate[,] <- toxData[match(plateS, names(toxData))]
  ###median polish
  median_polish <- medpolish(plate, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  residual <- median_polish$residuals
  toxBscore <- apply(residual, 1:2, function(x) (x/(1.4826*median(abs(residual-median(residual,na.rm=T)),na.rm=T))))
  
  tmp <- apply(toxBscore, 1:2, function(X) (X - min(X))/diff(range(X)))
  
  return(toxBscore)
}

### dev
## get Bscore normalized number of cell by well
sizeBscore <- function(data, plateSetup) {
  plateS <- getContent(plateSetup)
  plate <- matrix(, nrow(plateS), ncol(plateS))
  plate[,] <- data[match(plateS, names(data))]
  median_polish <- medpolish(plate, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  dataBscore <- median_polish$residuals
  
  return(dataBscore)
}

### dev
## get BScore/SSMDr cutoff value for selecting value
getBscoreCutoff <- function(data) {
  
  
  return(0)
}



## variante pour une dataframe
## Return mean and standart deviation
get_normal_parameters2 <- function(data) {
  ddata <- density(data, na.rm=T)
  mx <- ddata$x[which(ddata$y==max(ddata$y))]
  if (length(mx) > 1)
    mx <- mx[1]
  mx_b <- data[which(data<=mx)]
  mx_e <- data[which(data>=mx)]
  sx <- min(max(mx-mx_b),max(mx_e-mx))
  sm <- sd(data[which((data >= mx-sx) & (data <= mx+sx))])
  return(c(mx, sm))
}


getToxValues <- function(lengths, norm_pos, norm_neg) {
  return((lengths - norm_pos[1] - 3 * norm_pos[2])/abs(norm_neg[1] - norm_pos[1])) 
}

getLogisticModel2 <- function(controlsData, cols) {
  models <- list()
  for (col in cols) {
    formul <- as.formula(paste("Response ~ ", col)) 
    model <- glm(formul, data=controlsData, family=binomial())
    models[[col]] <- model
  }
  return(models)
}


getPredictivityAccuracy <- function(logisticModel) {
  p.acc <- c()
  cols <- names(logisticModel)
  for (col in cols) {
    my.cv <- CVbinary(logisticModel[[col]], print.details=FALSE)
    p.acc <- c(p.acc,  my.cv$acc.cv)
  }
  names(p.acc) <- cols
  return(p.acc)
}





### function to quantile normalization for batch, little modified for this only use 
normalizeQuantiles <- function(A, ties=TRUE) {
  
  n <- dim(A)
  if(is.null(n)) return(A)
  if(n[2]==1) return(A)
  O <- S <- array(,n)
  nobs <- rep(n[1],n[2])
  i <- (0:(n[1]-1))/(n[1]-1)
  for (j in 1:n[2]) {
    Si <- sort(as.numeric(A[,j]), method="quick", index.return=TRUE)
    nobsj <- length(Si$x)
    if(nobsj < n[1]) {
      nobs[j] <- nobsj
      isna <- is.na(A[,j])
      S[,j] <- approx((0:(nobsj-1))/(nobsj-1), Si$x, i, ties="ordered")$y
      O[!isna,j] <- ((1:n[1])[!isna])[Si$ix]
    } else {
      S[,j] <- Si$x
      O[,j] <- Si$ix
    }
  }
  m <- rowMeans(S)
  for (j in 1:n[2]) {
    if(ties) r <- rank(as.numeric(A[,j]))
    if(nobs[j] < n[1]) {
      isna <- is.na(A[,j])
      if(ties)
        A[!isna,j] <- approx(i, m, (r[!isna]-1)/(nobs[j]-1), ties="ordered")$y
      else
        A[O[!isna,j],j] <- approx(i, m, (0:(nobs[j]-1))/(nobs[j]-1), ties="ordered")$y
    } else {
      if(ties)
        A[,j] <- approx(i, m, (r-1)/(n[1]-1), ties="ordered")$y
      else
        A[O[,j],j] <- m
    }
  }
  A
}


## Gene counts classified by effect sizes !! only for SSMD
GeneEffectCounts <- function(data, feature) {
  print(subset(data,feature > 5.0))
  GeneEffCount <- data.frame(Type=c("Upregulated"), Effect.Classes=c(paste(feature," >= 5", sep="")), Effect.Cutoffs=c("Extremely Strong"), Counts=c(nrow(subset(data,feature >= 5,0))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("5 > ", feature," => 3", sep="")), Effect.Cutoffs=c("Very Strong"), Counts=c(nrow(subset(data,feature > 3.0 & feature < 5.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("3 > ", feature," >= 2", sep="")), Effect.Cutoffs=c("Strong"), Counts=c(nrow(subset(data,feature >= 2.0 & feature< 3.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("2 > ", feature," >= 1.645", sep="")), Effect.Cutoffs=c("Fairly Strong"), Counts=c(nrow(subset(data,feature >= 1.645 & feature < 2.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1.645 > ", feature," >= 1.28", sep="")), Effect.Cutoffs=c("Moderate"), Counts=c(nrow(subset(data,feature >= 1.28 & feature < 1.645 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1.28 > ", feature," >= 1", sep="")), Effect.Cutoffs=c("Fairly Moderate"), Counts=c(nrow(subset(data,feature >= 1 & feature < 1.28 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1 > ", feature," >= 0.75", sep="")), Effect.Cutoffs=c("Fairly Weak"), Counts=c(nrow(subset(data,feature >= 0.75 & feature < 1 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.75 > ", feature," >= 0.5", sep="")), Effect.Cutoffs=c("Weak"), Counts=c(nrow(subset(data,feature >= 0.5 & feature < 0.75 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.5 > ", feature," >= 0.25", sep="")), Effect.Cutoffs=c("Very Weak"), Counts=c(nrow(subset(data,feature >= 0.25 & feature < 0.5 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.25 > ", feature," >= 0", sep="")), Effect.Cutoffs=c("Extremely Weak"), Counts=c(nrow(subset(data,feature >= 0 & feature < 0.25 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("zero"), Effect.Classes=c("=0"), Effect.Cutoffs=c("no effect"), Counts=c(nrow(subset(data,feature == 0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("0 > ", feature," >= -0.25", sep="")), Effect.Cutoffs=c("Extremely Weak"), Counts=c(nrow(subset(data,feature >= -0.25 & feature < 0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.25 > ", feature," >= -0.5", sep="")), Effect.Cutoffs=c("Very Weak"), Counts=c(nrow(subset(data,feature >= -0.5 & feature < -0.25 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.5 > ", feature," >= -0.75", sep="")), Effect.Cutoffs=c("Weak"), Counts=c(nrow(subset(data,feature >= -0.75 & feature < -0.5 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.75 > ", feature," >= -1", sep="")), Effect.Cutoffs=c("Fairly Weak"), Counts=c(nrow(subset(data,feature >= -1 & feature < -0.75 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1 > ", feature," >= -1.28", sep="")), Effect.Cutoffs=c("Fairly Moderate"), Counts=c(nrow(subset(data,feature >= -1.28 & feature < -1 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1.28 > ", feature," >= -1.645", sep="")), Effect.Cutoffs=c("Moderate"), Counts=c(nrow(subset(data,feature >= -1.645 & feature < -1.28 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1.645 > ", feature," >= -2", sep="")), Effect.Cutoffs=c("Fairly Strong"), Counts=c(nrow(subset(data,feature >= -2 & feature < -1.645 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-2 > ", feature," >= -3", sep="")), Effect.Cutoffs=c("Strong"), Counts=c(nrow(subset(data,feature >= -3 & feature < -2 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-3 > ", feature," >= -5", sep="")), Effect.Cutoffs=c("Very Strong"), Counts=c(nrow(subset(data,feature >= -5 & feature < -3 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste(feature, "> -5", sep="")), Effect.Cutoffs=c("Extremely Strong"), Counts=c(nrow(subset(data, feature < -5 )))) )
  return(GeneEffCount)
}


#Get bscore normalized SSMDr on mean count Cell
getBscoresimpledata <- function(meanCounts, plateSetup, size, neg) {
  ## function to tranform Well in B3 to 2,3
  WellToLoc=function(WellNo) {
    WellNo=as.character(WellNo)
    row.num=match(substr(WellNo, 1, 1), LETTERS)
    col.num=as.integer(substr(WellNo, 2, 3))
    loc=cbind(row.num, col.num)
    return(list(loc=loc))
  }
  
  
  gene_well <- as.matrix(getGenes(plateSetup))
  bscore <- unlist(lapply(meanCounts, function(x) x=0))
  if (size == 96) {
    data <- matrix(-9999, nrow=8, ncol=12)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H"),         # row names 
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")) # column names
  } else {
    data <- matrix(-9999, nrow=16, ncol=24)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"),       
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24")) 
  } 
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      data_well <- meanCounts[gene]
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      data[row, col] <- data[row, col] + median(data_well) 
    }
  }
  data[data == -9999] <- NA
  median_polish <- medpolish(data, eps = 1e-5, na.rm=T, maxiter = 200, trace.iter=F)
  residual <- median_polish$residuals
  bscore_tmp = apply(residual, 1:2, function(x) (x/mad(residual, na.rm=T)))
  
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      bscore[gene] <- bscore_tmp[row, col]
    }
  } 
  
#   ## search number of neg well for median
#   platesetup.content <-getContent(plateSetup)
#   cnt <- table(platesetup.content)
#   neg.cnt <- cnt[names(cnt)==neg]
#   
#   ## neg data for median calcul
#   neg.data = bscore[neg]

  
  ##performed median on bscore normalized data
  meancount <- unlist(lapply(bscore, function(x) (x- median(bscore, na.rm=T))/ (sqrt(2)*mad(bscore, na.rm=T))))
  return(meancount)
  
  
}



###### deprecated function ######



# @depre
## function to tranform Well in B3 to 2,3
WellToLoc=function(WellNo) {
  WellNo=as.character(WellNo)
  row.num=match(substr(WellNo, 1, 1), LETTERS)
  col.num=as.integer(substr(WellNo, 2, 3))
  loc=cbind(row.num, col.num)
  return(list(loc=loc))
}

# @depre
## plot matrix into 3d perspective 
matrix_persp_plot = function(matrix, file_path) {
  pdf(file_path)
  persp(matrix, theta = 45, phi = 30, col = "green3", shade = 0.75,xlab = "A B C ...", ylab="1 2 3 ...", zlab="Value")
  dev.off()
}


# @depre
## dataframe to matrix
to_matrix_unop = function(dataframe, platesetup, column, size) {
  gene_well <- as.matrix(getGenes(platesetup))
  if (size == 96) {
    data <- matrix(0, nrow=8, ncol=12)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H"),         # row names 
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")) # column names
  } else {
    data <- matrix(0, nrow=16, ncol=24)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"),       
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"))
  }
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      data_well <- dataframe[gene]
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      data[row, col] <- data[row, col] + data_well 
    }
  }
  return(data)
}

to_matrix <- compiler::cmpfun(to_matrix_unop)

# @depre
## dataframe to matrix with 0 to NA 
to_matrix2_unop = function(dataframe, platesetup, column, size) {
  gene_well <- as.matrix(getGenes(platesetup))
  if (size == 96) {
    data <- matrix(0, nrow=8, ncol=12)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H"),         # row names 
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")) # column names
  } else {
    data <- matrix(0, nrow=16, ncol=24)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"),       
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"))
  }
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      data_well <- dataframe[gene]
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      data[row, col] <- data[row, col] + data_well 
    }
  }
  data[data == 0] <- NA
  return(data)
}

to_matrix2 <- compiler::cmpfun(to_matrix2_unop)


# @depre
## save matrix into csv 
save_matrix_csv = function(data, file_path) {
  write.csv(data, file_path, na="")
}

# @depre
## plot score (matrix data) in plate format
scorePlot <- function(data, fname, column, type) {
  pdf(fname)
  tit <- paste(c(type," Score for ", column), collapse="")
  plotPlate(as.vector(t(data)), ncol=ncol(data), nrow=nrow(data), col=brewer.pal(11, "Spectral"), main=tit, na.action="zero")
  dev.off()
}



