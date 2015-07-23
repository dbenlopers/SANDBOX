####################################################################################
# class definition for CellTCA
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
####################################################################################
setClass(
  Class = "CellTCA",
  representation = representation(
    numberOfReplicates = "numeric",
    metaInfo = "TCAMetaInfo",
    isNormalized = "logical",
    replicates = "list",
    normData = "TCAData",
    normDataLog = "TCAData"
  ),
  prototype = prototype(
    numberOfReplicates = numeric(0),
    metaInfo = NULL,
    replicates = NULL
  )
)


#----------------------------------------------------------------------------------
# CellTCA::initialize function
#----------------------------------------------------------------------------------
setMethod("initialize",
          signature = signature("CellTCA"),
          definition = function(.Object, metaInfo=NULL, replicates=NULL) {
            .Object@numberOfReplicates = length(replicates)
            .Object@replicates = replicates
            .Object@metaInfo = metaInfo
            .Object@isNormalized = F
            return(.Object)
          }
)	


#----------------------------------------------------------------------------------
# CellTCA::print function
#----------------------------------------------------------------------------------
setMethod("print",
          signature = signature("CellTCA"),
          definition = function(x, ...) {
            cat("\n*** Class CellTCA - Method print ***\n\n")
            cat(paste(c("Number of replicates : ", x@numberOfReplicates), collapse=""))
            cat("\n\n")
            print(x@metaInfo)
            for (i in 1:x@numberOfReplicates) {
              cat(paste(c("Replicate : ", i), collapse=""))
              cat("\n")
              print(x@replicates[i])
              cat("\n\n")
            }
          }
)



