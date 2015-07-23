## Script with Principal Component Analyzis (PCA)
start.time <- Sys.time()

source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCAMetaInfo.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCAPlateSetup.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCADataInfo.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCASummaries.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCAGeneBasedData.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCAData.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCAReplicate.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCAUtilities.R")
source("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/CellTCA.R")
source("/home/akopp/PROJECT/CellTCA/Core/TCAcsv.R")
load("/home/akopp/PROJECT/CellTCA/LIB/LIBcelltca/TCASVMModel.Rd")
templateDir <- "/home/akopp/PROJECT/CellTCA/templates"

if (! require(limma))
  stop("limma library is required to go any further.")
if (! require(prada))
  stop("prada library is required to go any further.")
if (! require(xtable))
  stop("xtable library is required to go any further.")
if (! require(grid))
  stop("grid library is required to go any further.")
if (! require(bioDist))
  stop("bioDist library is required to go any further.")
if (! require(e1071))
  stop("e1071 library is required to go any further.")
if (! require(DAAG))
  stop("DAAG library is required to go any further.")
if (! require(fitdistrplus))
  stop("fitdistrplus library is required to go any further.")




## VERSION WITH CONTROL


mywarnings <- as.character()
in.pathFile <-"/home/akopp/Bureau/test" # PARAM HERE !!!!!!!!!!!!
out.file <-"/home/akopp/Bureau/result_test_CELL" # PARAM HERE !!!!!!!!!!!!
dir.create(out.file)
in.file <-rev(unlist(strsplit(as.character(in.pathFile), "/")))[1]
idir <- in.pathFile
odir <- out.file
setwd(odir) 
colAnalyze <- "AvgIntensity" # PARAM HERE !!!!!!!!!!!!


descriptionFile <- as.character("/home/akopp/Bureau/test/descrition.txt")
multiParametric <- as.integer(1)
reportFilename <- as.character("/home/akopp/Bureau/result_test_CELL/report.html")
negSamp <- as.character("NT")
posSamp <- as.character("B1")
toxSamp <- as.character("B1")
negControlRef <- as.integer("NT")
posControlRef <- as.integer("B1")
toxControlRef <- as.integer("B1")


if (multiParametric) {
  if (! require(FactoMineR))
    stop("FactoMineR library is required to go any further.")
}

if (negSamp == "")
  stop("No negative sample name found")

if (toxSamp == "")
  stop("No toxicity sample name found")

if (posSamp == "")
  stop("No positive sample name found") 

# if (negControlRef) {
#   sampName <- negSamp
# } else if (posControlRef) {
#   sampName <- posSamp
# } else if (toxControlRef) {
#   sampName <- toxSamp
# } else {
#   stop("No reference found for selection.")
# }

sampName <- negSamp

controlValues <- c(); geneNameValues <- c(); 
negControlCellCountValues <- c(); posControlCellCountValues <- c()
tcaIdx <- 0; plateNameValues <- c(); meanCellCountValues <- c(); sdCellCountValues <- c()
cellCountPerWellValues <- c(); columnValues <- c()
precision <- 0.05; selectedColumns <- c(1, 14, 13, 6, 11, 7)
normalApproxSampleNumber <- 5000; geneNumberPerPlate <- 60
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



#redo = F check if data is already process
#redo = T make process is all case
#### Generate CellTCA data ####
readCSVDir(idir, odir, redo=T, refSamp=negSamp, refThr=95, colAnalyze) # PARAM HERE !!!!!!!!!!!!
entryNames <- dir(path=odir, pattern="RData")

dataFound = 1
if (length(entryNames) == 0) {
  dataFound = 0
}

cat("\n !!!!!!  Checkpoint1 !!!!!!  \n\n")

resultsDirName <- "results"

#### copying all necessary files into html folder (css, js, gifs...)
#cpfiles <- dir(file.path(templateDir, "css"), full=TRUE)
dir_tmp <- file.path(templateDir, "css/")
to_dir <- file.path(odir, "css/")
system(paste("cp -r",dir_tmp,to_dir))
#successVal <- file.copy(from=cpfiles, to=file.path(odir, "css"), overwrite=TRUE)

