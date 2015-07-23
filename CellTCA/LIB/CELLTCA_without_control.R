start.time <- Sys.time()

source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCAMetaInfo.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCAPlateSetup.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCADataInfo.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCASummaries.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCAGeneBasedData.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCAData.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCAReplicate.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCAUtilities.R")
source("/home/akopp/PROJECT/CellTCA/LIBcelltca/CellTCA.R")
source("/home/akopp/PROJECT/CellTCA/LIB/TCAcsv.R")
load("/home/akopp/PROJECT/CellTCA/LIBcelltca/TCASVMModel.Rd")


if (! require(limma))
  stop("limma library is required to go any further.")
if (! require(prada))
  stop("prada library is required to go any further.")
if (! require(grid))
  stop("grid library is required to go any further.")
if (! require(bioDist))
  stop("bioDist library is required to go any further.")
if (! require(e1071))
  stop("e1071 library is required to go any further.")
#if (! require(affy))
#  stop("affy library is required to go any further.")


## VERSION WITHOUT CONTROL

controlValues <- c(); thresholdValues <- c(); percentOfControlValues <- c()
pPositiveCellValues <- c(); pPositiveCellsSigmaValues <- c(); lzFactorValues <- c()
geneNameValues <- c(); normPValues <- c(); gtypeValues <- c(); percentPValues <- c()
adjPercentPValues <- c(); negControlCellCountValues <- c(); posControlCellCountValues <- c()
tcaIdx <- 0; plateNameValues <- c(); meanCellCountValues <- c(); sdCellCountValues <- c()
adjNormPValues <- c(); cellCountPerWellValues <- c(); columnValues <- c()
posMedianValues <- c(); medianValues <- NULL
precision <- 0.05; adjPvalueColumns <- c(14, 13, 6); selectedColumns <- c(1, 14, 13, 6, 11, 7)
normalApproxSampleNumber <- 5000; adjPercentPValues1 <- c(); adjPercentPValues2 <- c();
percentPValues1 <- c(); percentPValues2 <- c(); gtypeValues1 <- c(); gtypeValues2 <- c();
toxColumn <- 7; geneNumberPerPlate <- 60
percentErrorValues <- c()
sampleVarianceSize <- 500
alphaValues <- c(1.15, 1.5, 2); ralphaValues <- c(0.87, 0.5, 0.25)

mywarnings <- as.character()
in.pathFile <-"/home/akopp/Bureau/screen" # PARAM HERE !!!!!!!!!!!!
out.file <-"/home/akopp/Bureau/test_screen_CELLTCA_WC" # PARAM HERE !!!!!!!!!!!!
dir.create(out.file)
in.file <-rev(unlist(strsplit(as.character(in.pathFile), "/")))[1]
idir <- in.pathFile
odir <- out.file
setwd(odir) 
colAnalyze <- "X.Nuc.Cell.Intensity.Background" # PARAM HERE !!!!!!!!!!!!

negSamp <- as.character("NT")
posSamp <- as.character("Scramble")
toxSamp <- as.character("PLK1")
negControlRef <- as.integer("NT")
posControlRef <- as.integer("Scramble")
toxControlRef <- as.integer("PLK1")

OutputControlPlot = FALSE

if (negSamp == "")
  stop("No negative sample name found")

sampName <- negSamp


#redo = F check if data is already process
#redo = T make process is all case
#### Generate CellTCA data ####
readCSVDir(idir, odir, redo=F, refSamp=negSamp, refThr=95, colAnalyze) # PARAM HERE !!!!!!!!!!!!
entryNames <- dir(path=odir, pattern="RData")

dataFound = 1
if (length(entryNames) == 0) {
  dataFound = 0
}

#### Data Processing Parts
tcaIdx <- 0
nImages <- 6

