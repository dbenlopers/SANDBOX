###################################################################################
# class definition for TCA Data
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
###################################################################################
setClass(
  Class = "TCAData",
  representation = representation(
    data = "data.frame"
  ),
  prototype = prototype(
    data = data.frame(0)
  )
)



#--------------------------------------------------------------------------------
# TCAData::print function
#--------------------------------------------------------------------------------
setMethod("print", 
          signature = signature("TCAData"),
          definition = function(x, ...) {
            cat("\n***	Class TCAData - Method print ****\n\n")
            cat("*** Only the first 100 entries of the data matrix ***\n\n")
            print(x@data[1:100,])
          }
)


#---------------------------------------------------------------------------------
# TCAData::show function
#---------------------------------------------------------------------------------
setMethod("show",
          signature = signature("TCAData"),
          definition = function(object) {
            cat("\n***  Class TCAData - Method show ****\n\n")
            cat(paste(c("Matrix : ", nrow(object@data), " x ", ncol(object@data), " intensity values"), collapse=""))
            cat("\n")
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getContent function
# return the Data content of the TCAData object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("TCAData"),
          definition = function(object, repId, ...) {
            return(object@data)
          }
)




#-------------------------------------------------------------------------------#
# TCAData::getDataToAnalyze function
# return a data.frame where the columns are the data to analyze
#-------------------------------------------------------------------------------#
setGeneric("getDataToAnalyze",
           function(object, columnNamesToAnalyze=NULL) {
             standardGeneric("getDataToAnalyze")
           }
)

setMethod("getDataToAnalyze", 
          signature = signature("TCAData"),
          definition = function(object, columnNamesToAnalyze=NULL) {
            if (is.null(columnNamesToAnalyze)) {
              print("You need to specify the column names you want your data from!")
              print("Usage : getDataToAnalyze(object, columnNames)")
              return(NULL)
            }
            wellIds <- gsub("(\\s\\-\\s|\\(fld\\s+\\d+\\)$)", '',object@data[,"Well"], perl=TRUE)
            return(cbind(wellIds, object@data[,columnNamesToAnalyze]))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getGeneBasedData function
# return the data related to genes in TCAGeneBasedData object
#-------------------------------------------------------------------------------#
setMethod("getGeneBasedData",
          signature = signature("TCAData"),
          definition = function(object) {
            data <- split(object@data,factor(object@data$GeneName))
            return(new("TCAGeneBasedData", data=data))	
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getNumberOfDataRows function
#-------------------------------------------------------------------------------#
setGeneric("getNumberOfDataRows",
           function(object) {
             standardGeneric("getNumberOfDataRows")
           }
)


setMethod("getNumberOfDataRows",
          signature = signature("TCAData"),
          definition = function(object) {
            return(nrow(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getNumberOfDataColumns function
#-------------------------------------------------------------------------------#
setGeneric("getNumberOfDataColumns",
           function(object) {
             standardGeneric("getNumberOfDataColumns")
           }
)


setMethod("getNumberOfDataColumns",
          signature = signature("TCAData"),
          definition = function(object) {
            return(ncol(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getNumberOfDataRows function
#-------------------------------------------------------------------------------#
setGeneric("getNumberOfDataRows",
           function(object) {
             standardGeneric("getNumberOfDataRows")
           }
)


setMethod("getNumberOfDataRows",
          signature = signature("TCAData"),
          definition = function(object) {
            return(nrow(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getUniqueGeneNames function
#-------------------------------------------------------------------------------#
setGeneric("getUniqueGeneNames",
           function(object) {
             standardGeneric("getUniqueGeneNames")
           }
)


setMethod("getUniqueGeneNames",
          signature = signature("TCAData"),
          definition = function(object) {
            return(unique(object@data$GeneName))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getCntGeneNames function
#-------------------------------------------------------------------------------#
setGeneric("getCntGeneNames",
           function(object) {
             standardGeneric("getCntGeneNames")
           }
)


setMethod("getCntGeneNames",
          signature = signature("TCAData"),
          definition = function(object) {
            return(table(object@data$GeneName))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getGeneNameTCAData function
#-------------------------------------------------------------------------------#
setGeneric("getGeneNameTCAData",
           function(object, geneName) {
             standardGeneric("getGeneNameTCAData")
           }
)

setMethod("getGeneNameTCAData",
          signature = signature("TCAData"),
          definition = function(object, geneName) {
            return(object@data[which(object@data[, "GeneName"]==geneName), ])
          }
)



#-------------------------------------------------------------------------------#
# TCAData::getMaxCountCellInWellForGene function
#-------------------------------------------------------------------------------#
setGeneric("getMaxCountCellInWellForGene",
           function(object, geneName) {
             standardGeneric("getMaxCountCellInWellForGene")
           }
)

setMethod("getMaxCountCellInWellForGene",
          signature = signature("TCAData"),
          definition = function(object, geneName) {
            tmpVal <- object@data[which(object@data$GeneName==geneName), "wellIds"]
            return(max(table(tmpVal)))
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getNumberOfWellsForGene function
#-------------------------------------------------------------------------------#
setGeneric("getNumberOfWellsForGene",
           function(object, geneName) {
             standardGeneric("getNumberOfWellsForGene")
           }
)

setMethod("getNumberOfWellsForGene",
          signature = signature("TCAData"),
          definition = function(object, geneName) {
            return(length(table(object@data[which(object@data$GeneName==geneName), "wellIds"])))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getWellDataForGene function
#-------------------------------------------------------------------------------#
setGeneric("getWellDataForGene",
           function(object, geneName, col) {
             standardGeneric("getWellDataForGene")
           }
)


setMethod("getWellDataForGene",
          signature = signature("TCAData"),
          definition = function(object, geneName, col) {
            return(object@data[which(object@data$GeneName==geneName), c("wellIds", col)]) 
          }
)



#-------------------------------------------------------------------------------#
# TCAData::getControls function
#-------------------------------------------------------------------------------#
setGeneric("getControls",
           function(object, ...) {
             standardGeneric("getControls")
           }
)


setMethod("getControls",
          signature = signature("TCAData"),
          definition = function(object, ...) {
            dtmp <- object@data
            controls <- unique(dtmp[grep("^B", dtmp$wellIds, perl=TRUE), "GeneName"])
            controls <- c(controls, unique(dtmp[grep("^G", dtmp$wellIds, perl=TRUE), "GeneName"]))
            return(controls)
          }
)


#-------------------------------------------------------------------------------#
# TCAData::getWellGeneNameLengths function
#-------------------------------------------------------------------------------#
setGeneric("getWellGeneNameLengths",
           function(object) {
             standardGeneric("getWellGeneNameLengths")
           }
)


setMethod("getWellGeneNameLengths",
          signature = signature("TCAData"),
          definition = function(object) {
            results = as.data.frame(table(object@data[, c("wellIds", "GeneName")]))
            return(results[which(results[, 3]>0), ])
          }
)

#-------------------------------------------------------------------------------#
# TCAData::getWellTCAData function
#-------------------------------------------------------------------------------#
setGeneric("getWellTCAData",
           function(object, wellName, ...) {
             standardGeneric("getWellTCAData")
           }
)


setMethod("getWellTCAData",
          signature = signature("TCAData"),
          definition = function(object, wellName, col=NULL) {
            if (is.null(col))
              return(object@data[which(object@data[, "wellIds"]==wellName), ])
            return(object@data[which(object@data[, "wellIds"]==wellName), col]) 
          }
)