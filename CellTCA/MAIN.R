#!/usr/bin/env Rscript
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
cat("    ALL RIGHT RESERVED   KOPP@2014@IGBMC\n")
cat("    FOR HELP USE -h OPTION\n\n")


## IMPORT FOR PACKAGES DEPENDENCY
suppressPackageStartupMessages(library(limma))
suppressPackageStartupMessages(library(prada))
suppressPackageStartupMessages(library(bioDist))
suppressPackageStartupMessages(library(e1071))
suppressPackageStartupMessages(library(DAAG))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(reshape2))
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


## CLI 
option_list <- list (
  make_option(c("-i", "--input"), type="character", help="Input Directory with data files"),
  make_option(c("-o", "--output"), type="character", help="Output Directory where results will be saved"),
  make_option(c("-n", "--neg"), type="character", help="Negative Control in plate"),
  make_option(c("-p", "--pos"), type="character", help="Positive Control in plate"),
  make_option(c("-v", "--tox"), type="character", help="Toxicity Control in plate"),
  make_option(c("-f", "--feat"), type="character", help="Feature to analyze (column in data file"),
  make_option(c("-t", "--thres"), type="integer", help="Threshold for considering cell as positive : [default %default] ", default=NA),
  make_option(c("-m", "--median"), action="store_true", help="Median pooling of data replicats : [default %default] ", default=FALSE),
  make_option(c("-s", "--svm"), action="store_true", help="SVM processing of data replicats : [default %default]", default=FALSE),
  #   make_option(c("-a", "--adj"), action="store_true", help="Adjust whole screen variance : [default %default]", default=FALSE),
  make_option(c("-j", "--mp"), type="integer", help="Number of core to used : [default %default]", default=1)
)
opt <- parse_args(OptionParser(option_list=option_list))



## import arg
csvDir = opt$input
outputdir = opt$output
dir.create(outputdir)
setwd(outputdir)
pos = as.character(opt$pos)
neg = as.character(opt$neg)
tox = as.character(opt$tox)
Threshold.ref = opt$thres
colAnalyze <- c(opt$feat) 
median.processing <- opt$median
SVM.processing <- opt$svm
# adj.var <- option$adj
nb.process <- opt$mp

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
# writeLines(paste("ADJUSTING DATA VARIANCE : ",adj.var, sep=""), con=fileConn, sep = "\n")
writeLines(paste("SVM PROCESSING DATA : ",SVM.processing, sep=""), con=fileConn, sep = "\n")
close(fileConn)



#setup parallel backend to use X processors
registerDoMC(nb.process) #change the X to your number of CPU cores


## txt file for svm test
SVM_save = file("SVM_Removed_List.txt", "w")
cat("SVM Removed Replicat list",file=SVM_save,sep="\n")

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

## function for Quality control before normalization for each plate
## take in input a entry (RData file with cellTCA object) and give in return a dataframe with QC data
QCAnalyzis <- function(entry) {
  load(paste(outputdir, "/", entry, sep=""))
  plateName <- gsub(".RData", "", gsub("CellTCA_", "", entry))
  # Set positive control geneName
  posSamp <- c(posName=pos) 
  # Layout of the plate 
  plateSetup <- getPlateSetup(cellTCA, 1)
  # Negative control geneName
  sampName <- getRefSamp(cellTCA)
  ## Get Well/Gene name
  uGenes <- getUniqueGeneNames(cellTCA)
  QC.data <- c(); data <- c(); data2 <- c()
  
  graph.path <- paste(outputdir, plateName,sep="/")
  dir.create(graph.path)
  ## Change current dir
  setwd(graph.path)
  
  # QC (Quality Control) Validation data
  cat("    ######## QUALITY CONTROL :\"",entry,"\"########\n")
  for (i in 1:getNumberOfReplicates(cellTCA)) {
    plate <- paste(plateName, i, sep="")
    genebaseddata_tmp <- getGeneBasedData(cellTCA, i)
    tmp <- getQCData(genebaseddata_tmp, plate, sampName, posSamp, colAnalyze[1], uGenes)
    try({      
      replicatBoxplot(genebaseddata_tmp, paste("Replicat_", i, "_withoutExtrem.pdf", sep=""), graph.path)
      replicatBoxplotAll(genebaseddata_tmp, paste("Replicat_", i,".pdf", sep=""), graph.path)
    })
    
    # Mann-Whitney test to check that positive control distribution is significantly greater than
    # negative control distribution
    mwPvalues <- getMannWhitneyPvalues_c(genebaseddata_tmp, sampName, posSamp, colAnalyze[1])
    if (mwPvalues > 0.05) {
      comment <- "Warning !!! Neg and Pos controls have identical distribution"
    } else {
      comment <- "Neg and Pos controls have non indentical distribution "
    }
    tmp2 <- c(tmp, mwPvalues, comment)
    data <- rbind(data, tmp2)
    #data <- rbind(data, tmp)
  }
  QC.data <- data
  colnames(QC.data) <- c("Plate", "SN", "Zfactor", "Zprimefactor","SSMD", "Pvalue", "Observation")
  return(QC.data)
}