for (entry in entryNames){
  # Keep track of input file being processed
  tcaIdx <- tcaIdx + 1
  # Load the data file
  load(paste(odir, "/", entry, sep=""))
  plateName <- gsub(".RData", "", gsub("CellTCA_", "", entry))
  # Get control names
  controlValues <- c(controlValues, getControls(cellTCA))
  # Layout of the plate
  plateSetup <- getPlateSetup(cellTCA, 1)
  # Validate gene Data by SVM before normalization
  geneDataLabels <- validateTCAGeneData(cellTCA, TCASVMModel)
  # Run normalization over the data and store it in a form that will make it easy to process
  geneBasedData <- getWellNormGeneBasedData(cellTCA, geneDataLabels)
  #geneBasedData <- getSimpleWellNormGeneBasedDataNew(cellTCA)
  # Read columns of the data labeled for analyzing, If there are more than one column
  # each column will be analyzed separately
  colsToAnalyze <- sort(getModColumnNamesToAnalyze(cellTCA))

  # Estimate the cell positive cutoff from the data
  #thresholds <- getEstimatedThresholdValues(geneBasedData, negSamp, posSamp, colsToAnalyze)
  uGenes <- getUniqueGeneNames(cellTCA)
  uGenes <- uGenes[-which(uGenes==negSamp)]
  thresholds <- getEstimatedMultiThresholdValues(geneBasedData, negSamp, uGenes, colsToAnalyze)
  #getPlotDistributionTest(geneBasedData, negSamp, colsToAnalyze, "B10")
  if (negSamp == posSamp) {
    if (is.na(thresholds[negSamp, 1])) {
      next
    }
  }
  # Generate summaries from the data
  summaries <- getSummaries(geneBasedData, colsToAnalyze)
  # Keep track of number of replicates per gene
  countRepPerGene <- getNumberOfReplicatesPerGene(cellTCA)
  countRepPerGene <- countRepPerGene[which(!is.na(countRepPerGene))]
  
  
  
  for (i in 1:(length(colsToAnalyze))) {
    # Get percent of positive cells
    ###pPositiveCells <- getPercentAboveThreshold(geneBasedData, thresholds[i], colsToAnalyze[i])
    pPositiveCells <- getPercentAboveMultiThreshold(geneBasedData, negSamp, thresholds, colsToAnalyze[i])
    if (negSamp == sampName)
      pControlPositiveCells <- getControlPercentAboveMultiThreshold(geneBasedData, sampName, thresholds, colsToAnalyze[i])
    else {
      pControlPositiveCells <- rep(pPositiveCells[negSamp], length(pPositiveCells))
      names(pControlPositiveCells) <- names(pPositiveCells)
    }
    # refNames is used to make sure that comparisons are performed between genes with the same name
    refNames <- names(pPositiveCells)
    # Count the number of positive cells per well
    ###posCellCounts <- getCountAboveThreshold(geneBasedData, thresholds[i], colsToAnalyze[i])
    posCellCounts <- getCountAboveMultiThreshold(geneBasedData, thresholds, colsToAnalyze[i])
    
    # Percent of control is used for well identification
    percentOfControl <- pPositiveCells/pControlPositiveCells[refNames]
    percentOfControl[is.na(percentOfControl)] <- 1
    percentOfControlValues <- c(percentOfControlValues, percentOfControl[refNames])
    # Number of cell per well for toxicity evaluation
    cellCountPerWell <- getLengthSummary(summaries, i)
    #nCellCountPerWell <- floor(cellCountPerWell / countRepPerGene[names(cellCountPerWell)])
    
    # Cannot see any use for  now
    maxCellCount <- max(cellCountPerWell)
    minCellCount <- min(cellCountPerWell)
    meanCellCountValues <- c(meanCellCountValues, mean(cellCountPerWell))
    sdCellCountValues <- c(sdCellCountValues, sd(cellCountPerWell))
    
    # Standard deviation of percent of positive cells per well
    pPositiveCellsSigma <- sqrt((pPositiveCells*(1-pPositiveCells))/cellCountPerWell[refNames])
    pPositiveCellsSigmaValues <- c(pPositiveCellsSigmaValues, pPositiveCellsSigma)
    
    pControlsSigma <- sqrt((pControlPositiveCells[refNames]*(1-pControlPositiveCells[refNames]))/cellCountPerWell[negSamp])
    percentErrors <- getPercentErrorValues(sampleVarianceSize, pPositiveCells[refNames], pControlPositiveCells[refNames], pPositiveCellsSigma[refNames], pControlsSigma)
    percentErrorValues <- c(percentErrorValues, percentErrors)
    

    lzFactor <- 1
    ### Pas sur ici lz-factor neg et pos
    lzFactor <- 1 - ((3*(pPositiveCellsSigma[posSamp]+pPositiveCellsSigma[sampName]))/abs(pPositiveCells[posSamp]-pPositiveCells[sampName]))
    lzFactorValues <- c(lzFactorValues, rep(lzFactor, length(refNames)))
    # Keep track of all gene names for final results
    geneNameValues <- c(geneNameValues, refNames)
    columnValues <- c(columnValues, rep(colsToAnalyze[i], length(refNames)))
    
    #negativeControlNameValues <- c(negativeControlNameValues, rep(sampName, length(refNames)))
    #columnName <- c(columnName, rep(colsToAnalyze[i], length(refNames)))
    plateNameValues <- c(plateNameValues, rep(plateName, length(refNames)))
    
    pPositiveCellValues <- c(pPositiveCellValues, pPositiveCells[refNames])
    
    # Calculate pvalues based on difference of normal approximation
    # pNorm_tmp <- getNormPvalues(cellCountPerWell[refNames], posCellCounts[refNames], negSamp)
    # Adjust pvalues accordingly
    # cpNorm_tmp <- sort(pNorm_tmp) * seq(from=length(pNorm_tmp), to=1, by=-1)
    # adjNormPValues <- c(adjNormPValues, cpNorm_tmp[refNames])
    # pNorm_tmp <- pNorm_tmp[refNames]
    # normPValues <- c(normPValues, pNorm_tmp)
    
    
    ## calcule des gtype (a quoi sert-il ??)
    for (v in 1:length(alphaValues)) {
      alphaValue <- alphaValues[v]
      # I need to know whether percent of positive cells are less or greater than control
      gtype_tmp <- c()
      gtype_tmp[refNames] <- 0
      gtype_name <- names(which(percentOfControl[refNames] > alphaValue))
      gtype_tmp[gtype_name] <- 1
      gtype_name <- names(which(percentOfControl[refNames] < ralphaValues[v]))
      gtype_tmp[gtype_name] <- -1
      if (alphaValue == alphaValues[1]) {
        gtypeValues <- c(gtypeValues, gtype_tmp)
      }
      else if (alphaValue == alphaValues[2]) {
        gtypeValues1 <- c(gtypeValues1, gtype_tmp)
      }
      else {
        gtypeValues2 <- c(gtypeValues2, gtype_tmp)
      }
      
      # Calculate percent of control pvalues for gene classification
      percentOfControl_pos <- percentOfControl[which(percentOfControl>=alphaValue)]
      percentOfControl_neg <- percentOfControl[which((percentOfControl>0) & (percentOfControl<=ralphaValues[v]))]
      percentOfControl_zero <- percentOfControl[which(percentOfControl==0)]
      percentOfControl_null <- percentOfControl[which((percentOfControl<alphaValue) & (percentOfControl>ralphaValues[v]))]
      
      percentPValue_pos1 <- c()
      if (length(percentOfControl_pos)) {
        percentPValue_pos1 <- rep(1, length(percentOfControl_pos))
        names(percentPValue_pos1) <- names(percentOfControl_pos)
        for (g in names(percentOfControl_pos)) {
          if (percentOfControl_pos[g] != 1) {
            percentPValue_pos1[g] <- integrate(null_ratio2normals, lower=percentOfControl_pos[g], upper=Inf, alpha=alphaValue, mu=pControlPositiveCells[g], sigma=pControlsSigma[g])$value
          }
        }
      }
      #print(pPercent_pos1)
      percentPValue_neg1 <- c()
      if (length(percentOfControl_neg)) {
        percentPValue_neg1 <- rep(1, length(percentOfControl_neg))
        names(percentPValue_neg1) <- names(percentOfControl_neg)
        for (g in names(percentOfControl_neg)) {
          if (percentOfControl_neg[g] != 1) {
            #print(c(percentOfControl_neg[g], pControlPositiveCells[g], pControlsSigma[g]))
            percentPValue_neg1[g] <- integrate(null_ratio2normals, lower=-Inf, upper=percentOfControl_neg[g], alpha=ralphaValues[v], mu=pControlPositiveCells[g], sigma=pControlsSigma[g])$value
          }
        }
      }
      #print(pPercent_neg1)
      percentPValue_tmp <- c()
      adjPercentPValue_tmp <- c()
      if (length(percentPValue_pos1)) {
        #percentPValue_pos <- unlist(percentPValue_pos1[seq(from=1, to=length(percentPValue_pos1), by=5)])
        #print(pPercent_pos)
        #names(percentPValue_pos) <- colnames(percentPValue_pos1)
        percentPValue_tmp <- c(percentPValue_tmp, percentPValue_pos1)
        # Adjust accordingly
        adjPercentPValue_tmp <- sort(percentPValue_pos1) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(percentPValue_pos1)+1, by=-1)
      }
      if (length(percentPValue_neg1)) {
        #percentPValue_neg <- unlist(percentPValue_neg1[seq(from=1, to=length(percentPValue_neg1), by=5)])
        #print(pPercent_neg)
        #names(percentPValue_neg) <- colnames(percentPValue_neg1)
        percentPValue_tmp <- c(percentPValue_tmp, percentPValue_neg1)
        # Adjust accordingly
        adjPercentPValue_tmp <- c(adjPercentPValue_tmp, sort(percentPValue_neg1) * seq(from=geneNumberPerPlate, to=geneNumberPerPlate-length(percentPValue_neg1)+1, by=-1))
      }
      if (length(percentOfControl_zero)) {
        percentPValue_zero <- rep(0, length(percentOfControl_zero))
        names(percentPValue_zero) <- names(percentOfControl_zero)
        percentPValue_tmp <- c(percentPValue_tmp, percentPValue_zero)
        adjPercentPValue_tmp <- c(adjPercentPValue_tmp, percentPValue_zero)
      }
      if (length(percentOfControl_null)) {
        percentPValue_null <- rep(1, length(percentOfControl_null))
        names(percentPValue_null) <- names(percentOfControl_null)
        percentPValue_tmp <- c(percentPValue_tmp, percentPValue_null)
        adjPercentPValue_tmp <- c(adjPercentPValue_tmp, percentPValue_null)
      }
      if (alphaValue == alphaValues[1]) {
        percentPValues <- c(percentPValues, percentPValue_tmp[refNames])
        # Adjust accordingly
        adjPercentPValues <- c(adjPercentPValues, adjPercentPValue_tmp[refNames])
      }
      else if (alphaValue == alphaValues[2]) {
        percentPValues1 <- c(percentPValues1, percentPValue_tmp[refNames])
        # Adjust accordingly
        adjPercentPValues1 <- c(adjPercentPValues1, adjPercentPValue_tmp[refNames])
      }
      else {
        percentPValues2 <- c(percentPValues2, percentPValue_tmp[refNames])
        # Adjust accordingly
        adjPercentPValues2 <- c(adjPercentPValues2, adjPercentPValue_tmp[refNames])
      }
    }
    
    
    # Keep track of cell counts
    cellCountPerWellValues <- c(cellCountPerWellValues, cellCountPerWell[refNames])
    negControlCellCountValues <- c(negControlCellCountValues, cellCountPerWell[negSamp])
    posControlCellCountValues <- c(posControlCellCountValues, cellCountPerWell[toxSamp])
    
    if (OutputControlPlot == TRUE) {
      t_num <- 0
      for (g in uGenes) {
        if (! is.na(thresholds[g,i])) {
          t_num <- t_num + 1
          tfile <- paste('ctrs_', tcaIdx, '_', t_num, '_', i, ".pdf", sep="")
          tt <- plotControls(geneBasedData, sampName, g, thresholds[g,i], colsToAnalyze[i], tfile, 7, 5, 1)
        }
      } 
    }
     
    tfile <- paste('c', i, '_', 1+(tcaIdx-1)*nImages, ".pdf", sep="")
    tt <- barMultiThresholdPlots(summaries, geneBasedData, i, colsToAnalyze[i], sampName, thresholds, tfile, 7, 5, countRepPerGene, posSamp, 1)

    tfile <- paste('c', i, '_', 2+(tcaIdx-1)*nImages, ".pdf", sep="")
    tt <- plotPercentOfControl(summaries, percentOfControl, colsToAnalyze[i], tfile, 7, 5, 1)

    tfile <- paste('c', i, '_', 3+(tcaIdx-1)*nImages, ".pdf", sep="")
    tt <- plotMultiThresholdSummary(summaries, i, colsToAnalyze[i], sampName, tfile, 7, 5, 1)

    tfile <- paste('c', i, '_', 4+(tcaIdx-1)*nImages, ".pdf", sep="")
    tt <- spatialSummaryPlot(summaries, plateSetup, sampName, i, colsToAnalyze[i], tfile, 7, 5, 1)

    tfile <- paste('c', i, '_', 5+(tcaIdx-1)*nImages, ".pdf", sep="")
    tt <- cvPlot(summaries, plateSetup, sampName, i, colsToAnalyze[i], tfile, 7, 5, 1)
  }
}


