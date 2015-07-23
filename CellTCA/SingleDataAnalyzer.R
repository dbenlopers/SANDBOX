## Script for analyzis single data by well
## Made for sophie pernot in first by Arnaud KOPP
start.time <- Sys.time()
library(prada)

CsvDir <- "/home/akopp/Bureau/screen sophie HCV/Antago/reinf/"
outputdir <- "/home/akopp/Bureau/screen sophie HCV/Resultat3009/Antagoreinf/"
dir.create(outputdir)
setwd(outputdir)

TCARESULTS <- data.frame()


## add data(matrix) with geneName(platesetup matrix)
addData <- function(data1, data2, data3, data4, PlateSetup) {
  d <- nrow(PlateSetup)*ncol(PlateSetup)
  genes <- matrix(rep(NA, d), nrow=d, ncol=6)
  i <- 1
  for (row in rownames(PlateSetup)) {
    for (col in colnames(PlateSetup)) {
      genes[i,] <- c(paste(c(row, col), collapse=""), PlateSetup[row, col], data1[row, col], data2[row, col], data3[row, col], data4[row, col])
      i <- i+1
    }
  }
  # Remove NA genes before returning
  return(DatageneList <- (genes[which(!is.na(genes[,2])),]))
}

## add data(matrix) with geneName(platesetup matrix)
addDataBis <- function(data1, data2, data3, PlateSetup) {
  d <- nrow(PlateSetup)*ncol(PlateSetup)
  genes <- matrix(rep(NA, d), nrow=d, ncol=5)
  i <- 1
  for (row in rownames(PlateSetup)) {
    for (col in colnames(PlateSetup)) {
      genes[i,] <- c(paste(c(row, col), collapse=""), PlateSetup[row, col], data1[row, col], data2[row, col], data3[row, col])
      i <- i+1
    }
  }
  # Remove NA genes before returning
  return(DatageneList <- (genes[which(!is.na(genes[,2])),]))
}

## plot score in plate format
plotScorePlate <- function(data, file, title){
  pdf(file)
  plotPlate(as.vector(t(data)),nrow=nrow(data), ncol=ncol(data), col=brewer.pal(11, "Spectral"), main=title, na.action="xout")
  dev.off() 
}




spnames <- dir(pattern="Rep", path=CsvDir, ignore.case=TRUE) #data file
ppnames <- dir(pattern="PP", path=CsvDir, ignore.case=TRUE) #platesetup file
searchSUP <- regexpr("SUP",spnames)
searchREP <- regexpr("rep", spnames)
searchPP <- regexpr("PP", ppnames)
replTy <- factor(substr(spnames,1,2+apply(cbind(searchREP,searchSUP),1,max))) #ensemble de replica de plaque
ppTy <- factor(substr(ppnames,1,2+apply(cbind(searchPP,searchSUP),1,max))) #PP (PlanPlaque)