#cpfiles <- dir(file.path(templateDir, "img"), full=TRUE)
dir_tmp <- file.path(templateDir, "img")
to_dir <- file.path(odir, "img/")
system(paste("cp -r",dir_tmp,to_dir))
#successVal <- file.copy(from=cpfiles, to=file.path(odir, "img"), overwrite=TRUE)

descriptionTxtFile <- descriptionFile
descriptionHtmlFile <- file.path(odir, "index.html")
headerHtmlFile <- file.path(templateDir, "header.html")
bottomHtmlFile <- file.path(templateDir, "bottom.html")
description2html(descriptionTxtFile, descriptionHtmlFile, headerHtmlFile, bottomHtmlFile)

nPlates <- length(entryNames)
plateListHtmlFile <- file.path(odir, 'plateList.html')
plateList2html(nPlates, plateListHtmlFile, headerHtmlFile, bottomHtmlFile)

dir.create(file.path(odir, resultsDirName), showWarnings=FALSE)
resultsHtmlFile <- file.path(odir, "screenresults.html")
highTargetsHtmlFile <- file.path(odir, "highTargets.html")
lowTargetsHtmlFile <- file.path(odir, "lowTargets.html")
rawResultsFile <- file.path(odir, resultsDirName, "raw_results.csv")
highResultsFile <- file.path(odir, resultsDirName, "high_targets_genes.csv")
lowResultsFile <- file.path(odir, resultsDirName, "low_targets_genes.csv")


#### Data Processing Parts
tcaIdx <- 0
nImages <- 6

cat("\n !!!!!!  Checkpoint2 !!!!!!  \n\n")

