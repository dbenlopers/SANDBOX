###################################################################################
# class definition for TCA replicate
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
###################################################################################
setClass(
  Class = "TCAReplicate",
  representation = representation(
    data = "TCAData",
    info = "TCADataInfo",
    plateSetup = "TCAPlateSetup",
    summaries = "TCASummaries"
  ),
  prototype = prototype(
    data = NULL,
    plateSetup = NULL,
    info = NULL
  )
)


#----------------------------------------------------------------------------------
# TCAReplicates::print function
#----------------------------------------------------------------------------------
setMethod("print",
          signature = signature("TCAReplicate"),
          definition = function(x, ...) {
            cat("\n*** Class TCAReplicate - Method print ***\n\n")
            print(x@info)
            cat("\n\n")
            print(x@plateSetup)
            cat("\n\n")
            print(x@data)
          }
)


#----------------------------------------------------------------------------------
# TCAReplicate::show function
#----------------------------------------------------------------------------------
setMethod("show",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            cat("\n*** Class TCA Replicate - Method show ***\n\n")
            show(object@info)
            cat("\n\n")
            show(object@plateSetup)
            cat("\n\n")
            show(object@data)
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getContent function
# return the content of the TCAReplicate object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("TCAReplicate"),
          definition = function(object, repId, ...) {
            return(list(info = getContent(object@info),
                        data = getContent(object@data)))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getPlateSetup function
#-------------------------------------------------------------------------------#
setGeneric("getPlateSetup",
           function(object, ...) {
             standardGeneric("getPlateSetup")
           }
)


setMethod("getPlateSetup",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(object@plateSetup)
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getTCAData function
#-------------------------------------------------------------------------------#
setGeneric("getTCAData",
           function(object, repId=0) {
             standardGeneric("getTCAData")
           }
)

setMethod("getTCAData",
          signature = signature("TCAReplicate"),
          definition = function(object, repId=0) {
            return(object@data)
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getDataInfo function
#-------------------------------------------------------------------------------#
setGeneric("getDataInfo",
           function(object, repId=1, ...) {
             standardGeneric("getDataInfo")
           }
)

setMethod("getDataInfo",
          signature = signature("TCAReplicate"),
          definition = function(object, repId, ...) {
            return(object@info)
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getDataToAnalyze function
# returns columns of the data selected for analysis
#-------------------------------------------------------------------------------#
setMethod("getDataToAnalyze",
          signature = signature("TCAReplicate"),
          definition = function(object, columnNamesToAnalyze=NULL) {
            if (is.null(columnNamesToAnalyze)) {
              print("You need to specify the column names you want your data from!")
              print("Usage : getDataToAnalyze(object, columnNames)")
              return(NULL)
            }
            return(getDataToAnalyze(object@data, columnNamesToAnalyze))
          }
)

#-------------------------------------------------------------------------------#
# TCAReplicate::getGeneBasedData function
#-------------------------------------------------------------------------------#
setMethod("getGeneBasedData",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getGeneBasedData(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getNumberOfDataRows function
#-------------------------------------------------------------------------------#
setMethod("getNumberOfDataRows",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getNumberOfDataRows(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getNumberOfDataColumns function
#-------------------------------------------------------------------------------#
setMethod("getNumberOfDataColumns",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getNumberOfDataColumns(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getNumberOfDataRows function
#-------------------------------------------------------------------------------#
setMethod("getNumberOfDataRows",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getNumberOfDataRows(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getFileName function
#-------------------------------------------------------------------------------#
setMethod("getFileName",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getFileName(object@info))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getUniqueGeneNames function
#-------------------------------------------------------------------------------#
setMethod("getUniqueGeneNames",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getUniqueGeneNames(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getCntGeneNames function
#-------------------------------------------------------------------------------#
setMethod("getCntGeneNames",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getCntGeneNames(object@data))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getGeneNameTCAData function
#-------------------------------------------------------------------------------#
setMethod("getGeneNameTCAData",
          signature = signature("TCAReplicate"),
          definition = function(object, geneName) {
            return(getGeneNameTCAData(object@data, geneName))
          }
)



#-------------------------------------------------------------------------------#
# TCAReplicate::getFormattedPlateSetup
#-------------------------------------------------------------------------------#
setMethod("getFormattedPlateSetup",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getFormattedPlateSetup(object@plateSetup))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getNumberOfReplicatesPerGene
#-------------------------------------------------------------------------------#
setMethod("getNumberOfReplicatesPerGene",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getNumberOfReplicatesPerGene(object@plateSetup))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getMaxCountCellInWellForGene function
#-------------------------------------------------------------------------------#
setMethod("getMaxCountCellInWellForGene",
          signature = signature("TCAReplicate"),
          definition = function(object, geneName) {
            return(getMaxCountCellInWellForGene(object@data, geneName))
          }
)



#-------------------------------------------------------------------------------#
# TCAReplicate::getNumberOfWellsForGene function
#-------------------------------------------------------------------------------#   
setMethod("getNumberOfWellsForGene",
          signature = signature("TCAReplicate"),
          definition = function(object, geneName) {
            return(getNumberOfWellsForGene(object@data, geneName))
          }
)


#-------------------------------------------------------------------------------#
# TCAReplicate::getWellDataForGene function
#-------------------------------------------------------------------------------#
setMethod("getWellDataForGene",
          signature = signature("TCAReplicate"),
          definition = function(object, geneName, col) {
            return(getWellDataForGene(object@data, geneName, col))
          }
)



#-------------------------------------------------------------------------------#
# TCAReplicate::getControls function
#-------------------------------------------------------------------------------#
setMethod("getControls",
          signature = signature("TCAReplicate"),
          definition = function(object, ...) {
            return(getControls(object@data))
          }
)

#-------------------------------------------------------------------------------#
# TCAReplicate::getWellGeneNameLengths function
#-------------------------------------------------------------------------------#
setMethod("getWellGeneNameLengths",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getWellGeneNameLengths(object@data))
          }
)

#-------------------------------------------------------------------------------#
# TCAReplicate::getWellTCAData function
#-------------------------------------------------------------------------------#
setMethod("getWellTCAData",
          signature = signature("TCAReplicate"),
          definition = function(object, wellName, col=NULL) {
            return(getWellTCAData(object@data, wellName, col))
          }
)