cntPlot <- 0
array_ncol <- ncol(getContent(plateSetup))
array_nrow <- nrow(getContent(plateSetup))

# Normal parameters for toxicity evaluation

data_tmp <- getGeneBasedData(geneBasedData)
data_pos <- as.data.frame(data_tmp[posSamp])
data_neg <- as.data.frame(data_tmp[negSamp])
normParams_pos <- get_normal_parameters2(data_pos[,1])
normParams_neg <- get_normal_parameters2(data_neg[,1])

#normParams_pos <- get_normal_parameters(posControlCellCountValues)
#normParams_neg <- get_normal_parameters(negControlCellCountValues)

#calcul viability
toxValues <- getToxValues(cellCountPerWellValues, normParams_pos, normParams_neg)
#calcul zfactor pourtant deja calculer avant mais il semble faux ???
zfactor <- getZfactor(normParams_pos, normParams_neg)
zfactor <- rep(zfactor, length(toxValues))


resDownNames <- c("Gene", "gtype", "gtype1", "gtype2", "percentPValues", "Viability", "lzfactor", "zfactor", "column", "Percent of control", 'percentOfControlSd', "plateNames", paste("p-value(alpha=",alphaValues[1],")",sep=""), paste("p-value(alpha=",alphaValues[2],")",sep=""), paste("p-value(alpha=",alphaValues[3],")",sep="")) 
resUpNames <- c("Gene", "gtype", "gtype1", "gtype2", "percentPValues", "Viability", "lzfactor", "zfactor", "column", "Percent of control",'percentOfControlSd', "plateNames", paste("p-value(alpha=",ralphaValues[1],")",sep=""), paste("p-value(alpha=",ralphaValues[2],")",sep=""), paste("p-value(alpha=",ralphaValues[3],")",sep=""))
resValues = data.frame(geneNameValues, gtypeValues, gtypeValues1, gtypeValues2, percentPValues, toxValues, lzFactorValues, zfactor, columnValues, percentOfControlValues, percentErrorValues, plateNameValues, adjPercentPValues, adjPercentPValues1, adjPercentPValues2)
colnames(resValues) <- resDownNames