## function for analyzis each plate
## take in input a entry (RData file with cellTCA object) and give in return a dataframe with results data
Analyzis <- function(entry) {
  ### Create some variable
  geneRef <- c(); columnName <- c(); geneName <- c(); percentValues <- c(); semPercentValues <- c()
  plateNames <- c(); meanCounts <- c(); sdCounts <- c(); totalPvalues <- c(); totalInfectionIdx <- c()
  totalToxicityIdx <- c(); totalMwPvalues <- c(); controls <- c()
  zscore <- c();zscorer <- c(); ssmd <- c(); ssmdr <- c(); mad <- c(); control_norm <- c(); control_normR <- c()
  log_zscorer <- c(); log_ssmdr <- c(); log_control_normR <- c(); bscore.norm.ssmdr <- c(); bscorelog.norm.ssmdr <- c()
  mean <- c()
  median <- c();bscorelog.norm.foldchanger.log <- c();bscore.norm.foldchanger <-c()
  bscore.norm.meancount <-c(); bscore.norm.percentvalue <-c(); bscore.norm.totaltoxicity <-c(); bscore.norm.totalinfection <-c()
  gene.well.position <- c()
  
  
  
  highFisherFdrValues <- c();  lowFisherFdrValues <- c()
  countHighFisherTargetValues <- c(); countLowFisherTargetValues <- c()
  highRel_riskFdrValues <- c(); lowRel_riskFdrValues <- c();  relativeRiskValues <- c()
  oddsRatioValues <- c(); highOddsRatioFdrValues <- c(); lowOddsRatioFdrValues <- c()
  probValues <- c(); relativeProbMMValues <- c(); highRelativeProbMMFdrValues <- c(); 
  lowRelativeProbMMFdrValues <- c(); probOddsRatioMMValues <- c()
  highProbOddsRatioMMFdrValues <- c(); lowProbOddsRatioMMFdrValues <- c()
  highProbOddsRatioMLFdrValues <- c(); lowProbOddsRatioMLFdrValues <- c()  
  predictiveAccuracyValues <- c(); countHighSoftTargetValues <- c()
  countLowSoftTargetValues <- c()
  fisherFdrValues <- c()
  relativeRiskFdrValues <- c() 
  oddsRatioFdrValues <- c()
  relativeProbMMFdrValues <- c() 
  probOddsRatioMMFdrValues <- c()
  
  
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
  if (SVM.processing == T) {
    # Validate gene Data by SVM before normalization
    geneDataLabels <- validateTCAGeneData(cellTCA, TCASVMModel)
    # Run normalization over the data and store it in a form that will make it easy to process
    geneBasedData <- getWellNormGeneBasedDataEnhanced(cellTCA, median=median.processing, log=F, geneDataLabels, SVM_save)
    # Normlalized data with log10 transformation
    geneBasedDatalog <- getWellNormGeneBasedDataEnhanced(cellTCA, median=median.processing, log=T, geneDataLabels, SVM_save)
  }
  else {
    # Run normalization over the data and store it in a form that will make it easy to process
    geneBasedData <- getWellNormGeneBasedData(cellTCA, median=median.processing)
    # Normlalized data with log10 transformation
    geneBasedDatalog <- getWellNormLogGeneBasedData(cellTCA, median=median.processing)
  }
  
  
  
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
    #     gene.well.position_tmp <- getGenes(plateSetup)
    #     colnames(gene.well.position_tmp) <- c("Well", "geneName")
    #     gene.well.position <- rbind(gene.well.position, gene.well.position_tmp)
    #     gene.well.position <- gene.well.position[!duplicated(gene.well.position[,2]),]
    #     gene.well.position <- split(gene.well.position[,1], gene.well.position[,2])
    
    
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
      ## MAD Median Absolute Deviation ( more robust than standard deviation)
      mad_tmp <- c()
      mad_tmp <- getMAD(geneBasedData, uGenes, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-MAD.pdf", sep="")
      plotScore(mad_tmp, file, colsToAnalyze[i], "MAD", plateSetup)
      mad <- c(mad, mad_tmp)
    })
    try({
      ## SSMD
      ssmd_tmp <- getSSMD(geneBasedData, uGenes, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-SSMD.pdf", sep="")
      plotScore(ssmd_tmp, file, colsToAnalyze[i], "SSMD", plateSetup)
      ssmd <- c(ssmd, ssmd_tmp)
    })
    try({
      ## robust SSMD
      ssmdr_tmp <- getRobustSSMD(geneBasedData, uGenes, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-SSMD_r.pdf", sep="")
      plotScore(ssmdr_tmp, file, colsToAnalyze[i], "Robust SSMD", plateSetup)
      ssmdr <- c(ssmdr, ssmdr_tmp)
    })
    try({
      ## log robust SSMD
      log_ssmdr_tmp <- getRobustSSMD(geneBasedDatalog, uGenes, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-SSMD_r_log.pdf", sep="")
      plotScore(log_ssmdr_tmp, file, colsToAnalyze[i], "Robust SSMD log", plateSetup)
      log_ssmdr <- c(log_ssmdr, log_ssmdr_tmp)
    })
    try({
      ## zscore
      zscore_tmp <- getZScore(geneBasedData, uGenes_without_controls, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-zscore.pdf", sep="")
      plotScore(zscore_tmp, file, colsToAnalyze[i], "Zscore", plateSetup)
      zscore <- c(zscore, zscore_tmp)
    })
    try({
      ## robust zscore
      zscorer_tmp <- getRobustZScore(geneBasedData, uGenes_without_controls, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-zscore_r.pdf", sep="")
      plotScore(zscorer_tmp, file, colsToAnalyze[i], "Robust Zscore", plateSetup)
      zscorer <- c(zscorer, zscorer_tmp)
    })
    try({
      ## log robust zscore
      log_zscorer_tmp <- getRobustZScore(geneBasedDatalog, uGenes_without_controls, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-zscore_r_log.pdf", sep="")
      plotScore(log_zscorer_tmp, file, colsToAnalyze[i], "Robust Zscore log", plateSetup)
      log_zscorer <- c(log_zscorer, log_zscorer_tmp)
    })
    try({
      ## control normlization
      control_norm_tmp <- getContNorm(geneBasedData, uGenes, sampName, posSamp, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-control_norm.pdf", sep="")
      plotScore(control_norm_tmp, file, colsToAnalyze[i], "Controle normalization", plateSetup)
      control_norm <- c(control_norm, control_norm_tmp)
    })
    try({
      ## robust control normalization
      control_normR_tmp <- getRobustContNorm(geneBasedData, uGenes, sampName, posSamp, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-control_norm_r.pdf", sep="")
      plotScore(control_normR_tmp, file, colsToAnalyze[i], "RobustControle normalization", plateSetup)
      control_normR <- c(control_normR, control_normR_tmp)
    })
    try({
      ## log robust control normalization
      log_control_normR_tmp <- getRobustContNorm(geneBasedDatalog, uGenes, sampName, posSamp, colsToAnalyze[i])
      file <- paste(colsToAnalyze[i],plateName, "-control_norm_r_log.pdf", sep="")
      plotScore(log_control_normR_tmp, file, colsToAnalyze[i], "RobustControle normalization log", plateSetup)
      log_control_normR <- c(log_control_normR, log_control_normR_tmp)
    })
    try({
      ## B-score 
      bscore_tmp <- getBScoreSSMDr(geneBasedData, plateSetup, colsToAnalyze[i], size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-bscore.norm.ssmdr_plot.pdf", sep="")
      plotScore(bscore_tmp, file, colsToAnalyze[i], "Bscore norm SSMDr", plateSetup)
      bscore.norm.ssmdr <- c(bscore.norm.ssmdr, bscore_tmp)
    })
    try({
      # b-score log
      bscorelog_tmp <- getBScoreSSMDr(geneBasedDatalog, plateSetup, colsToAnalyze[i], size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-bscorelog.norm.ssmdr_plot.pdf", sep="")
      plotScore(bscorelog_tmp, file, colsToAnalyze[i], "Bscore norm log SSMDr", plateSetup)
      bscorelog.norm.ssmdr <- c(bscorelog.norm.ssmdr, bscorelog_tmp)
    })    
    try({
      # robust fold change
      foldchanger_tmp <- getBScoreFoldChange(geneBasedData, plateSetup, colsToAnalyze[i], size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-foldchanger_plot.pdf", sep="")
      plotScore(foldchanger_tmp, file, colsToAnalyze[i], "Robust Fold Change", plateSetup)
      bscore.norm.foldchanger<- c(bscore.norm.foldchanger, foldchanger_tmp)
    })
    try({
      # robust fold change log data
      foldchanger.log_tmp <- getBScoreFoldChange(geneBasedDatalog, plateSetup, colsToAnalyze[i], size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-foldchanger.log_plot.pdf", sep="")
      plotScore(foldchanger.log_tmp, file, colsToAnalyze[i], "Robust fold Change log data", plateSetup)
      bscorelog.norm.foldchanger.log <- c(bscorelog.norm.foldchanger.log, foldchanger.log_tmp)
    })
    try({
      # bscore norm ssmdr on mean count
      meancountssmdr <- getBscoresimpledata(meanCounts, plateSetup, size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-Bscore_meanCounts.pdf", sep="")
      plotScore(meancountssmdr, file, colsToAnalyze[i], "Bscore Norm mean Counts", plateSetup)
      bscore.norm.meancount <- c(bscore.norm.meancount, meancountssmdr)
    })
    try({
      # bscore norm ssmdr on percentvalue
      percentvaluessmdr <- getBscoresimpledata(percentValues, plateSetup, size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-Bscore_percentvalue.pdf", sep="")
      plotScore(percentvaluessmdr, file, colsToAnalyze[i], "Bscore Norm percent value", plateSetup)
      bscore.norm.percentvalue <- c(bscore.norm.percentvalue, percentvaluessmdr)
    })
    try({
      # bscore norm ssmdr on total toxicity idx
      totaltoxicityssmdr <- getBscoresimpledata(totalToxicityIdx, plateSetup, size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-Bscore_totaltoxicity.pdf", sep="")
      plotScore(totaltoxicityssmdr, file, colsToAnalyze[i], "Bscore Norm total toxicity idx", plateSetup)
      bscore.norm.totaltoxicity <- c(bscore.norm.totaltoxicity, totaltoxicityssmdr)
    })
    try({
      # bscore norm ssmdr on total infection idx
      totalinfectionssmdr <- getBscoresimpledata(totalInfectionIdx, plateSetup, size, sampName)
      file <- paste(colsToAnalyze[i],plateName,"-Bscore_totalinfectidx.pdf", sep="")
      plotScore(totalinfectionssmdr, file, colsToAnalyze[i], "Bscore Norm total infection idx", plateSetup)
      bscore.norm.totalinfection <- c(bscore.norm.totalinfection, totalinfectionssmdr)
    })
    
    try({
      mean_tmp <-getMean(geneBasedData, uGenes, colsToAnalyze[i])
      mean <- c(mean, mean_tmp)
    })
    
    try({
      median_tmp <-getMedian(geneBasedData, uGenes, colsToAnalyze[i])
      median <- c(median, median_tmp)
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
    
    ### UNDER HEAVY DEV !!!!!!
    ## don't work with no replicate (i don't know why ...)
    if (getNumberOfReplicates(cellTCA)>1) {
      try({
        controlsData <- getControlsData(geneBasedData, neg, pos)
        logisticModel <- getLogisticModel2(controlsData, colsToAnalyze[i])
        probData <- getProbData(geneBasedData, logisticModel, colsToAnalyze[i])
        geneBasedData@data <- probData 
        predictive.acc <- getPredictivityAccuracy(logisticModel)
        predictiveAccuracyValues <- c(predictiveAccuracyValues, predictive.acc)
        
        # Fisher exact test
        fvalues <- getFisherValues(geneBasedData, sampName, 0.5, colsToAnalyze[i])
        refNames <- row.names(fvalues)
        
        # extract Fisher Values
        fPvalues <- fvalues$fpval_greater
        names(fPvalues) <- refNames
        cfPvalues <- sort(fPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(fPvalues)+1, by=-1)
        highFisherFdrValues <- c(highFisherFdrValues, cfPvalues[refNames])
        countHighFisherTargetValues <- c(countHighFisherTargetValues, length(which(cfPvalues<0.05)))
        fPvalues <- fvalues$fpval_less
        names(fPvalues) <- refNames
        cfPvalues <- sort(fPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(fPvalues)+1, by=-1)
        lowFisherFdrValues <- c(lowFisherFdrValues, cfPvalues[refNames])
        countLowFisherTargetValues <- c(countLowFisherTargetValues, length(which(cfPvalues<0.05)))
        
        # Relative Risk test
        relativeRisk <- getRelativeRiskValues(geneBasedData, sampName, 0.5, colsToAnalyze[i])
        tnames <- row.names(relativeRisk)
        
        relativeRiskVal <- relativeRisk$rr_val
        names(relativeRiskVal) <- tnames
        relativeRiskValues <- c(relativeRiskValues, relativeRiskVal[refNames])
        highRel_riskPvalues <- relativeRisk$rr_pval_high
        names(highRel_riskPvalues) <- tnames
        highRel_riskFdr <- sort(highRel_riskPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(highRel_riskPvalues)+1, by=-1)
        highRel_riskFdrValues <- c(highRel_riskFdrValues, highRel_riskFdr[refNames])
        lowRel_riskPvalues <- relativeRisk$rr_pval_low
        names(lowRel_riskPvalues) <- tnames
        lowRel_riskFdr <- sort(lowRel_riskPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(lowRel_riskPvalues)+1, by=-1)
        lowRel_riskFdrValues <- c(lowRel_riskFdrValues, lowRel_riskFdr[refNames])
        
        # Odds ratio test
        odds_ratio <- relativeRisk$od_val
        names(odds_ratio) <- tnames
        oddsRatioValues <- c(oddsRatioValues, odds_ratio[refNames])
        odds_ratioPvalues <- relativeRisk$od_pval_high
        names(odds_ratioPvalues) <- tnames
        odds_ratioFdr <- sort(odds_ratioPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(odds_ratioPvalues)+1, by=-1)
        highOddsRatioFdrValues <- c(highOddsRatioFdrValues, odds_ratioFdr[refNames])
        odds_ratioPvalues <- relativeRisk$od_pval_low
        names(odds_ratioPvalues) <- tnames
        odds_ratioFdr <- sort(odds_ratioPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(odds_ratioPvalues)+1, by=-1)
        lowOddsRatioFdrValues <- c(lowOddsRatioFdrValues, odds_ratioFdr[refNames])
        
        
        # Get prob values
        probs <- getProbValues(geneBasedData, sampName, colsToAnalyze[i])
        probValues <- c(probValues, probs[refNames])
        
        # Soft MM Relative Risk test (with method of moments)
        rel_probValues <- getRelativeProbValuesMM(geneBasedData, sampName, colsToAnalyze[i])
        rel_probs <- rel_probValues$rr_mm_val
        tnames <- row.names(rel_probValues)
        names(rel_probs) <- tnames
        relativeProbMMValues <- c(relativeProbMMValues, rel_probs[refNames])
        rel_probPvalues <- rel_probValues$rr_mm_pval_high
        names(rel_probPvalues) <- tnames
        rel_probFdr <- sort(rel_probPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(rel_probPvalues)+1, by=-1)
        countHighSoftTargetValues <- c(countHighSoftTargetValues, length(which(rel_probFdr<0.05)))
        highRelativeProbMMFdrValues <- c(highRelativeProbMMFdrValues, rel_probFdr[refNames])
        rel_probPvalues <- rel_probValues$rr_mm_pval_low
        names(rel_probPvalues) <- tnames
        rel_probFdr <- sort(rel_probPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(rel_probPvalues)+1, by=-1)
        lowRelativeProbMMFdrValues <- c(lowRelativeProbMMFdrValues, rel_probFdr[refNames])
        countLowSoftTargetValues <- c(countLowSoftTargetValues, length(which(rel_probFdr<0.05)))
        
        # Soft MM odds ratio test
        prob_odds_ratio <- rel_probValues$od_mm_val
        names(prob_odds_ratio) <- tnames
        probOddsRatioMMValues <- c(probOddsRatioMMValues, prob_odds_ratio[refNames])
        prob_odds_ratioPvalues <- rel_probValues$od_mm_pval_high
        names(prob_odds_ratioPvalues) <- tnames
        prob_odds_ratioFdr <- sort(prob_odds_ratioPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(prob_odds_ratioPvalues)+1, by=-1)
        highProbOddsRatioMMFdrValues <- c(highProbOddsRatioMMFdrValues, prob_odds_ratioFdr[refNames])
        prob_odds_ratioPvalues <- rel_probValues$od_mm_pval_low
        names(prob_odds_ratioPvalues) <- tnames
        prob_odds_ratioFdr <- sort(prob_odds_ratioPvalues) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(prob_odds_ratioPvalues)+1, by=-1)
        lowProbOddsRatioMMFdrValues <- c(lowProbOddsRatioMMFdrValues, prob_odds_ratioFdr[refNames])
        
        fisherFdrValues <- apply(as.data.frame(cbind(highFisherFdrValues, lowFisherFdrValues)), 1, min)
        relativeRiskFdrValues <- apply(as.data.frame(cbind(highRel_riskFdrValues, lowRel_riskFdrValues)), 1, min)
        oddsRatioFdrValues <- apply(as.data.frame(cbind(highOddsRatioFdrValues, lowOddsRatioFdrValues)), 1, min)
        relativeProbMMFdrValues <- apply(as.data.frame(cbind(highRelativeProbMMFdrValues, lowRelativeProbMMFdrValues)), 1, min)
        probOddsRatioMMFdrValues <- apply(as.data.frame(cbind(highProbOddsRatioMMFdrValues, lowProbOddsRatioMMFdrValues)), 1, min)
        
        resNames <- c("Gene", "fisher-fdr", "rel-riskValue", "rel-risk-fdr", "odds-ratioValue", "odds-ratio-fdr", "prValue", "rel-probMM", "rel-probMM-fdr", "prob-oddsRatioMM", "prob-oddsRatioMM-fdr", "column")
        plate.test = data.frame(geneName, fisherFdrValues, relativeRiskValues, relativeRiskFdrValues, oddsRatioValues, oddsRatioFdrValues, probValues, relativeProbMMValues, relativeProbMMFdrValues, probOddsRatioMMValues, probOddsRatioMMFdrValues, columnName)
        colnames(plate.test) <- resNames
        
        ## save plate result in csv
        file <- paste(graph.path, "/Plate_test.csv", sep="")
        write.csv(plate.test, file=file)
        
      })
      
      try({
        tfile <- paste("plotpercentofpositivecells", '_', 7, ".jpg", sep="")
        tt <- plotPercentOfPositiveCells(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 8, 6, countRepPerGene, posSamp, 1)
      })
      try({
        tfile <- paste("plotprobofpositivecells", '_', 8, ".jpg", sep="")
        tt <- plotProbOfPositiveCells(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 8, 6, countRepPerGene, posSamp, 1)
      })
      try({
        tfile <- paste("plotcountrelativeriskvalues", '_', 9, ".jpg", sep="")
        tt <- plotCountRelativeRiskValues(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 8, 6, countRepPerGene, posSamp, 1)
      })
      try({
        tfile <- paste("plotprobrelativeriskvalue", '_', 10, ".jpg", sep="")
        tt <- plotProbRelativeRiskValues(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 8, 6, countRepPerGene, posSamp, 1)
      })
      try({
        tfile <- paste("plotrelativeriskspatialsummary", '_', 11, ".jpg", sep="")
        tt <- plotRelativeRiskSpatialSummary(summaries, geneBasedData, plateSetup, sampName, i, colsToAnalyze[i], 0.5, tfile, 8, 6, 1)
      })
      try({
        tfile <- paste("plotprobrelativeriskspatialsummary", '_', 12, ".jpg", sep="")
        tt <- plotProbRelativeRiskSpatialSummary(summaries, geneBasedData, plateSetup, sampName, i, colsToAnalyze[i], 0.5, tfile, 8, 6, 1)
      })
    }
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
    data_results <- data.frame(cbind(data_results[,], bscore.norm.percentvalue), stringsAsFactors=FALSE)
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
    data_results <- data.frame(cbind(data_results[,], bscore.norm.meancount), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], totalPvalues), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], totalInfectionIdx), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], bscore.norm.totalinfection), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], totalToxicityIdx), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], bscore.norm.totaltoxicity), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], mad), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], ssmd), stringsAsFactors=FALSE)
  }) 
  try({
    data_results <- data.frame(cbind(data_results[,], ssmdr), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], bscore.norm.ssmdr), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], mean), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], bscore.norm.foldchanger), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], median), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], zscore), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], zscorer), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], control_norm), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], control_normR), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], log_zscorer), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], log_ssmdr), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], bscorelog.norm.ssmdr), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], bscorelog.norm.foldchanger.log), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], log_control_normR), stringsAsFactors=FALSE)
  })
  try({
    data_results <- data.frame(cbind(data_results[,], toxValues), stringsAsFactors=FALSE)
  })
  if (getNumberOfReplicates(cellTCA)>1) {
    try({
      data_results <- data.frame(cbind(data_results[,], fisherFdrValues), stringsAsFactors=FALSE)
    })
    try({
      data_results <- data.frame(cbind(data_results[,], relativeRiskFdrValues), stringsAsFactors=FALSE)
    })
    try({
      data_results <- data.frame(cbind(data_results[,], oddsRatioFdrValues), stringsAsFactors=FALSE)
    })
    try({
      data_results <- data.frame(cbind(data_results[,], relativeProbMMFdrValues), stringsAsFactors=FALSE)
    })
    try({
      data_results <- data.frame(cbind(data_results[,], probOddsRatioMMFdrValues), stringsAsFactors=FALSE)
    })
  }
  #   try({
  #     data_results <- data.frame(cbind(data_results[,], gene.well.position), stringsAsFactors=FALSE)
  #   })
  
  ## save plate result in csv
  file <- paste(graph.path, "/PlateResults.csv", sep="")
  write.csv(data_results, file=file)
  
  ##return big data frame results
  return(data_results)
}