for (entry in entryNames){
  # keep trak of input file being processed
  tcaIdx <- tcaIdx + 1
  plateDirName <- paste('p', paste(rep('0', 5-nchar(tcaIdx)), collapse=""), tcaIdx, sep="")
  dir.create(file.path(odir, plateDirName), showWarning=FALSE)
  plateHtmlFile <- file.path(odir, plateDirName, paste(plateDirName, ".html", sep=""))
  plateDirImg <- file.path(odir, plateDirName, plateDirName)
  # load data file
  cat("\n !!!!!!  Checkpoint3 !!!!!!  \n\n")
  load(paste(odir, "/", entry, sep=""))
  plateName <- gsub(".RData", "", gsub("CellTCA_", "", entry))
  cat("\n !!!!!!  Checkpoint4 !!!!!!  \n\n")
  # Get control names
  controlValues <- c(controlValues, getControls(cellTCA))
  
  # Set positive control geneName
  #sampName <- getRefSamp(cellTCA)
  #posSamp <- c(posName="PSMB1-2")
  #posSamp <- c(posName="GFP")
  #toxSamp <- c(toxSamp="PLK1")
  #toxSamp <- c(toxSamp="PLK1 non trait\E9")
  # Modif to take into account
  #negSamp <- sampName
  #negSamp <- posSamp
  
  # layout of plate
  plateSetup <- getPlateSetup(cellTCA, 1)
  
  # Negative control geneName
  #sampName <- getRefSamp(cellTCA)
  #negSamp <- sampName
  
  # Validate gene Data by SVM before normalization
  #geneDataLabels <- validateTCAGeneData(cellTCA, TCASVMModel)
  
  # Read columns of the data labeled for analyzing, If there are more than one column
  # each column will be analyzed separately
  colsToAnalyze <- sort(getModColumnNamesToAnalyze(cellTCA))
  
  cat("\n !!!!!!  Checkpoint3 !!!!!!  \n\n")
  
  # Run normalization over the data and store it in a form that will make it easy to process
  #geneBasedData <- getWellNormGeneBasedData(cellTCA, geneDataLabels)
  if (multiParametric) { 
    geneBasedData <- getSimpleWellPCANormGeneBasedData(cellTCA, colsToAnalyze)
  }  
  else {
    geneBasedData <- getSimpleWellNormGeneBasedDataNew(cellTCA)
  }
  mwPvalues <- getMannWhitneyPvalues_c(geneBasedData, negSamp, posSamp, colsToAnalyze)
  cat("\nPlate : \"",entry,"\"\n")
  cat("Mann Witney P Values :  \"", mwPvalues, "\"\n")
  if (mwPvalues > 0.05) {
    cat("Warning !!! Neg and Pos controls have identical distribution \n\n")
  } else {
    cat("Neg and Pos controls have non indentical distribution \n\n")
  }
  
  if (multiParametric) {
    pcaInputData <- getPCAInputData(geneBasedData, negSamp, posSamp)
    responseInd <- which(names(pcaInputData)=="Response")
    posAndNegCenter <- colMeans(pcaInputData[, -responseInd])
    pcaData <- PCA(pcaInputData[, -responseInd], scale.unit=FALSE, graph=FALSE, ncp=length(colsToAnalyze))  
    nComp <- getOptimalPrincipalComponents(pcaInputData, pcaData)
    predictive.acc <- nComp[1]
    nComp <- nComp[-1]
    logisticModel <- getLogisticModel(pcaInputData, pcaData, nComp)
    pcaGeneBasedData <- getPCAGeneBasedData(geneBasedData, pcaData, nComp, colsToAnalyze, posAndNegCenter)
    probData <- getPCAProbData(pcaGeneBasedData, logisticModel)
    geneBasedData@data <- probData
    oldColsToAnalyze <- colsToAnalyze
    colsToAnalyze <- 'Comp'
  } 
  else {
    controlsData <- getControlsData(geneBasedData, negSamp, posSamp)
    logisticModel <- getLogisticModel2(controlsData, colsToAnalyze)
    probData <- getProbData(geneBasedData, logisticModel, colsToAnalyze)
    geneBasedData@data <- probData 
    predictive.acc <- getPredictivityAccuracy(logisticModel) 
  }
  predictiveAccuracyValues <- c(predictiveAccuracyValues, predictive.acc) 
  
  # Generate summaries from the data
  summaries <- getSummaries(geneBasedData, colsToAnalyze)
  
  # Keep track of number of replicates per gene
  countRepPerGene <- getNumberOfReplicatesPerGene(cellTCA)
  countRepPerGene <- countRepPerGene[which(!is.na(countRepPerGene))]
  
  meanSdCellCounts <- getMeanAndSdCellCounts(cellTCA)
  
  for (i in 1:(length(colsToAnalyze))) {
    
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
    
    # Number of cell per well for toxicity evaluation
    cellCountPerWell <- getLengthSummary(summaries, i)
    #nCellCountPerWell <- floor(cellCountPerWell / countRepPerGene[names(cellCountPerWell)])
    
    # Cannot see any use for  now
    maxCellCount <- max(cellCountPerWell)
    minCellCount <- min(cellCountPerWell)
    meanCellCountValues <- c(meanCellCountValues, mean(cellCountPerWell))
    sdCellCountValues <- c(sdCellCountValues, sd(cellCountPerWell))
    
    # Keep track of all gene names for final results
    geneNameValues <- c(geneNameValues, refNames)
    columnValues <- c(columnValues, rep(colsToAnalyze[i], length(refNames)))
    
    #negativeControlNameValues <- c(negativeControlNameValues, rep(sampName, length(refNames)))
    #columnName <- c(columnName, rep(colsToAnalyze[i], length(refNames)))
    plateNameValues <- c(plateNameValues, rep(plateName, length(refNames)))
    
    
    # Keep track of cell counts
    cellCountPerWellValues <- c(cellCountPerWellValues, cellCountPerWell[refNames])
    negControlCellCountValues <- c(negControlCellCountValues, cellCountPerWell[negSamp])
    posControlCellCountValues <- c(posControlCellCountValues, cellCountPerWell[toxSamp])
    
    tfile <- paste(plateDirImg, '_', 1, ".jpg", sep="")
    tt <- plotPercentOfPositiveCells(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 7, 5, countRepPerGene, posSamp, 1)
    
    tfile <- paste(plateDirImg, '_', 2, ".jpg", sep="")
    tt <- plotProbOfPositiveCells(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 7, 5, countRepPerGene, posSamp, 1)
    
    tfile <- paste(plateDirImg, '_', 3, ".jpg", sep="")
    tt <- plotCountRelativeRiskValues(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 7, 5, countRepPerGene, posSamp, 1)
    
    tfile <- paste(plateDirImg, '_', 4, ".jpg", sep="")
    tt <- plotProbRelativeRiskValues(summaries, geneBasedData, i, colsToAnalyze[i], sampName, 0.5, tfile, 7, 5, countRepPerGene, posSamp, 1)
    
    tfile <- paste(plateDirImg, '_', 5, ".jpg", sep="")
    tt <- plotRelativeRiskSpatialSummary(summaries, geneBasedData, plateSetup, sampName, i, colsToAnalyze[i], 0.5, tfile, 7, 5, 1)
    
    tfile <- paste(plateDirImg, '_', 6, ".jpg", sep="")
    tt <- plotProbRelativeRiskSpatialSummary(summaries, geneBasedData, plateSetup, sampName, i, colsToAnalyze[i], 0.5, tfile, 7, 5, 1)
    
    #tfile <- paste(colsToAnalyze[i], 2+(tcaIdx-1)*nImages, ".pdf", sep="")
    #tt <- barPlots(summaries, geneBasedData, i, colsToAnalyze[i], sampName, thresholds[i], tfile, 7, 5, countRepPerGene, posSamp, 1)
    
    #tfile <- paste(colsToAnalyze[i], 3+(tcaIdx-1)*nImages, ".pdf", sep="")
    #tt <- plotPercentOfControl(summaries, percentOfControl, colsToAnalyze[i], tfile, 7, 5, 1)
    
    #tfile <- paste(colsToAnalyze[i], 4+(tcaIdx-1)*nImages, ".pdf", sep="")
    #tt <- plotSummary(summaries, i, colsToAnalyze[i], sampName, thresholds[i], tfile, 7, 5, 1)
    
    #tfile <- paste(colsToAnalyze[i], 5+(tcaIdx-1)*nImages, ".pdf", sep="")
    #tt <- spatialSummaryPlot(summaries, plateSetup, sampName, i, colsToAnalyze[i], tfile, 7, 5, 1)
    
    #tfile <- paste(colsToAnalyze[i], 6+(tcaIdx-1)*nImages, ".pdf", sep="")
    #tt <- cvPlot(summaries, plateSetup, sampName, i, colsToAnalyze[i], tfile, 7, 5, 1)
    
  }
  plate2html(plateDirName, getContent(plateSetup), plateHtmlFile, headerHtmlFile, bottomHtmlFile)
}