resValues = resValues[order(-resValues[,10]), ]

write.csv(resValues, file=paste(odir, "/", "raw_results.csv", sep=""))
resValues[which(resValues[,2]==0), adjPvalueColumns[3]] <- NA
resValues[which(resValues[,3]==0), adjPvalueColumns[2]] <- NA
resValues[which(resValues[,4]==0), adjPvalueColumns[1]] <- NA
cntPlot <- cntPlot + 1


controls <- c(unique(controlValues), "vide")
columns <- unique(as.vector(resValues$column))
# No need to consider all the columns to calculate cell counts
count_t <- cellCountPerWellValues[which(columnValues==columns[1])]
samples <- setdiff(geneNameValues, controls)
sample_counts <- count_t[which(names(count_t) %in% samples)]
tfile <- "zfactor_plot.jpg"
tt <- plotZfactor(normalApproxSampleNumber, normParams_pos, normParams_neg, sample_counts, tfile, 7, 5, 1)


cid <- 1
for (col in columns) {
  colData <- resValues[which(resValues$column==col),]
  rawData <- colData[which(colData[,2] == 1),]
  colData <- colData[which((colData[,1]%in%samples)&(colData[,2]==1)),]
  #write.csv2(rawData, file=paste(odir, "/", col, "_downregulator_raw_results.csv", sep=""))
  #write.csv2(colData, file=paste(odir, "/", col, "_downregulator_raw_sample_results.csv", sep=""))
  write.csv(rawData, file=paste(odir, "/c", cid, "_downregulator_raw_results.csv", sep=""))
  write.csv(colData, file=paste(odir, "/c", cid, "_downregulator_raw_sample_results.csv", sep=""))
  colData <- colData[order(colData[, adjPvalueColumns[1]]),]
  rowsFound = which(colData[,adjPvalueColumns[1]]<=precision)
  if (length(rowsFound)) {
    pos <- max(rowsFound)
    colData[(pos+1):nrow(colData), adjPvalueColumns[1]] <- NA
  }
  else {
    pos <- 0
  }
  if ((pos+1) < nrow(colData)) {
    colData[(pos+1):nrow(colData),] <- colData[pos+order(colData[(pos+1):nrow(colData),adjPvalueColumns[2]]),]
    rowsFound = which(colData[,adjPvalueColumns[2]]<=precision)
    if (length(rowsFound)) {
      pos <- max(rowsFound)
      colData[(pos+1):nrow(colData), adjPvalueColumns[2]] <- NA
    }
    if ((pos+1) < nrow(colData)) {
      colData[(pos+1):nrow(colData),] <- colData[pos+order(colData[(pos+1):nrow(colData),adjPvalueColumns[3]]),]
    }
  }
  colData <- colData[which((colData[,adjPvalueColumns[3]] <= precision) & (colData[,toxColumn] >=0)),]
  if (nrow(colData)) {
    
    dat <- colData[, selectedColumns]
    row.names(dat) <- 1:nrow(dat)
    #write.csv2(dat, file=paste(odir, "/", col, "_downregulator_order_results.csv", sep=""))
    write.csv(dat, file=paste(odir, "/c", cid, "_downregulator_order_results.csv", sep=""))
  }
  cid <- cid + 1
}