#----------------------------------------------------------------------------------
# CellTCA::show function
#----------------------------------------------------------------------------------
setMethod("show",
          signature = signature("CellTCA"),
          definition = function(object) {
            cat("\n*** Class CellTCA - Method show ***\n\n")
            cat(paste(c("Number of replicates : ", object@numberOfReplicates), collapse=""))
            cat("\n\n")
            show(object@metaInfo)
            for (i in 1:object@numberOfReplicates) {
              cat(paste(c("Replicate : ", i), collapse=""))
              cat("\n")
              show(object@replicates[i])
              cat("\n\n")
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::outOfRange function
#-------------------------------------------------------------------------------#
setGeneric("outOfRange",
           function(object, repId, ...) {
             standardGeneric("outOfRange")
           }
)

setMethod("outOfRange",
          signature = signature("CellTCA"),
          definition = function(object, repId) {
            if ((repId > object@numberOfReplicates) | (repId < 0)) {
              cat(paste(c("Error : Replicate number ", repId, " is out of range "), collapse=""))
              cat("\n")
              return(1)
            }
            return(0)
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::getPlateSetup function
#-------------------------------------------------------------------------------#
setMethod("getPlateSetup",
          signature = signature("CellTCA"),
          definition = function(object, repId=0) {
            if (repId == 0) {
              print("Usage : getPlateSetup(object, repId)")
              print("to get the data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId)) {
              return(getPlateSetup(object@replicates[[repId]]))
            }
            return(NULL)
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::getMetaInfo function
#-------------------------------------------------------------------------------#
setGeneric("getMetaInfo",
           function(object) {
             standardGeneric("getMetaInfo")
           }
)

setMethod("getMetaInfo",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(object@metaInfo)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getTCAData function
#-------------------------------------------------------------------------------#
setMethod("getTCAData",
          signature = signature("CellTCA"),
          definition = function(object, repId=0) {
            if (repId == 0) {
              print("Usage : getTCAData(object, repId)")
              print("to get the data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId)) {
              return(getTCAData(object@replicates[[repId]]))
            }
            return(NULL)
          }
)

#-------------------------------------------------------------------------------#
# CellTCA::getNormData function
#-------------------------------------------------------------------------------#
setGeneric("getNormGeneBasedData",
           function(object) {
             standardGeneric("getNormGeneBasedData")
           }
)

setMethod("getNormGeneBasedData",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(getGeneBasedData(object@normData))
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::getNormData function
#-------------------------------------------------------------------------------#
setGeneric("getNormGeneBasedDataLog",
           function(object) {
             standardGeneric("getNormGeneBasedDataLog")
           }
)

setMethod("getNormGeneBasedDataLog",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(getGeneBasedData(object@normDataLog))
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::isNorm function
#-------------------------------------------------------------------------------#
setGeneric("isNorm",
           function(object) {
             standardGeneric("isNorm")
           }
)

setMethod("isNorm",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(object@isNormalized)
          }
)




#-------------------------------------------------------------------------------#
# CellTCA::getDataInfo function
#-------------------------------------------------------------------------------#
setMethod("getDataInfo",
          signature = signature("CellTCA"),
          definition = function(object, repId=0, ...) {
            if (repId == 0) {
              print("Usage : getDataInfo(object, repId)")
              print("to get the data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId))
              return(getDataInfo(object@replicates[[repId]]))
            return(NULL)
          }
)

#-------------------------------------------------------------------------------#
# CellTCA::getContent function
# return the content of the CellTCA object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("CellTCA"),
          definition = function(object, repId=0, ...) {
            if (repId == 0)
              return(lapply(object@replicates, getContent))
            if (! outOfRange(object, repId))
              return(getContent(object@replicates[[repId]]))
            return(NULL)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getReplicate function
#-------------------------------------------------------------------------------#
setGeneric("getReplicate",
           function(object, repId=0, ...) {
             standardGeneric("getReplicate")
           }
)

setMethod("getReplicate",
          signature = signature("CellTCA"),
          definition = function(object, repId=0, ...) {
            if (repId == 0) {
              print("Usage : getReplicate(object, repId)")
              print("to get the data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId))
              return(object@replicates[[repId]])
            return(NULL)
          }
)

#-------------------------------------------------------------------------------#
# CellTCA::getNumberOfReplicates function
#-------------------------------------------------------------------------------#
setGeneric("getNumberOfReplicates",
           function(object) {
             standardGeneric("getNumberOfReplicates")
           }
)

setMethod("getNumberOfReplicates",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(object@numberOfReplicates)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getReplicates function
#-------------------------------------------------------------------------------#
setGeneric("getReplicates",
           function(object) {
             standardGeneric("getReplicates")
           }
)

setMethod("getReplicates",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(object@replicates)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getGenes function
# return a matrix [wellId, geneId] 
#-------------------------------------------------------------------------------#
setMethod("getGenes",
          signature = signature("CellTCA"),
          definition = function(object, repId) {
            if (repId == 0) {
              print("Usage : getGenes(object, repId)")
              print("to get the data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId))
              return(getGenes(object@replicates[[repId]]))
            return(NULL)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getColumnNamesToAnalyze function
# return columns select to analyze
#-------------------------------------------------------------------------------#

setMethod("getColumnNamesToAnalyze",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(getColumnNamesToAnalyze(object@metaInfo))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getModColumnNamesToAnalyze function
# return modified columns select to analyze
#-------------------------------------------------------------------------------#
setMethod("getModColumnNamesToAnalyze",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(getModColumnNamesToAnalyze(object@metaInfo))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getDataToAnalyze function
# return selected columns from normalized data for analysis 
#-------------------------------------------------------------------------------#

setMethod("getDataToAnalyze",
          signature = signature("CellTCA"),
          definition = function(object, columnNamesToAnalyze=NULL) {
            if (is.null(columnNamesToAnalyze)) {
              print("You need to specify the column names you want your data from!")
              print("Usage : getDataToAnalyze(object, columnNames)")
              return(NULL)
            }
            if (object@isNormalized)
              return(getDataToAnalyze(object@normalizedPlate, columnNamesToAnalyze))
            print("No normalized plate available, use getNNDataToAnalyze instead")
            return(NULL)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getRefThreshold
# return threshold value
#-------------------------------------------------------------------------------#
setMethod("getRefThreshold",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(getRefThreshold(object@metaInfo))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getRefSamp
# return reference sample name
#-------------------------------------------------------------------------------#
setMethod("getRefSamp",
          signature = signature("CellTCA"),
          definition = function(object) {
            return(getRefSamp(object@metaInfo))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getGeneBasedData function
#-------------------------------------------------------------------------------#
setMethod("getGeneBasedData",
          signature = signature("CellTCA"),
          definition = function(object, repId=0) {
            if (repId == 0) {
              print("Usage : getGeneBasedData(object, repId)")
              print("to get gene based data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId)) {
              return(getGeneBasedData(object@replicates[[repId]]))
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getWellNormGeneBasedData function
#-------------------------------------------------------------------------------#
setGeneric("getWellNormLogGeneBasedData_unop",
           function(object, median) {
             standardGeneric("getWellNormLogGeneBasedData_unop")
           }
)


setMethod("getWellNormLogGeneBasedData_unop",
          signature = signature("CellTCA"),
          definition = function(object, median) {
            # No intra plate normalization available
            if (getNumberOfReplicates(object) == 1)
              return(getGeneBasedData(object, 1))
            
            # Better be cautious in case a gene is found 
            # in one plate and not in another one	
            geneNames <- getUniqueGeneNames(object)
            # Build a matrix n replicates x n genes
            # Each row will contain the number records for each gene
            # within that replicate
            geneTabNames <- matrix(, getNumberOfReplicates(object), length(geneNames))
            for (i in 1:getNumberOfReplicates(object)) {
              tmpGeneNames <- getCntGeneNames(object@replicates[[i]])
              tmpGeneNames <- tmpGeneNames[geneNames]
              tmpGeneNames[which(is.na(tmpGeneNames))] <- 0
              geneTabNames[i,] <- tmpGeneNames
            }
            # Take the maximum count over the three replicates for each gene
            geneCnt <- apply(geneTabNames, 2, max)
            delCols <- rep(0, length(geneCnt))
            # Here the maximum gene entries
            maxDataRows <- sum(geneCnt)
            
            cols <- getModColumnNamesToAnalyze(object)
            dataToSummarize <- NULL
            firstCol <- TRUE
            for (col in cols) {
              colData <- c() 
              for (i in 1:length(geneNames)) {   
                dataForNorm <- matrix(, geneCnt[i], getNumberOfReplicates(object))
                # If a gene is missing in a replicate
                # delCol will prevent from performing normalization
                # with a NA column
                delCol <- 0
                for (j in 1:getNumberOfReplicates(object)) {
                  dataTmp <- getGeneNameTCAData(object@replicates[[j]], geneNames[i])
                  if (length(dataTmp[, col]) & length(which(!is.na(dataTmp[, col])))) {
                    # Making sure that column is not an na column
                    if (delCol != 2) {
                      dataForNorm[1:nrow(dataTmp), j-delCol] <- as.numeric(dataTmp[1:nrow(dataTmp), col])
                    }
                    else {
                      dataForNorm[1:nrow(dataTmp)] <- as.numeric(dataTmp[1:nrow(dataTmp), col])
                    }
                  }
                  else {
                    # In case of an na column, we need to remove it from dataForNorm
                    # reducing the number of replicates by 1
                    # We also need to update delCol to take into account the removed
                    # column in the coming steps 
                    dataForNorm <- dataForNorm[, -(j-delCol)]
                    delCol <- delCol + 1
                  }
                }
                if (is.matrix(dataForNorm)) {
                  normalizedData <- normalizeBetweenArrays(dataForNorm, method="quantile")
                  normalizedData <- log2(normalizedData)
                  
                  if (median == T) {
                    normalizedData <- apply(normalizedData, 1, median, na.rm = T)
                  }
                  
                }
                else {
                  normalizedData <- dataForNorm
                }
                # the data is organized on a column based
                # each line will consist of gene id and column values
                # As each each column represents the same distribution,
                # we only need one of them. Preferably, one without na
                # or with less na entries
                if (is.matrix(normalizedData)) {
                  naCount <- apply(normalizedData, 2, function(u) length(which(is.na(u))))
                  minCount <- min(naCount)
                  colLeader <- which(naCount==minCount)[1]
                  colData <- c(colData, normalizedData[, colLeader])
                }
                else {
                  colData <- c(colData, normalizedData) 
                }
                if (firstCol) {
                  delCols[i] <- delCol
                }
              }
              if (is.null(dataToSummarize)) {
                dataToSummarize <- data.frame(colData)
              }
              else {
                scol <- ncol(dataToSummarize)
                dataToSummarize <- data.frame(cbind(dataToSummarize[,1:scol], 
                                                    as.numeric(colData)))
              }
              firstCol = FALSE
            }
            names(dataToSummarize) <- cols
            # Collect gene names for entries in the global data frame
            dataToSummarize$GeneName <- rep(geneNames, geneCnt)
            dataToSummarize <- new("TCAData", data=dataToSummarize)
#             object@normDataLog = dataToSummarize
#             object@isNormalized = TRUE
            return(getGeneBasedData(dataToSummarize))
          }
)

getWellNormLogGeneBasedData <- compiler::cmpfun(getWellNormLogGeneBasedData_unop)

#-------------------------------------------------------------------------------#
# CellTCA::getWellNormGeneBasedData function
#-------------------------------------------------------------------------------#
setGeneric("getWellNormGeneBasedData_unop",
           function(object, median) {
             standardGeneric("getWellNormGeneBasedData_unop")
           }
)

setMethod("getWellNormGeneBasedData_unop",
          signature = signature("CellTCA"),
          definition = function(object, median) {
            # No intra plate normalization available
            if (getNumberOfReplicates(object) == 1)
              return(getGeneBasedData(object, 1))
            
            # Better be cautious in case a gene is found 
            # in one plate and not in another one	
            geneNames <- getUniqueGeneNames(object)
            # Build a matrix n replicates x n genes
            # Each row will contain the number records for each gene
            # within that replicate
            geneTabNames <- matrix(, getNumberOfReplicates(object), length(geneNames))
            for (i in 1:getNumberOfReplicates(object)) {
              tmpGeneNames <- getCntGeneNames(object@replicates[[i]])
              tmpGeneNames <- tmpGeneNames[geneNames]
              tmpGeneNames[which(is.na(tmpGeneNames))] <- 0
              geneTabNames[i,] <- tmpGeneNames
            }
            # Take the maximum count over the three replicates for each gene
            geneCnt <- apply(geneTabNames, 2, max)
            delCols <- rep(0, length(geneCnt))
            # Here the maximum gene entries
            maxDataRows <- sum(geneCnt)
            
            cols <- getModColumnNamesToAnalyze(object)
            dataToSummarize <- NULL
            firstCol <- TRUE
            for (col in cols) {
              colData <- c() 
              for (i in 1:length(geneNames)) {   
                dataForNorm <- matrix(, geneCnt[i], getNumberOfReplicates(object))
                # If a gene is missing in a replicate
                # delCol will prevent from performing normalization
                # with a NA column
                delCol <- 0
                for (j in 1:getNumberOfReplicates(object)) {
                  dataTmp <- getGeneNameTCAData(object@replicates[[j]], geneNames[i])
                  if (length(dataTmp[, col]) & length(which(!is.na(dataTmp[, col])))) {
                    # Making sure that column is not an na column
                    if (delCol != 2) {
                      dataForNorm[1:nrow(dataTmp), j-delCol] <- as.numeric(dataTmp[1:nrow(dataTmp), col])
                    }
                    else {
                      dataForNorm[1:nrow(dataTmp)] <- as.numeric(dataTmp[1:nrow(dataTmp), col])
                    }
                  }
                  else {
                    # In case of an na column, we need to remove it from dataForNorm
                    # reducing the number of replicates by 1
                    # We also need to update delCol to take into account the removed
                    # column in the coming steps 
                    dataForNorm <- dataForNorm[, -(j-delCol)]
                    delCol <- delCol + 1
                  }
                }
                if (is.matrix(dataForNorm)) {
                  normalizedData <- normalizeBetweenArrays(dataForNorm, method="quantile")
                  
                  if (median == T) {
                    normalizedData <- apply(normalizedData, 1, median, na.rm = T)
                  }

                }
                else {
                  normalizedData <- dataForNorm
                }
                # the data is organized on a column based
                # each line will consist of gene id and column values
                # As each each column represents the same distribution,
                # we only need one of them. Preferably, one without na
                # or with less na entries
                if (is.matrix(normalizedData)) {
                  naCount <- apply(normalizedData, 2, function(u) length(which(is.na(u))))
                  minCount <- min(naCount)
                  colLeader <- which(naCount==minCount)[1]
                  colData <- c(colData, normalizedData[, colLeader])
                }
                else {
                  colData <- c(colData, normalizedData) 
                }
                if (firstCol) {
                  delCols[i] <- delCol
                }
              }
              if (is.null(dataToSummarize)) {
                dataToSummarize <- data.frame(colData)
              }
              else {
                scol <- ncol(dataToSummarize)
                dataToSummarize <- data.frame(cbind(dataToSummarize[,1:scol], 
                                                    as.numeric(colData)))
              }
              firstCol = FALSE
            }
            names(dataToSummarize) <- cols
            # Collect gene names for entries in the global data frame
            dataToSummarize$GeneName <- rep(geneNames, geneCnt)
            dataToSummarize <- new("TCAData", data=dataToSummarize)
#             object@normData = dataToSummarize
#             object@isNormalized = TRUE
            return(getGeneBasedData(dataToSummarize))
          }
)

getWellNormGeneBasedData <- compiler::cmpfun(getWellNormGeneBasedData_unop)

#-------------------------------------------------------------------------------#
# CellTCA::getNormGeneBasedData function
#-------------------------------------------------------------------------------#
setGeneric("getNNGeneBasedData",
           function(object) {
             standardGeneric("getNNGeneBasedData")
           }
)

setMethod("getNNGeneBasedData",
          signature = signature("CellTCA"),
          definition = function(object) {
            if (getNumberOfReplicates(object) == 1)
              return(getGeneBasedData(object, 1))
            
            cols <- getModColumnNamesToAnalyze(object)
            rawdata = getContent(getTCAData(object, 1))
            for (i in 2:getNumberOfReplicates(object)) {
              tmp <- getContent(getTCAData(object, i))
              rawdata <- data.frame(rbind(rawdata[1:nrow(rawdata),], tmp[1:nrow(tmp),]))
            }
            data = new("TCAData", data=rawdata)
            return(getGeneBasedData(data))
          }
)




#-------------------------------------------------------------------------------#
# CellTCA::plotNNReplicateSummaries function 
#-------------------------------------------------------------------------------#
setGeneric("plotNNReplicateSummaries",
           function(object, repId=0) {
             standardGeneric("plotNNReplicateSummaries")
           }
)


setMethod("plotNNReplicateSummaries",
          signature = signature("CellTCA"),
          definition = function(object, repId=0) {
            if (repId == 0) {
              print("Usage : plotNNReplicateSummaries(object, repId)")
              print("will plot summaries for a non normalized plate")
              return(NULL)
            }
            cols <- getModColumnNamesToAnalyze(object)
            geneDataObject <- getGeneBasedData(object, repId)
            summaries <- getSummaries(geneDataObject, cols)
            sampName <- getRefSamp(object)
            if (is.na(sampName)) {
              cat("No reference sample found, plain plots will be triggered\n")
              columns <- c(cols[1])
              layout(1:1)
              for (i in 1:length(cols)) {
                plotPlainSummary(summaries, i, cols[i])
              }
            }
            else {
              refThreshold <- getRefThreshold(object)
              if (is.na(refThreshold)) {
                cat("No reference threshold found. Default is : 0.05\n")
                refThreshold <- 0.05
              }
              thresholds <- getThresholdValues(geneDataObject, sampName, refThreshold, cols) 
              cnt <- getNumberOfReplicatesPerGene(object)
              columns <- c(cols[1])
              layout(1:2)
              for (i in 1:length(columns)) {
                plotSummary(summaries, i, columns[i], sampName, thresholds[columns[i]])
                plotPercentData(geneDataObject, summaries, thresholds[columns[i]], i, columns[i], cnt)
              }
            }	 
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::plotNNallReplicatesSummaries function 
#-------------------------------------------------------------------------------#
setGeneric("plotNNallReplicatesSummaries",
           function(object) {
             standardGeneric("plotNNallReplicatesSummaries")
           }
)

setMethod("plotNNallReplicatesSummaries",
          signature = signature("CellTCA"),
          definition = function(object) {
            cols <- getModColumnNamesToAnalyze(object)
            rawdata = getContent(getTCAData(object, 1))
            for (i in 2:getNumberOfReplicates(object)) {
              tmp <- getContent(getTCAData(object, i))
              rawdata <- data.frame(rbind(rawdata[1:nrow(rawdata),], tmp[1:nrow(tmp),]))
            }
            print(nrow(rawdata))
            data = new("TCAData", data=rawdata)
            geneDataObject <- getGeneBasedData(data)
            summaries <- getSummaries(geneDataObject, cols)
            sampName <- getRefSamp(object)
            if (is.na(sampName)) {
              cat("No reference sample found, plain plots will be triggered\n")
              columns <- c(cols[1])
              layout(1:1)
              for (i in 1:length(cols)) {
                plotPlainSummary(summaries, i, cols[i])
              }
            }
            else {
              if (is.na(refThreshold)) {
                cat("No reference threshold found. Default is : 0.05\n")
                refThreshold <- 0.05
              }
              refThreshold <- getRefThreshold(object)
              thresholds <- getThresholdValues(geneDataObject, sampName, refThreshold, cols) 
              cnt <- getNumberOfReplicatesPerGene(object) * getNumberOfReplicates(object)
              columns <- c(cols[1])
              layout(1:2)
              for (column in columns) {
                plotSummary(summaries, column, sampName, thresholds[column])
                plotPercentData(geneDataObject, summaries, thresholds[column], 1, column, cnt)
              }
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::plotReplicatesSummaries function 
#-------------------------------------------------------------------------------#
setGeneric("plotReplicatesSummaries",
           function(object) {
             standardGeneric("plotReplicatesSummaries")
           }
)

setMethod("plotReplicatesSummaries",
          signature = signature("CellTCA"),
          definition = function(object) {
            dataNrows <- as.numeric()
            for (i in 1:getNumberOfReplicates(object))
              dataNrows[i] <- getNumberOfDataRows(object@replicates[[i]])
            maxDataRows <- max(dataNrows)
            dataForNorm <- matrix(, maxDataRows, getNumberOfReplicates(object))
            cols <- getModColumnNamesToAnalyze(object)
            dataToSummarize <- NULL
            for (col in cols) {
              for (i in 1:getNumberOfReplicates(object)) {
                data <- getContent(getTCAData(object@replicates[[i]]))
                dataForNorm[1:nrow(data), i] <- as.numeric(data[1:nrow(data), col])
              }
              normalizedData <- normalizeBetweenArrays(dataForNorm, method="quantile")
              if (is.null(dataToSummarize)) {
                dataToSummarize <- data.frame(as.vector(normalizedData))
              }
              else {
                scol <- ncol(dataToSummarize)
                dataToSummarize <- data.frame(cbind(dataToSummarize[,1:scol], 
                                                    as.numeric(normalizedData)))
              }
            }
            names(dataToSummarize) <- cols
            data <- getContent(getTCAData(object@replicates[[which(dataNrows==maxDataRows)]]))
            dataToSummarize$GeneName <- as.character(data$GeneName)
            dataToSummarize <- new("TCAData", data=dataToSummarize)
            dataToSummarize <- getGeneBasedData(dataToSummarize)
            summaries <- getSummaries(dataToSummarize, cols)
            sampName <- getRefSamp(object)
            refThreshold <- getRefThreshold(object)
            if (is.na(sampName)) {
              cat("No reference sample found, plain plots will be triggered\n")
              columns <- c(cols[1])
              layout(1:1)
              for (i in 1:length(cols)) {
                plotPlainSummary(summaries, i, cols[i])
              }
            }
            else {
              if (is.na(refThreshold)) {
                cat("No reference threshold found. Default is : 0.05\n")
                refThreshold <- 0.05
              }
              thresholds <- getThresholdValues(dataToSummarize, sampName, refThreshold, cols)
              cnt <- getNumberOfReplicatesPerGene(object) * getNumberOfReplicates(object)
              cols <- c(cols[1])
              layout(1:2)
              for (i in 1:length(cols)) {
                plotSummary(summaries, i, cols[i], sampName, thresholds[i])
                plotPercentData(dataToSummarize, summaries, thresholds[i], i, cols[i], cnt)
              }
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::plotSummaries function 
#-------------------------------------------------------------------------------#
setGeneric("plotSummaries",
           function(object) {
             standardGeneric("plotSummaries")
           }
)


setMethod("plotSummaries",
          signature = signature("CellTCA"),
          definition = function(object) {
            n <- getNumberOfReplicates(object)
            if (n > 1)
              return(plotReplicatesSummaries(object))
            if (n == 1)
              return(plotNNReplicateSummaries(object, 1))
            print("No TCA plate available!")
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::analyze 
#-------------------------------------------------------------------------------#
setGeneric("analyze",
           function(object, id) {
             standardGeneric("analyze")
           }
)


setMethod("analyze",
          signature = signature("CellTCA"),
          definition = function(object, id) {
            cat(paste(c("Generate Report for Plate : ", id, "\n"), sep=""))
            geneBasedData <- getNormGeneBasedData(object)
            cols <- getModColumnNamesToAnalyze(object)
            summaries <- getSummaries(geneBasedData, cols)
            sampName <- getRefSamp(object)
            pSetup <- getPlateSetup(object)
            if (is.na(sampName)) {
              cat("No reference sample found, plain plots will be triggered\n")
              for (j in 1:length(cols)) {
                cat(paste(c("Generate bar plot for ", cols[j], "\n"), sep=""))
                x11()
                layout(1:1)
                plotPlainSummary(summaries, j, cols[j])
                cat(paste(c("Generate CV plot for ", cols[j], "\n"), sep=""))
                x11()
                layout(1:1)
                plotCV(summaries, pSetup, sampName, cols[j])
              }
            }
            else {
              refThreshold <- getRefThreshold(object)
              if (is.na(refThreshold)) {
                cat("No reference threshold found. Default is : 0.05\n")
                refThreshold <- 0.05
              }
              thresholds <- getThresholdValues(geneBasedData, sampName, refThreshold, cols)
              cnt <- getNumberOfReplicatesPerGene(object)
              for (j in 1:length(cols)) {
                cat(paste(c("Generate bar plot for ", cols[j], "\n"), sep=""))
                x11()
                layout(1:2)
                plotSummary(summaries, j, cols[j], sampName, thresholds[j])
                plotPercentData(geneBasedData, summaries, thresholds[j], j, cols[j], cnt)
                cat(paste(c("Generate CV plot for ", cols[j], "\n"), sep=""))
                x11()
                layout(1:1)
                plotCV(summaries, pSetup, sampName, cols[j])
              }
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getFileNames
#-------------------------------------------------------------------------------#
setGeneric("getFileNames",
           function(object) {
             standardGeneric("getFileNames")
           }
)

setMethod("getFileNames",
          signature = signature("CellTCA"),
          definition = function(object) {
            fnames <- c()
            for (i in 1:getNumberOfReplicates(object)) {
              fnames <- c(fnames, getFileName(object@replicates[[i]]))
            }
            return(fnames)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getSettings
#-------------------------------------------------------------------------------#
setMethod("getSettings",
          signature = signature("CellTCA"),
          definition = function(object) {
            theNames <- paste("File(s) : ", getFileNames(object), collapse=" ")
            infos <- getSettings(object@metaInfo)
            return(c(theNames, infos))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getFormattedSettings
#-------------------------------------------------------------------------------#
setGeneric("getFormattedSettings",
           function(object) {
             standardGeneric("getFormattedSettings")
           }
)

setMethod("getFormattedSettings",
          signature = signature("CellTCA"),
          definition = function(object) {
            preamble <- "\\begin{Schunk}\n\\begin{Soutput}\n"
            fnames <- paste(getFileNames(object), collapse="\t")
            theNames <- paste("File(s) : ", fnames, collapse="\t")
            infos <- paste(getSettings(object@metaInfo), collapse="\n")
            postamble <- "\n\\end{Soutput}\n\\end{Schunk}\n"
            return(paste(c(preamble, theNames, infos, postamble), collapse="\n"))
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::getFormattedPlateSetup
#-------------------------------------------------------------------------------#
setMethod("getFormattedPlateSetup",
          signature = signature("CellTCA"),
          definition = function(object, repId) {
            if (repId == 0) {
              print("Usage : getFormattedPlateSetup(object, repId)")
              print("to get the data from a specific replicate")
              return(NULL)
            }
            if (! outOfRange(object, repId))
              return(getFormattedPlateSetup(object@replicates[[repId]]))
            return(NULL)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getNumberOfReplicatesPerGene
#-------------------------------------------------------------------------------#
setMethod("getNumberOfReplicatesPerGene",
          signature = signature("CellTCA"),
          definition = function(object) {
            geneNames <- getUniqueGeneNames(object)
            geneCnt <- rep(0, length(geneNames))
            names(geneCnt) <- geneNames
            for (i in 1:getNumberOfReplicates(object)) {
              genes <- getNumberOfReplicatesPerGene(object@replicates[[i]])
              geneCnt[names(genes)] <- geneCnt[names(genes)] + genes
            }
            return(geneCnt)
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::plotDensities
#-------------------------------------------------------------------------------#
setGeneric("plotDensities",
           function(object, columnName, ...) {
             standardGeneric("plotDensities")
           }
)


setMethod("plotDensities",
          signature = signature("CellTCA"),
          definition = function(object, columnName, fname, ht, wd) {
            n <- getNumberOfReplicates(object)
            pdf(fname, width=wd, height=ht)
            layout(1:n) 
            for (i in 1:n) {
              tmp <- getContent(getTCAData(object, i))
              maintitle <- paste("Density plot for Replicate ", i, collapse=" ")
              plot(density(as.numeric(tmp[, columnName]), na.rm=T), main=maintitle, xlim=c(-5, 50))
            }
            dev.off()
          }
)


setMethod("getUniqueGeneNames",
          signature = signature("CellTCA"),
          definition = function(object) {
            gnames <- c()
            for (i in 1:getNumberOfReplicates(object))
              gnames <- c(gnames, getUniqueGeneNames(object@replicates[[i]]))
            return(unique(gnames))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getMeanLengths function
#-------------------------------------------------------------------------------#
setGeneric("getMeanLengths",
           function(object) {
             standardGeneric("getMeanLengths")
           }
)


setMethod("getMeanLengths",
          signature = signature("CellTCA"),
          definition = function(object) {
            geneName <- c()
            cellCount <- c()
            for (i in 1:getNumberOfReplicates(object)) {
              tcaData <- getContent(getTCAData(object, i))
              buffer <- as.data.frame(table(tcaData[,c(1,ncol(tcaData))]))
              buffer <- buffer[which(buffer[,3]>0),]
              geneName <- c(geneName, as.vector(buffer$GeneName))
              cellCount <- c(cellCount, as.vector(buffer$Freq))
            }
            dataf <- data.frame(geneName, cellCount)
            results <- split(dataf, factor(dataf$geneName))
            lst <- lapply(results, function(s) {c(summary(s$cellCount), sd=sd(s$cellCount))})
            rmean <- unlist(lapply(lst, function(x) {u <- as.integer(x["Mean"]); names(u) <- NULL; return(u)}))
            rsd <- unlist(lapply(lst, function(x) {u <- x["sd"]; names(u) <- NULL; return(u)}))
            return(list(mean=rmean, sd=rsd))
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getMaxCountCellInWellForGene function
#-------------------------------------------------------------------------------#   
setMethod("getMaxCountCellInWellForGene",
          signature = signature("CellTCA"),
          definition = function(object, geneName) {
            maxCount = 0
            for (i in 1:getNumberOfReplicates(object)) {
              tmpVal = getMaxCountCellInWellForGene(object@replicates[[i]], geneName)
              if (tmpVal > maxCount)
                maxCount = tmpVal
            }
            return(maxCount)
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::getNumberOfWellsForGene function
#-------------------------------------------------------------------------------#   
setMethod("getNumberOfWellsForGene",
          signature = signature("CellTCA"),
          definition = function(object, geneName) {
            count = 0
            for (i in 1:getNumberOfReplicates(object)) {
              count <- count + getNumberOfWellsForGene(object@replicates[[i]], geneName)
            }
            return(count)
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::plotMultiWellDistribution function
#-------------------------------------------------------------------------------#
setGeneric("plotSingleGeneDataDistribution",
           function(object, ...) {
             standardGeneric("plotSingleGeneDataDistribution")
           }
)

setMethod("plotSingleGeneDataDistribution",
          signature = signature("CellTCA"),
          definition = function(object, geneName, col, cutoff) {
            layout(getNumberOfReplicates(object):1)
            wellIds <- NULL
            for (i in 1:getNumberOfReplicates(object)) { 
              dat <- getContent(getTCAData(object, i))
              tmpVal <- table(dat[which(dat$GeneName==geneName), "wellIds"])
              maxCount <- max(tmpVal)
              nbWells <- length(tmpVal)
              if (is.null(wellIds))
                wellIds <- names(tmpVal)
              cellMatrix <- matrix(, maxCount, nbWells)
              dataf <- dat[which(dat$GeneName==geneName), c("wellIds", col)]
              colMatrix <- 1
              for (wellId in wellIds) {
                tmp <- as.numeric(dataf[which(dataf[, 1]==wellId), 2])
                cellMatrix[1:length(tmp), colMatrix] <- tmp
                colMatrix <- colMatrix + 1
              }
              plotDensity(cellMatrix, lty=1, lwd=1, xlim=c(0, cutoff))
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::plotMultiWellDistribution function
#-------------------------------------------------------------------------------#
setGeneric("plotCellNumberDistribution",
           function(object, ...) {
             standardGeneric("plotCellNumberDistribution")
           }
)

setMethod("plotCellNumberDistribution",
          signature = signature("CellTCA"),
          definition = function(object, col, cutoff) {
            layout(getNumberOfReplicates(object):1)
            wellIds <- NULL
            for (i in 1:getNumberOfReplicates(object)) { 
              dat <- getContent(getTCAData(object, i))
              tmpVal <- table(dat[, "wellIds"])
              if (is.null(wellIds))
                wellIds <- names(tmpVal)
              cellData <- c()
              dataf <- dat[, c("wellIds", col)]
              for (wellId in wellIds) {
                cellData <- c(cellData, length(dataf[which(dataf[, 1]==wellId), 2]))
              }
              plot(density(cellData), lty=1, lwd=1, xlim=c(0, cutoff))
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::plotGeneDistribution function
#-------------------------------------------------------------------------------#
setGeneric("getGeneDataDistribution",
           function(object, geneName, repId, col, ...) {
             standardGeneric("getGeneDataDistribution")
           }
)

setMethod("getGeneDataDistribution",
          signature = signature("CellTCA"),
          definition = function(object, geneName, repId, col, ...) {
            dat <- getContent(getTCAData(object, repId))
            tmpVal <- table(dat[which(dat$GeneName==geneName), "wellIds"])
            maxCnt <- max(tmpVal)
            print(tmpVal)
            cells <- matrix(, maxCnt, length(tmpVal))
            wellIds <- names(tmpVal)
            for (k in 1:length(wellIds)) {
              tmp <- as.vector(dat[which(dat[, "wellIds"]==wellIds[k]), c(col)])
              cells[1:length(tmp),k] <- as.numeric(tmp)
            }
            return(cells)
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::plotUniqueGeneData function
#-------------------------------------------------------------------------------#
setGeneric("plotUniqueGeneData",
           function(object, geneName, repId, col, x_beg, x_end, y_beg=0, y_end=0.3, ...) {
             standardGeneric("plotUniqueGeneData")
           }
)

setMethod("plotUniqueGeneData",
          signature = signature("CellTCA"),
          definition = function(object, geneName, repId, col, x_beg, x_end, y_beg, y_end,...) {
            cells <- getGeneDataDistribution(object, geneName, repId, col)
            plot(density(cells[,1], na.rm=TRUE), xlim=c(x_beg, x_end), ylim=c(y_beg, y_end))
            if (ncol(cells) > 1) {
              for (j in 2:ncol(cells)) {
                lines(density(cells[, j], na.rm=TRUE), col=j, xlim=c(x_beg, x_end), ylim=c(y_beg, y_end))
              }
              x11()
              plot(density(as.vector(cells), na.rm=TRUE), col=ncol(cells)+1, xlim=c(x_beg, x_end), ylim=c(y_beg, y_end))
            }
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::plotUniqueGeneDataOverPlates function
#-------------------------------------------------------------------------------#
setGeneric("plotUniqueGeneDataOverPlates",
           function(object, geneName, col, x_beg, x_end, y_beg=0, y_end=0.3, ...) {
             standardGeneric("plotUniqueGeneDataOverPlates")
           }
)

setMethod("plotUniqueGeneDataOverPlates",
          signature = signature("CellTCA"),
          definition = function(object, geneName, col, x_beg, x_end, y_beg, y_end,...) {
            allcells <- c()
            cells <- getGeneDataDistribution(object, geneName, 1, col)
            plot(density(as.vector(cells), na.rm=TRUE), xlim=c(x_beg, x_end), ylim=c(y_beg, y_end))
            allcells <- c(allcells, as.vector(cells))
            if (getNumberOfReplicates(object) > 1) {
              for (j in 2:getNumberOfReplicates(object)) {
                cells <- getGeneDataDistribution(object, geneName, j, col)
                allcells <- c(allcells, as.vector(cells))
                lines(density(as.vector(cells), na.rm=TRUE), col=j, xlim=c(x_beg, x_end), ylim=c(y_beg, y_end))
              }
              x11()
              plot(density(allcells, na.rm=TRUE), col=ncol(cells)+1, xlim=c(x_beg, x_end), ylim=c(y_beg, y_end))
            }
          }
)


#-------------------------------------------------------------------------------#
# CellTCA::getControls function
#-------------------------------------------------------------------------------#
setMethod("getControls",
          signature = signature("CellTCA"),
          definition = function(object, ...) {
            controls <- c()
            for (i in (1:getNumberOfReplicates(object))) {
              controls <- c(controls, getControls(object@replicates[[i]]))
            }
            return(unique(controls))
          }
)



#-------------------------------------------------------------------------------#
# CellTCA::getWellNormGeneBasedDataEnhanced function
#-------------------------------------------------------------------------------#
setGeneric("getWellNormGeneBasedDataEnhanced_unop",
           function(object, ...) {
             standardGeneric("getWellNormGeneBasedDataEnhanced_unop")
           }
)

setMethod("getWellNormGeneBasedDataEnhanced_unop",
          signature = signature("CellTCA"),
          definition = function(object, median, log, geneSVMLabels, file.output) {
            # No intra plate normalization available
            if (getNumberOfReplicates(object) == 1)
              return(getGeneBasedData(object, 1))
            
            # Better be cautious in case a gene is found 
            # in one plate and not in another one  
            geneNames <- sort(getUniqueGeneNames(object))
            # Build a matrix n replicates x n genes
            # Each row will contain the number records for each gene
            # within that replicate
            geneTabNames <- matrix(, getNumberOfReplicates(object), length(geneNames))
            wellTabCounts <- matrix(, getNumberOfReplicates(object), length(geneNames))
            for (i in 1:getNumberOfReplicates(object)) {
              tmpWellGeneNames <- getWellGeneNameLengths(object@replicates[[i]])
              for (g in 1:length(geneNames)) {
                ttmp = tmpWellGeneNames[which(tmpWellGeneNames[, 2]==geneNames[g]), 3]
                cnt_g = 0
                if (length(ttmp)) {
                  cnt_g = max(ttmp)
                }
                geneTabNames[i,g] = cnt_g
                wellTabCounts[i, g] = length(ttmp)
              }
            }
            # Take the maximum count over the three replicates for each gene
            geneCnt <- apply(geneTabNames, 2, max)
            
            # Here the maximum gene entries
            maxDataRows <- sum(geneCnt)
            
            cols <- sort(getModColumnNamesToAnalyze(object))
            dataToSummarize <- NULL
            for (k in 1:length(cols)) {
              colData <- c() 
              for (i in 1:length(geneNames)) {   
                dataForNorm <- c()
                # If a gene is missing in a replicate
                # delCol will prevent from performing normalization
                # with a NA column
                valid = FALSE
                geneLabels <- as.vector(geneSVMLabels[i, k, ])
                for (j in 1:getNumberOfReplicates(object)) {
                  if (j == 1)
                    valid = (geneLabels[j] | geneLabels[j+1])
                  else if (j == 2)
                    valid = (geneLabels[j-1] | geneLabels[j+1])
                  else if (j == 3)
                    valid = (geneLabels[j-1] | geneLabels[j])
                  else
                    stop("getWellNormGeneBasedData : wrong number of replicates\n")
                  ## add replicate if pass SVM test
                  if (valid) { 
                    tmpWellGeneNames <- getWellGeneNameLengths(object@replicates[[j]])  
                    wells = tmpWellGeneNames[which(tmpWellGeneNames[, 2] == geneNames[i]), 1]
                    for (w in 1:length(wells)) {
                      dataTmp <- getWellTCAData(object@replicates[[j]], wells[w])  
                      if (length(dataTmp[, cols[k]]) & length(which(!is.na(dataTmp[, cols[k]])))) {
                        #print(paste("Detecting col for ", geneNames[i], " in ", wells[w], sep=""))
                        # Making sure that column is not an na column
                        dataForNormTmp <- rep(NA, geneCnt[i])
                        dataForNormTmp[1:nrow(dataTmp)] <- as.numeric(dataTmp[1:nrow(dataTmp), cols[k]])
                        dataForNorm <- c(dataForNorm, dataForNormTmp)
                      }
                    }
                  }
                  else {
                    xdata <- getDataInfo(object, j)
                    file <- getFileName(xdata)
                    cat("!!!!  \"",file,"\" : FAIL TO SVM TEST !!!! \n")
                    #writeLines(paste("FAIL TO SVM TEST  : ",file, sep=""), con=file.output, sep = "\n")
                    cat(paste("FAIL TO SVM TEST  : ",file,"\n", sep=""), file=file.output, append=TRUE)
                  }
                }
                dataForNorm <- matrix(dataForNorm, nrow=geneCnt[i])  
                if (is.matrix(dataForNorm)) {
                  normalizedData <- normalizeBetweenArrays(dataForNorm, method="quantile")
                  
                  if (log == T) {
                    normalizedData <- log2(normalizedData)
                  }
                  
                  if (median == T) {
                    normalizedData <- apply(normalizedData, 1, median, na.rm = T)
                  }
                  
                }
                else {
                  normalizedData <- dataForNorm
                }
                # the data is organized on a column based
                # each line will consist of gene id and column values
                # As each each column represents the same distribution,
                # we only need one of them. Preferably, one without na
                # or with less na entries
                if (is.matrix(normalizedData)) {
                  naCount <- apply(normalizedData, 2, function(u) length(which(is.na(u))))
                  minCount <- min(naCount)
                  colLeader <- which(naCount==minCount)[1]
                  colData <- c(colData, normalizedData[, colLeader])
                }
                else {
                  colData <- c(colData, normalizedData) 
                }
              }
              if (is.null(dataToSummarize)) {
                dataToSummarize <- data.frame(colData)
              }
              else {
                scol <- ncol(dataToSummarize)
                dataToSummarize <- data.frame(cbind(dataToSummarize[,1:scol], 
                                                    as.numeric(colData)))
              }
            }
            names(dataToSummarize) <- cols
            # Collect gene names for entries in the global data frame
            dataToSummarize$GeneName <- rep(geneNames, geneCnt)
            dataToSummarize <- new("TCAData", data=dataToSummarize)
#             if (log == F) {
#               object@normData = dataToSummarize
#             }
#             else {
#               object@normDataLog = dataToSummarize
#             }
#             object@isNormalized = TRUE
            return(getGeneBasedData(dataToSummarize))
          }
)

getWellNormGeneBasedDataEnhanced <- compiler::cmpfun(getWellNormGeneBasedDataEnhanced_unop)

#-------------------------------------------------------------------------------#
# CellTCA::validateGenedata function
#-------------------------------------------------------------------------------#
setGeneric("validateTCAGeneData_unop",
           function(object, svmModel, ...) {
             standardGeneric("validateTCAGeneData_unop")
           }
)

setMethod("validateTCAGeneData_unop",
          signature = signature("CellTCA"),
          definition = function(object, svmModel, ...) {
            geneNames <- sort(getUniqueGeneNames(object))
            cols <- sort(getModColumnNamesToAnalyze(object))
            dataLabels <- array(0, dim=c(length(geneNames), length(cols), 3)) 
            cellNumCutoff = 20
            for (k in 1:length(cols)) {
              for (i in 1:length(geneNames)) {
                #print(geneNames[i])
                dat1 <- NULL
                dat2 <- NULL
                dat3 <- NULL  
                for (j in 1:getNumberOfReplicates(object)) {
                  tmpWellGeneNames <- getWellGeneNameLengths(object@replicates[[j]])  
                  wellCnts = tmpWellGeneNames[which(tmpWellGeneNames[, 2] == geneNames[i]), c(1,3)]
                  maxCnt = max(wellCnts[, 2])
                  nflag = 0
                  dataForNorm <- c()
                  for (w in 1:length(wellCnts[, 1])) {
                    dataTmp <- as.numeric(getWellTCAData(object@replicates[[j]], wellCnts[w, 1], cols[k]))
                    if (length(dataTmp)) {
                      #print(paste("Replicate for ", wellCnts[w, 1], sep=""))
                      nflag <- nflag + 1
                      dataForNormTmp <- rep(NA, maxCnt)
                      dataForNormTmp[1:length(dataTmp)] <- dataTmp
                      dataForNorm <- c(dataForNorm, dataForNormTmp)
                    }
                  }
                  if (nflag > 1) {
                    #print(paste("Normalization for ", geneNames[i], sep=""))
                    dataForNorm <- matrix(dataForNorm, nrow=maxCnt)  
                    #normalizedData <- normalizeBetweenArrays(dataForNorm, method="quantile")
                    #naCount <- apply(normalizedData, 2, function(u) length(which(is.na(u))))
                    naCount <- apply(dataForNorm, 2, function(u) length(which(is.na(u))))
                    minCount <- min(naCount)
                    colLeader <- which(naCount==minCount)[1]
                    dataTmp <- normalizedData[, colLeader]
                  }
                  else {
                    dataTmp <- dataForNorm 
                  }
                  if (j == 1) {
                    dat1 <- dataTmp
                    qdat <- quantile(dat1, probs=c(0.05, 0.95), na.rm=TRUE)
                    dat1 <- dat1[which((dat1>=qdat[1])&(dat1<=qdat[2]))]
                  }
                  else if (j == 2) {
                    dat2 <- dataTmp
                    qdat <- quantile(dat2, probs=c(0.05, 0.95), na.rm=TRUE)
                    dat2 <- dat2[which((dat2>=qdat[1])&(dat2<=qdat[2]))]
                  }
                  else if (j == 3) {
                    dat3 <- dataTmp
                    qdat <- quantile(dat3, probs=c(0.05, 0.95), na.rm=TRUE)
                    dat3 <- dat3[which((dat3>=qdat[1])&(dat3<=qdat[2]))]
                  }
                  else
                    stop("validateGeneData: too many replicates")
                }
                if ((length(dat1)>cellNumCutoff) & (length(dat2)>cellNumCutoff) & (length(dat3)>cellNumCutoff)) {
                  gridsize = max(2000, max(length(dat1), length(dat2), length(dat3))/10)
                  # KLD for all
                  distances1 <- as.vector(KLdist.matrix(list(dat1, dat2, dat3), gridsize=gridsize))
                  distances2 <- as.vector(KLdist.matrix(list(dat3, dat2, dat1), gridsize=gridsize)) 
                  distances2 <- distances2[length(distances2):1]
                  dat <- data.frame(D1=distances1, D2=distances2)
                  #print(dat)
                  prediction <- predict(svmModel, dat, probability=T)  
                  #print(prediction)        
                  dataLabels[i, k, 1:3] <- as.integer(prediction=='P')
                  #print(dataLabels[i, k, 1:3])
                  if (sum(dataLabels[i, k, 1:3]) == 0) {
                    probs <- attr(prediction, 'probabilities')[, "P"]
                    dataLabels[i, k, which(probs == max(probs))] <- 1
                    #print(dat)
                    #print(prediction)
                    #print(dataLabels[i, k, 1:3])
                  }
                } 
                else if ((length(dat1)>cellNumCutoff) & (length(dat2)>cellNumCutoff)) {
                  # KLD for 1 and 2
                  dataLabels[i, k, 1] = 1
                }
                else if ((length(dat1)>cellNumCutoff) & (length(dat3)>cellNumCutoff)) {
                  # KLD for 1 and 3
                  dataLabels[i, k, 2] <- 1 
                }
                else if ((length(dat2)>cellNumCutoff) & (length(dat3)>cellNumCutoff)) {
                  # KLD for 2 and 3
                  dataLabels[i, k, 3] <- 1
                }
                else {
                  dataLabels[i, k, 1:3] <- rep(1, 3)
                }
              }
            }
            return(dataLabels) 
          }
)

validateTCAGeneData <- compiler::cmpfun(validateTCAGeneData_unop)




















#-------------------------------------------------------------------------------#
# CellTCA::getWellNormGeneBasedData function
#-------------------------------------------------------------------------------#
setGeneric("getWellNormGeneBasedData_test_unop",
           function(object, median) {
             standardGeneric("getWellNormGeneBasedData_test_unop")
           }
)

setMethod("getWellNormGeneBasedData_test_unop",
          signature = signature("CellTCA"),
          definition = function(object, median) {
            # No intra plate normalization available
            if (getNumberOfReplicates(object) == 1)
              return(getGeneBasedData(object, 1))
            
            # Better be cautious in case a gene is found 
            # in one plate and not in another one  
            geneNames <- getUniqueGeneNames(object)
            # Build a matrix n replicates x n genes
            # Each row will contain the number records for each gene
            # within that replicate
            geneTabNames <- matrix(, getNumberOfReplicates(object), length(geneNames))
            for (i in 1:getNumberOfReplicates(object)) {
              tmpGeneNames <- getCntGeneNames(object@replicates[[i]])
              tmpGeneNames <- tmpGeneNames[geneNames]
              tmpGeneNames[which(is.na(tmpGeneNames))] <- 0
              geneTabNames[i,] <- tmpGeneNames
            }
            # Take the maximum count over the three replicates for each gene
            geneCnt <- apply(geneTabNames, 2, max)
            delCols <- rep(0, length(geneCnt))
            # Here the maximum gene entries
            maxDataRows <- sum(geneCnt)
            
            cols <- getModColumnNamesToAnalyze(object)
            dataToSummarize <- NULL
            firstCol <- TRUE
            for (col in cols) {
              colData <- c() 
              for (i in 1:length(geneNames)) {   
                dataForNorm <- matrix(, geneCnt[i], getNumberOfReplicates(object))
                # If a gene is missing in a replicate
                # delCol will prevent from performing normalization
                # with a NA column
                delCol <- 0
                for (j in 1:getNumberOfReplicates(object)) {
                  dataTmp <- getGeneNameTCAData(object@replicates[[j]], geneNames[i])
                  if (length(dataTmp[, col]) & length(which(!is.na(dataTmp[, col])))) {
                    # Making sure that column is not an na column
                    if (delCol != 2) {
                      dataForNorm[1:nrow(dataTmp), j-delCol] <- as.numeric(dataTmp[1:nrow(dataTmp), col])
                    }
                    else {
                      dataForNorm[1:nrow(dataTmp)] <- as.numeric(dataTmp[1:nrow(dataTmp), col])
                    }
                  }
                  else {
                    # In case of an na column, we need to remove it from dataForNorm
                    # reducing the number of replicates by 1
                    # We also need to update delCol to take into account the removed
                    # column in the coming steps 
                    dataForNorm <- dataForNorm[, -(j-delCol)]
                    delCol <- delCol + 1
                  }
                }
                if (is.matrix(dataForNorm)) {
                  normalizedData <- normalizeBetweenArrays(dataForNorm, method="quantile")
                  
                  if (median == T) {
                    normalizedData <- apply(normalizedData, 1, median, na.rm = T)
                  }
                  
                }
                else {
                  normalizedData <- dataForNorm
                }
                # the data is organized on a column based
                # each line will consist of gene id and column values
                # As each each column represents the same distribution,
                # we only need one of them. Preferably, one without na
                # or with less na entries
                if (is.matrix(normalizedData)) {
                  naCount <- apply(normalizedData, 2, function(u) length(which(is.na(u))))
                  minCount <- min(naCount)
                  colLeader <- which(naCount==minCount)[1]
                  colData <- c(colData, normalizedData[, colLeader])
                }
                else {
                  colData <- c(colData, normalizedData) 
                }
                if (firstCol) {
                  delCols[i] <- delCol
                }
              }
              if (is.null(dataToSummarize)) {
                dataToSummarize <- data.frame(colData)
              }
              else {
                scol <- ncol(dataToSummarize)
                dataToSummarize <- data.frame(cbind(dataToSummarize[,1:scol], 
                                                    as.numeric(colData)))
              }
              firstCol = FALSE
            }
            names(dataToSummarize) <- cols
            # Collect gene names for entries in the global data frame
            dataToSummarize$GeneName <- rep(geneNames, geneCnt)
            dataToSummarize <- new("TCAData", data=dataToSummarize)
            object@normData = dataToSummarize
            object@isNormalized = TRUE
            return(object)
          }
)

getWellNormGeneBasedData_test <- compiler::cmpfun(getWellNormGeneBasedData_test_unop)