######## Calcul performed for every different plate ########
cat("\n\n################ CALCUL PERFORMED ################\n\n")
QC.data <- foreach(entry=entryNames, .combine="rbind", .inorder=FALSE, .errorhandling = "pass") %dopar%  QCAnalyzis(entry)
print(head(QC.data))


#adj.var.value <- NormalizePlate(entryNames)


RES <- foreach(entry=entryNames, .combine="rbind", .inorder=FALSE, .errorhandling = "pass") %dopar% Analyzis(entry)
cat("\n")
print(head(RES))


cat("\n\n################ OUTPUT PROCESSING ################\n\n")
##Save results in csv file and make some graphics

cat("  ### Saving results to csv file ###\n")


# Save TCA result
file <- paste(outputdir, "/TCAResults.csv", sep="")
write.csv(RES, file=file)




# Quality Control Output
cat("  ### Quality Control graphics output###\n")
row.names(QC.data) <- NULL
QC.data <- as.data.frame(QC.data)
file <- paste(outputdir, "/QC.csv", sep="")
write.csv(QC.data, file=file)

xdata <- read.csv(file, header = T, check.names=F)

try({
  xdata2 <- xdata[,2:6]
  xdata2.m <- melt(xdata2)
  p <- ggplot(xdata2.m, aes(Plate, value, color = variable)) + geom_point() + geom_line(aes(group=variable)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  ggsave(filename="QC_charts.pdf", plot=last_plot(), path=outputdir, width=16, height=12, dpi=300)
})
try({
  xdata3 <- cbind(xdata[2], xdata[3])
  xdata3.m <- melt(xdata3)
  p <- ggplot(xdata3.m, aes(Plate, value, color = variable)) + geom_point() + geom_line(aes(group=variable)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  ggsave(filename="QC_sn.pdf", plot=last_plot(), path=outputdir, width=16, height=12, dpi=300)
})
try({
  xdata4 <- cbind(xdata[2], xdata[4])
  xdata4.m <- melt(xdata4)
  p <- ggplot(xdata4.m, aes(Plate, value, color = variable)) + geom_point() + geom_line(aes(group=variable)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  ggsave(filename="QC_zfactor.pdf", plot=last_plot(), path=outputdir, width=16, height=12, dpi=300)
})
try({
  xdata5 <- cbind(xdata[2], xdata[5])
  xdata5.m <- melt(xdata5)
  p <- ggplot(xdata5.m, aes(Plate, value, color = variable)) + geom_point() + geom_line(aes(group=variable)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  ggsave(filename="QC_zprimefactor.pdf", plot=last_plot(), path=outputdir, width=16, height=12, dpi=300)
})
try({
  xdata6 <- cbind(xdata[2], xdata[6])
  xdata6.m <- melt(xdata6)
  p <- ggplot(xdata6.m, aes(Plate, value, color = variable)) + geom_point() + geom_line(aes(group=variable)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  ggsave(filename="QC_ssmd.pdf", plot=last_plot(), path=outputdir, width=16, height=12, dpi=300)
})

try({
  ## get gene counts classified by effect sizes
  cat("  ### Genes counts classified by effect sizes ###\n\n")
  feature <- "bscore.norm.ssmdr"
  GeneEffCount <- data.frame(Type=c("Upregulated"), Effect.Classes=c(paste(feature," >= 5", sep="")), Effect.Cutoffs=c("Extremely Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 5,0))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("5 > ", feature," => 3", sep="")), Effect.Cutoffs=c("Very Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr > 3.0 & bscore.norm.ssmdr < 5.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("3 > ", feature," >= 2", sep="")), Effect.Cutoffs=c("Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 2.0 & bscore.norm.ssmdr< 3.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("2 > ", feature," >= 1.645", sep="")), Effect.Cutoffs=c("Fairly Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 1.645 & bscore.norm.ssmdr < 2.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1.645 > ", feature," >= 1.28", sep="")), Effect.Cutoffs=c("Moderate"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 1.28 & bscore.norm.ssmdr < 1.645 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1.28 > ", feature," >= 1", sep="")), Effect.Cutoffs=c("Fairly Moderate"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 1 & bscore.norm.ssmdr < 1.28 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1 > ", feature," >= 0.75", sep="")), Effect.Cutoffs=c("Fairly Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 0.75 & bscore.norm.ssmdr < 1 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.75 > ", feature," >= 0.5", sep="")), Effect.Cutoffs=c("Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 0.5 & bscore.norm.ssmdr < 0.75 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.5 > ", feature," >= 0.25", sep="")), Effect.Cutoffs=c("Very Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 0.25 & bscore.norm.ssmdr < 0.5 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.25 > ", feature," >= 0", sep="")), Effect.Cutoffs=c("Extremely Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= 0 & bscore.norm.ssmdr < 0.25 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("zero"), Effect.Classes=c("=0"), Effect.Cutoffs=c("no effect"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr == 0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("0 > ", feature," >= -0.25", sep="")), Effect.Cutoffs=c("Extremely Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -0.25 & bscore.norm.ssmdr < 0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.25 > ", feature," >= -0.5", sep="")), Effect.Cutoffs=c("Very Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -0.5 & bscore.norm.ssmdr < -0.25 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.5 > ", feature," >= -0.75", sep="")), Effect.Cutoffs=c("Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -0.75 & bscore.norm.ssmdr < -0.5 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.75 > ", feature," >= -1", sep="")), Effect.Cutoffs=c("Fairly Weak"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -1 & bscore.norm.ssmdr < -0.75 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1 > ", feature," >= -1.28", sep="")), Effect.Cutoffs=c("Fairly Moderate"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -1.28 & bscore.norm.ssmdr < -1 )))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1.28 > ", feature," >= -1.645", sep="")), Effect.Cutoffs=c("Moderate"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -1.645 & bscore.norm.ssmdr < -1.28)))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1.645 > ", feature," >= -2", sep="")), Effect.Cutoffs=c("Fairly Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -2 & bscore.norm.ssmdr < -1.645 )))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-2 > ", feature," >= -3", sep="")), Effect.Cutoffs=c("Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -3 & bscore.norm.ssmdr < -2 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-3 > ", feature," >= -5", sep="")), Effect.Cutoffs=c("Very Strong"), Counts=c(nrow(subset(RES,bscore.norm.ssmdr >= -5 & bscore.norm.ssmdr < -3 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste(feature, "> -5", sep="")), Effect.Cutoffs=c("Extremely Strong"), Counts=c(nrow(subset(RES, bscore.norm.ssmdr < -5 )))) )
  
  print(GeneEffCount)
  file <- paste(outputdir, "/GeneEffectCounts.csv", sep="")
  write.table(GeneEffCount, file=file, col.names=TRUE, sep=",")
  cat("\n")
  
  feature <- "bscorelog.norm.ssmdr"
  GeneEffCount <- data.frame(Type=c("Upregulated"), Effect.Classes=c(paste(feature," >= 5", sep="")), Effect.Cutoffs=c("Extremely Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 5,0))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("5 > ", feature," => 3", sep="")), Effect.Cutoffs=c("Very Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr > 3.0 & bscorelog.norm.ssmdr < 5.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("3 > ", feature," >= 2", sep="")), Effect.Cutoffs=c("Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 2.0 & bscorelog.norm.ssmdr< 3.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("2 > ", feature," >= 1.645", sep="")), Effect.Cutoffs=c("Fairly Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 1.645 & bscorelog.norm.ssmdr < 2.0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1.645 > ", feature," >= 1.28", sep="")), Effect.Cutoffs=c("Moderate"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 1.28 & bscorelog.norm.ssmdr < 1.645 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1.28 > ", feature," >= 1", sep="")), Effect.Cutoffs=c("Fairly Moderate"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 1 & bscorelog.norm.ssmdr < 1.28 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("1 > ", feature," >= 0.75", sep="")), Effect.Cutoffs=c("Fairly Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 0.75 & bscorelog.norm.ssmdr < 1 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.75 > ", feature," >= 0.5", sep="")), Effect.Cutoffs=c("Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 0.5 & bscorelog.norm.ssmdr < 0.75 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.5 > ", feature," >= 0.25", sep="")), Effect.Cutoffs=c("Very Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 0.25 & bscorelog.norm.ssmdr < 0.5 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Upregulated"), Effect.Classes=c(paste("0.25 > ", feature," >= 0", sep="")), Effect.Cutoffs=c("Extremely Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= 0 & bscorelog.norm.ssmdr < 0.25 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("zero"), Effect.Classes=c("=0"), Effect.Cutoffs=c("no effect"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr == 0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("0 > ", feature," >= -0.25", sep="")), Effect.Cutoffs=c("Extremely Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -0.25 & bscorelog.norm.ssmdr < 0 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.25 > ", feature," >= -0.5", sep="")), Effect.Cutoffs=c("Very Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -0.5 & bscorelog.norm.ssmdr < -0.25 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.5 > ", feature," >= -0.75", sep="")), Effect.Cutoffs=c("Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -0.75 & bscorelog.norm.ssmdr < -0.5 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-0.75 > ", feature," >= -1", sep="")), Effect.Cutoffs=c("Fairly Weak"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -1 & bscorelog.norm.ssmdr < -0.75 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1 > ", feature," >= -1.28", sep="")), Effect.Cutoffs=c("Fairly Moderate"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -1.28 & bscorelog.norm.ssmdr < -1 )))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1.28 > ", feature," >= -1.645", sep="")), Effect.Cutoffs=c("Moderate"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -1.645 & bscorelog.norm.ssmdr < -1.28)))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-1.645 > ", feature," >= -2", sep="")), Effect.Cutoffs=c("Fairly Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -2 & bscorelog.norm.ssmdr < -1.645 )))))
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-2 > ", feature," >= -3", sep="")), Effect.Cutoffs=c("Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -3 & bscorelog.norm.ssmdr < -2 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste("-3 > ", feature," >= -5", sep="")), Effect.Cutoffs=c("Very Strong"), Counts=c(nrow(subset(RES,bscorelog.norm.ssmdr >= -5 & bscorelog.norm.ssmdr < -3 )))) )
  GeneEffCount <- rbind(GeneEffCount, data.frame(Type=c("Downregulated"), Effect.Classes=c(paste(feature, "> -5", sep="")), Effect.Cutoffs=c("Extremely Strong"), Counts=c(nrow(subset(RES, bscorelog.norm.ssmdr < -5 )))) )
  
  print(GeneEffCount)
  file <- paste(outputdir, "/GeneEffectCounts.csv", sep="")
  write.table(GeneEffCount, file=file, col.names=FALSE, sep=",", append=TRUE)
  cat("\n")
  
})
close(SVM_save)
close(thres.save)

end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)