colnames(resValues) <- resUpNames
cid <- 1
for (col in columns) {
  colData <- resValues[which(resValues$column==col),]
  rawData <- colData[which(colData[,2]==-1),]
  colData <- colData[which((colData[,1]%in%samples)&(colData[,2]==-1)),]
  write.csv(rawData, file=paste(odir, "/c", cid, "_upregulator_raw_results.csv", sep=""))
  write.csv(colData, file=paste(odir, "/c", cid, "_upregulator_raw_sample_results.csv", sep=""))
  colData <- colData[order(colData[, adjPvalueColumns[1]]),]
  rowsFound = which(colData[,adjPvalueColumns[1]]<=precision)
  if (length(rowsFound)) {
    pos <- max(rowsFound)
    colData[(rowsFound+1):nrow(colData), adjPvalueColumns[1]] <- NA
  }
  else {
    pos <- 0
  }
  if ((pos+1) < nrow(colData)) {
    colData[(pos+1):nrow(colData),] <- colData[pos+order(colData[(pos+1):nrow(colData),adjPvalueColumns[2]]),]
    rowsFound = which(colData[,adjPvalueColumns[2]]<=precision)
    if (length(rowsFound)) {
      pos <- max(rowsFound)
      colData[(rowsFound+1):nrow(colData), adjPvalueColumns[2]] <- NA
    }
    if ((pos+1) < nrow(colData)) {
      colData[(pos+1):nrow(colData),] <- colData[pos+order(colData[(pos+1):nrow(colData),adjPvalueColumns[3]]),]
    }
  }
  
  colData <- colData[which((colData[,adjPvalueColumns[3]] <= precision) & (colData[,toxColumn] >=0)),]
  
  if (nrow(colData)) {
    dat <- colData[, selectedColumns]
    row.names(dat) <- 1:nrow(dat)
    
    write.csv(dat, file=paste(odir, "/c", cid, "_upregulator_order_results.csv", sep=""))
  }
  cid <- cid + 1
} 

cid <- 1
for (col in columns) {
  colData <- resValues[which(resValues$column==col),]
  colData <- colData[which((colData[,1]%in%samples)&(colData[, toxColumn]<0)),]
  write.csv(colData, file=paste(odir, "/c", cid, "_toxic_all_genes.csv", sep=""))
  colData <- colData[order(colData[, adjPvalueColumns[3]]),]
  
  if (nrow(colData)) {
    dat <- colData[, selectedColumns]
    row.names(dat) <- 1:nrow(dat)
    write.csv(dat, file=paste(odir, "/c", cid, "_toxic_genes.csv", sep=""))
  }
  cid <- cid + 1
} 


end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)