### SANDBOX !!!!!!!!!!!!
start.time <- Sys.time()

options("width"=220)
cat("\n     #     # #######  #####     ######                            #                                                    \n")
cat("     #     #    #    #     #    #     #   ##   #####   ##        # #   #    #   ##   #      #   # ###### ###### #####  \n")
cat("     #     #    #    #          #     #  #  #    #    #  #      #   #  ##   #  #  #  #       # #      #  #      #    # \n")
cat("     #######    #     #####     #     # #    #   #   #    #    #     # # #  # #    # #        #      #   #####  #    # \n")
cat("     #     #    #          #    #     # ######   #   ######    ####### #  # # ###### #        #     #    #      #####  \n")
cat("     #     #    #    #     #    #     # #    #   #   #    #    #     # #   ## #    # #        #    #     #      #   #  \n")
cat("     #     #    #     #####     ######  #    #   #   #    #    #     # #    # #    # ######   #   ###### ###### #    # \n")
cat("\n\n    WELCOME TO THE HTS DATA PROGRAM ANALYZER \n")
cat("    THIS PROGRAM IS PROVIDED WITHOUT ANY GUARANTIE \n")


## IMPORT FOR PACKAGES DEPENDENCY
suppressPackageStartupMessages(library(limma))
suppressPackageStartupMessages(library(prada))
suppressPackageStartupMessages(library(foreach))
suppressPackageStartupMessages(library(doMC))
suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(methods))


## IMPORT CELLTCA Core
source("/home/arnaud/PROJECT/CellTCA/Core/TCAMetaInfo.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCAPlateSetup.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCADataInfo.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCASummaries.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCAGeneBasedData.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCAData.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCAReplicate.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCAUtilities.R")
source("/home/arnaud/PROJECT/CellTCA/Core/CellTCA.R")
source("/home/arnaud/PROJECT/CellTCA/Core/TCAcsv.R")
load("/home/arnaud/PROJECT/CellTCA/Core/TCASVMModel.Rd")



## import arg
csvDir = "/home/arnaud/Desktop/TEMP/Ali/" # PARAM HERE !!!!!!!!!!!!
outputdir = "/home/arnaud/Desktop/TEMP/Ali/RES_50/" # PARAM HERE !!!!!!!!!!!!
dir.create(outputdir)
setwd(outputdir)
neg = as.character("C5")
pos = as.character("C4")
tox = as.character("C4")
Threshold.ref = 50
colAnalyze <- c("TargetTotalIntenCh2") # PARAM HERE !!!!!!!!!!!!
median.processing <- F
nb.process <- 3


## Save arg in txt file
fileConn<-file("PARAMETERS.txt", "w")
writeLines(paste("INPUT DATA : ",csvDir, sep=""), con=fileConn, sep = "\n")
writeLines(paste("OUPUT DATA : ",outputdir, sep=""), con=fileConn, sep = "\n")
writeLines(paste("NEGATIF CONTROL : ",neg, sep=""), con=fileConn, sep = "\n")
writeLines(paste("POSITIF CONTROL : ",pos, sep=""), con=fileConn, sep = "\n")
writeLines(paste("TOXICITY CONTROL : ",tox, sep=""), con=fileConn, sep = "\n")
writeLines(paste("THRESHOLD : ",Threshold.ref, sep=""), con=fileConn, sep = "\n")
writeLines(paste("FEATURES ANALYSED : ",colAnalyze, sep=""), con=fileConn, sep = "\n")
writeLines(paste("MEDIAN PROCESSING DATA : ",median.processing, sep=""), con=fileConn, sep = "\n")
close(fileConn)



#setup parallel backend to use X processors
registerDoMC(nb.process) #change the X to your number of CPU cores


## txt file for thres for each plate
thres.save <- file("Thres_save.txt", "w")
cat("THRESHOLD FOR CONSIDER CELL AS POSITIVE, FOR ALL PLATE",file=thres.save,sep="\n")


if (length(colAnalyze)>1) {
  cat("\n!!! BEWARE QUALITY CONTROL AND REF CHECK ONLY PERFORMED ON FIRST ENTRY COLUMN !!!\n")
  cat("!!! NO AUTOMATIC HIT SELECTION WITH MULTI COLUMN ANALYSIS \n\n")
}

if (neg == "")
  stop("No negative sample name found")
if (pos == "")
  stop("No positive sample name found")
if (tox == "")
  stop("No toxicity sample name found")

#redo = F check if data is already process
#redo = T make process is all case
#### Generate CellTCA data ####
cat("\n\n################ READING INPUT DATA ################\n\n")
readCSVDir(csvDir, outputdir, redo=T, refSamp=neg, refThr=Threshold.ref, colAnalyze, nb.process) 
entryNames <- dir(path=outputdir, pattern="RData")


if (length(entryNames) == 0) {
  stop("No DATA FOUND !!")
} else {
  cat("FOUND :\"",length(entryNames),"\" PLATE(S)\n")
}

tcaIdx <- 0
nImages <- 6

######### FUNCTIONS DEFINITION ###########