## Performed analysis on each couple of replicat
for(i in 1:length(levels(replTy))) { 
  l <- 0
  ppnum <- i
  ## reading plate setup for each type of plate
  pp.path.file <- ppnames[ppnum] 
  file.path <- paste(CsvDir,pp.path.file, sep="/")
  cat(paste("Opening file : ", file.path,"\n"))
  
  
  ## input reading
  plateSetup = read.csv(file.path, header = TRUE, check.names=FALSE)
  PlateSetup <- as.matrix(plateSetup[1:8,2:13])
  colnames(PlateSetup) <- 1:12
  rownames(PlateSetup) <- LETTERS[1:8]

  ## the replicate of same plate
  plateType <- factor(substr(spnames,1,2+apply(cbind(searchREP,searchSUP),1,max))) 
  fileList <- list()
  for(j in which(replTy == levels(replTy)[i])) {   ##parcours de chaque replicat/fichier
    l <- l+1
    tmpDir <- spnames[j]
    in.pathFile <- tmpDir
    file.path <- paste(CsvDir,in.pathFile, sep="/")
    cat(paste("Opening file : ", file.path, "\n"))
    fileList <- c(fileList, file.path)
  }

  ## READING REPLICAT
  rep1 = as.matrix(read.csv(fileList[[1]], header = F, check.names=FALSE))
  colnames(rep1) <- 1:12
  rownames(rep1) <- LETTERS[1:8]
  rep2 = as.matrix(read.csv(fileList[[2]], header = F, check.names=FALSE))
  colnames(rep2) <- 1:12
  rownames(rep2) <- LETTERS[1:8]
  rep3 = as.matrix(read.csv(fileList[[3]], header = F, check.names=FALSE))
  colnames(rep3) <- 1:12
  rownames(rep3) <- LETTERS[1:8]
  
  
  ## BEGIN 

  TCAResults <- addDataBis(rep1, rep2, rep3, PlateSetup)
  ## Rename column
  colnames(TCAResults) <- c("Well"," GeneName", "Replicat1", "Replicat2", "Replicat3")
  
  ## mean of replicat
  repmean <- apply(rep1+rep2+rep3, c(1,2), function(x) x/3)
  
  ## determine SSMDr
  ssmdr1 <- apply(rep1, c(1,2), function(x) (as.numeric(x)- median(as.numeric(rep1)))/ (sqrt(2)*mad(as.numeric(rep1))))
  ssmdr2 <- apply(rep2, c(1,2), function(x) (as.numeric(x)- median(as.numeric(rep2)))/ (sqrt(2)*mad(as.numeric(rep2))))
  ssmdr3 <- apply(rep3, c(1,2), function(x) (as.numeric(x)- median(as.numeric(rep3)))/ (sqrt(2)*mad(as.numeric(rep3))))
  ssmdrmean <- apply(repmean, c(1,2), function(x) (as.numeric(x)- median(as.numeric(repmean)))/ (sqrt(2)*mad(as.numeric(repmean))))
  plotScorePlate(ssmdrmean, paste(replTy[ppnum],"SSMDr", sep="_"), "SSMDr from mean data")
  
  SSMDRData <- addData(ssmdr1, ssmdr2, ssmdr3, ssmdrmean, PlateSetup)
  colnames(SSMDRData) <- c("Well"," GeneName", "SSMDr1", "SSMDr2", "SSMDr3", "SSMDrMean")
  TCAResults <- as.data.frame(cbind(TCAResults[,], SSMDRData))
  
  ##  median polish  = B-score norm
  median_polish1 <- medpolish(rep1, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  median_polish2 <- medpolish(rep2, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  median_polish3 <- medpolish(rep3, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  median_polishmean <- medpolish(repmean, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  
  ## determiner SSMDr on bscore normalized data
  ssmdrnorm1 <-  apply(median_polish1$residuals, c(1,2), function(x) (as.numeric(x)- median(as.numeric(median_polish1$residuals)))/ (sqrt(2)*mad(as.numeric(median_polish1$residuals))))
  ssmdrnorm2 <-  apply(median_polish2$residuals, c(1,2), function(x) (as.numeric(x)- median(as.numeric(median_polish2$residuals)))/ (sqrt(2)*mad(as.numeric(median_polish2$residuals))))
  ssmdrnorm3 <-  apply(median_polish3$residuals, c(1,2), function(x) (as.numeric(x)- median(as.numeric(median_polish3$residuals)))/ (sqrt(2)*mad(as.numeric(median_polish3$residuals))))
  ssmdrnormmean <- apply(median_polishmean$residuals, c(1,2), function(x) (as.numeric(x)- median(as.numeric(median_polishmean$residuals)))/ (sqrt(2)*mad(as.numeric(median_polishmean$residuals))))
  plotScorePlate(ssmdrnormmean, paste(replTy[ppnum],"SSMDrBscoreNorm", sep="_"), "SSMDr with B-score norm from mean data")
  
  SSMDRNormData <- addData(ssmdrnorm1, ssmdrnorm2, ssmdrnorm3, ssmdrnormmean, PlateSetup)
  colnames(SSMDRNormData) <- c("Well"," GeneName", "SSMDrNorm1", "SSMDrNorm2", "SSMDrNorm3", "SSMDrNormMean")
  TCAResults <- cbind(TCAResults, SSMDRNormData)
  
  TCARESULTS <- rbind(TCARESULTS, TCAResults)
  
}
filePath <- "RESULTSTCA.csv"
write.csv(TCARESULTS, file=filePath)


end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)