array_ncol <- ncol(getContent(plateSetup))
array_nrow <- nrow(getContent(plateSetup))

# print(posControlCellCountValues)
# Normal parameters for toxicity evaluation
normParams_pos <- get_normal_parameters(posControlCellCountValues)
normParams_neg <- get_normal_parameters(negControlCellCountValues)
toxValues <- getToxValues(cellCountPerWellValues, normParams_pos, normParams_neg)
zfactor <- getZfactor(normParams_pos, normParams_neg)
zfactor <- rep(zfactor, length(toxValues))

fisherFdrValues <- apply(as.data.frame(cbind(highFisherFdrValues, lowFisherFdrValues)), 1, min)
relativeRiskFdrValues <- apply(as.data.frame(cbind(highRel_riskFdrValues, lowRel_riskFdrValues)), 1, min)
oddsRatioFdrValues <- apply(as.data.frame(cbind(highOddsRatioFdrValues, lowOddsRatioFdrValues)), 1, min)
relativeProbMMFdrValues <- apply(as.data.frame(cbind(highRelativeProbMMFdrValues, lowRelativeProbMMFdrValues)), 1, min)
probOddsRatioMMFdrValues <- apply(as.data.frame(cbind(highProbOddsRatioMMFdrValues, lowProbOddsRatioMMFdrValues)), 1, min)