## function for analyzis each plate
## take in input a entry (RData file with cellTCA object) and give in return a dataframe with results data
Analyzis <- function(entry) {
  ### Create some variable
  geneRef <- c(); columnName <- c(); geneName <- c(); percentValues <- c(); semPercentValues <- c()
  plateNames <- c(); meanCounts <- c(); sdCounts <- c(); totalPvalues <- c(); totalInfectionIdx <- c()
  totalToxicityIdx <- c(); totalMwPvalues <- c(); controls <- c()
  mean <- c()
  median <- c()
  ssmdr <- c()
  ssmd <- c()
  
  
  cat("\n######## ANALYSIS of :\"",entry,"\" ########\n")
  tcaIdx <- tcaIdx + 1
  load(paste(outputdir, "/", entry, sep=""))
  plateName <- gsub(".RData", "", gsub("CellTCA_", "", entry))
  # Get control names
  controls <- c(controls, getControls(cellTCA)) 
  # Set positive control geneName
  posSamp <- c(posName=pos) 
  # Layout of the plate 
  plateSetup <- getPlateSetup(cellTCA, 1)
  # Negative control geneName
  sampName <- getRefSamp(cellTCA)
  
  ## Get Well/Gene name
  uGenes <- getUniqueGeneNames(cellTCA)
  
  ## Get Well/Gene name without controls 
  uGenes_without_controls <- getUniqueGeneNames(cellTCA)
  uGenes_without_controls <- uGenes_without_controls[-which(uGenes==sampName)]
  uGenes_without_controls <- uGenes_without_controls[-which(uGenes==posSamp)]
  
  
  graph.path <- paste(outputdir, plateName,sep="/")
  dir.create(graph.path)
  ## Change current dir
  setwd(graph.path)
  
  
  ## NORMALIZATION PROCESSING
  cat("    ######## NORMALIZATION PROCESSING ########\n")
  # Run normalization over the data and store it in a form that will make it easy to process
  geneBasedData <- getWellNormGeneBasedData(cellTCA, median=median.processing)
  
  # Read columns of the data labeled for analyzing, If there are more than one column 
  # each column will be analyzed separately
  colsToAnalyze <- getModColumnNamesToAnalyze(cellTCA)
  
  
  for (i in 1:length(colsToAnalyze)) {
    cat("    ######## ANALYSIS DATA COLUMN : \"",colsToAnalyze[i],"\" ########\n")
    
    refThreshold <- getRefThreshold(cellTCA)
    if (is.na(refThreshold)) {
      if (is.na(sampName) | is.null(sampName) | (length(sampName)==0)
          | is.na(posSamp) | is.null(posSamp) | (length(posSamp)==0)) {
        stop("Control is missing")
      }
      else {
        # Estimate the cell positive cutoff from the data
        thresholdValues <- getEstimatedThresholdValues_c(geneBasedData, sampName, posSamp, colsToAnalyze[i])
        if (length(thresholdValues) == 0)
          thresholdValues = 0.0
      }  
    }
    else {
      if (refThreshold >= 1)            
        refThreshold <- 1-(refThreshold/100)
      thresholdValues <- getThresholdValues(geneBasedData, sampName, refThreshold, colsToAnalyze[i])
    }
    print(thresholdValues)
    cat(paste("PLATE : ", plateName,"  THRES : ", thresholdValues[1],"\n",sep=""),file=thres.save, append=TRUE)
    
    
    # Generate summaries from the data
    summaries <- getSummaries(geneBasedData, colsToAnalyze[i])
    
    # Keep track of number of replicates per gene
    countRepPerGene <- getNumberOfReplicatesPerGene(cellTCA)
    countRepPerGene <- countRepPerGene[which(!is.na(countRepPerGene))]
    counts <- getMeanLengths(cellTCA)
    geneNumberPerPlate <- length(uGenes)
    
    tmp <- getMetaInfo(cellTCA)
    size <- getPlateSize(tmp)
    
    # Collect data for final output results
    
    geneRef <- c(geneRef, rep(sampName, length(countRepPerGene)))
    columnName <- c(columnName, rep(colsToAnalyze[i], length(countRepPerGene)))
    plateNames <- c(plateNames, rep(plateName, length(countRepPerGene)))
    pValues <- getChisqPvalues(geneBasedData, posSamp, thresholdValues[1], colsToAnalyze[i])
    vtmp <- getPercentAboveThreshold(geneBasedData, thresholdValues[1], colsToAnalyze[i])
    infectIdx <- vtmp/vtmp[posSamp]
    lengths <- getLengthSummary(summaries, 1)
    t_lengths <- lengths / countRepPerGene[names(lengths)]
    maxLen <- max(t_lengths)
    minLen <- min(t_lengths)
    toxIndex <- (maxLen - t_lengths) / (maxLen - minLen)
    ntmp <- names(vtmp)
    # Standard deviation of percent of positive cells per well
    semPc <- sqrt((vtmp*(1-vtmp))/(lengths[ntmp]))
    semPercentValues <- c(semPercentValues, semPc) 
    geneName <- c(geneName, ntmp)
    percentValues <- c(percentValues, vtmp[ntmp])
    meanCounts <- c(meanCounts, counts$mean[ntmp])
    sdCounts <- c(sdCounts, counts$sd[ntmp])
    ## avoid if no replicat error warning
    sdCounts <- unlist(lapply(sdCounts, function(x) replace(x,is.na(x),0)))
    totalPvalues <- c(totalPvalues, pValues[ntmp])
    totalInfectionIdx <- c(totalInfectionIdx, infectIdx[ntmp])
    totalToxicityIdx <- c(totalToxicityIdx, toxIndex[ntmp])      
    
    #calcul viability/toxicity
    try({
      data_tmp <- getGeneBasedData(geneBasedData)
      data_pos <- as.data.frame(data_tmp[pos])
      data_neg <- as.data.frame(data_tmp[neg])
      if (getNumberOfReplicates(cellTCA)==1) {
        normParams_pos <- get_normal_parameters2(as.numeric(data_pos[,2]))
        normParams_neg <- get_normal_parameters2(as.numeric(data_neg[,2]))
      }
      else {
        normParams_pos <- get_normal_parameters2(data_pos[,1])
        normParams_neg <- get_normal_parameters2(data_neg[,1])
      }
      toxValues <- getToxValues(lengths, normParams_pos, normParams_neg)
    })
    
    try({
      mean_tmp <-getMean(geneBasedData, uGenes, colsToAnalyze[i])
      mean <- c(mean, mean_tmp)
    })
    
    try({
      median_tmp <-getMedian(geneBasedData, uGenes, colsToAnalyze[i])
      median <- c(median, median_tmp)
    })
    
    try({
      ## robust SSMD
      ssmdr_tmp <- getRobustSSMD(geneBasedData, uGenes, colsToAnalyze[i])
      ssmdr <- c(ssmdr, ssmdr_tmp)
    })
    try({
      ## SSMD
      ssmd_tmp <- getSSMD(geneBasedData, uGenes, colsToAnalyze[i])
      ssmd <- c(ssmd, ssmd_tmp)
    })
    
    setwd(graph.path)
    try({
      file <- paste(colsToAnalyze[i],"_", 1, ".pdf", sep="") 
      tt <- plotControls(geneBasedData, sampName, posSamp, thresholdValues[i], colsToAnalyze[i], file, 10, 8)
    })
    
    try({
      file <- paste(colsToAnalyze[i],"_", 2, ".pdf", sep="")
      tt <- barPlots(summaries, geneBasedData, 1, colsToAnalyze[i], sampName, thresholdValues[i], file, 10, 8, countRepPerGene, posSamp)
    })
    
    try({
      file <- paste(colsToAnalyze[i],"_", 3, ".pdf", sep="")
      tt <- plotTransIdx(summaries, infectIdx, colsToAnalyze[i], file, 10, 8)
    })
    
    try({
      file <- paste(colsToAnalyze[i],"_", 4, ".pdf", sep="")
      tt <- plotToxIndex(summaries, toxIndex, colsToAnalyze[i], file, 10, 8)
    })
    
    try({
      file <- paste(colsToAnalyze[i],"_", 5, ".pdf", sep="")
      tt <- spatialSummaryPlot(summaries, plateSetup, sampName, 1, colsToAnalyze[i], file, 10, 8)
    })
    
    try({
      file <- paste(colsToAnalyze[i],"_", 6, ".pdf", sep="")
      tt <- cvPlot(summaries, plateSetup, sampName, 1, colsToAnalyze[i], file, 10, 8)
    })
  }
  
  ## CREATING BIG DATA FRAME FOR RESULTS
  try({
    data_results <- data.frame(cbind(geneRef, columnName), row.names=NULL, stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], geneName), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], plateNames), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], percentValues), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], semPercentValues), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], meanCounts), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], sdCounts), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], totalPvalues), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], totalInfectionIdx), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], totalToxicityIdx), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], mean), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], ssmd), stringsAsFactors=FALSE)
  }) 
  try({
    data_results <- data.frame(cbind(data_results[,], ssmdr), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], median), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], toxValues), stringsAsFactors=FALSE)
  })
  
  ## save plate result in csv
  file <- paste(graph.path, "/PlateResults.csv", sep="")
  write.csv(data_results, file=file)
  
  ##return big data frame results
  return(data_results)
}


######## Calcul performed for every different plate ########
cat("\n\n################ CALCUL PERFORMED ################\n\n")
RES <- foreach(entry=entryNames, .combine="rbind", .inorder=FALSE, .errorhandling = "pass") %dopar% Analyzis(entry)
cat("\n")
print(head(RES))


cat("\n\n################ OUTPUT PROCESSING ################\n\n")
##Save results in csv file and make some graphics

cat("  ### Saving results to csv file ###\n")


# Save TCA result
file <- paste(outputdir, "/TCAResults.csv", sep="")
write.csv(RES, file=file)


close(thres.save)

end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)