resNames <- c("Gene", "fisher-fdr", "rel-riskValue", "rel-risk-fdr", "odds-ratioValue", "odds-ratio-fdr", "prValue", "rel-probMM", "rel-probMM-fdr", "prob-oddsRatioMM", "prob-oddsRatioMM-fdr", "viability", "zfactor", "column", "plateName")
resValues = data.frame(geneNameValues, fisherFdrValues, relativeRiskValues, relativeRiskFdrValues, oddsRatioValues, oddsRatioFdrValues, probValues, relativeProbMMValues, relativeProbMMFdrValues, probOddsRatioMMValues, probOddsRatioMMFdrValues, toxValues, zfactor, columnValues, plateNameValues)
colnames(resValues) <- resNames
write.csv(resValues, file=rawResultsFile, quote=FALSE)

controls <- c(unique(controlValues), "vide")
columns <- unique(as.vector(resValues$column))
# No need to consider all the columns to calculate cell counts
count_t <- cellCountPerWellValues[which(columnValues==columns[1])]
samples <- setdiff(geneNameValues, controls)
sample_counts <- count_t[which(names(count_t) %in% samples)]

screenSummaryHtmlFile <- file.path(odir, 'screensummary.html')
screensummary2html(screenSummaryHtmlFile, headerHtmlFile, bottomHtmlFile)

#tfile <- "zfactor_plot.pdf"
tfile <- paste(odir, "/zfactor.jpg", sep="")
tt <- plotZfactor(normalApproxSampleNumber, normParams_pos, normParams_neg, sample_counts, tfile, 7, 5, 1)

tfile <- paste(odir, "/predictive_acc.jpg", sep="")
xlabel <- "Plate Number"
ylabel <- "Predictive accuracy"
tt <- plotPredictiveAcc(predictiveAccuracyValues, tfile, xlabel, ylabel)

tfile <- paste(odir, "/positive_genes_pp.jpg", sep="")
xlabel <- "Plate Number"
ylabel <- "Number of Target Genes Found"
tt <- plotTargetGenePerPlate(countHighFisherTargetValues, tfile, xlabel, ylabel)

tfile <- paste(odir, "/positive_genes_pp_soft.jpg", sep="")
xlabel <- "Plate Number"
ylabel <- "Number of Target Genes Found"
tt <- plotTargetGenePerPlate(countHighSoftTargetValues, tfile, xlabel, ylabel)

tfile <- paste(odir, "/negative_genes_pp.jpg", sep="")
xlabel <- "Plate Number"
ylabel <- "Number of Target Genes Found"
tt <- plotTargetGenePerPlate(countLowFisherTargetValues, tfile, xlabel, ylabel)

tfile <- paste(odir, "/negative_genes_pp_soft.jpg", sep="")
xlabel <- "Plate Number"
ylabel <- "Number of Target Genes Found"
tt <- plotTargetGenePerPlate(countLowSoftTargetValues, tfile, xlabel, ylabel)

# Target identification
resValues <- resValues[which(resValues[,1] %in% samples),]
highTargets <- resValues[which((resValues[,9]<0.05)&(resValues[,8]>0)),]
lowTargets <- resValues[which((resValues[,9]<0.05)&(resValues[,8]<0)),]
highTargets <- highTargets[order(highTargets[,9]),]
lowTargets <- lowTargets[order(lowTargets[,9]),]
write.csv2(highTargets, file=highResultsFile, quote=FALSE)
write.csv2(lowTargets, file=lowResultsFile, quote=FALSE)
highTitle <- "Target genes with phenotypic effect higher than the negative control"
lowTitle <- "Target genes with phenotypic effect lower than the negative control"
targetList2html(highTargetsHtmlFile, highTargets, highTitle, headerHtmlFile, bottomHtmlFile)
targetList2html(lowTargetsHtmlFile, lowTargets, lowTitle, headerHtmlFile, bottomHtmlFile)
screenresults2html(resultsHtmlFile, nrow(highTargets), nrow(lowTargets), reportFilename, headerHtmlFile, bottomHtmlFile)





end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)