
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
# TCAReplicate::getGeneBasedData function
#-------------------------------------------------------------------------------#
setMethod("getGeneBasedData",
          signature = signature("TCAReplicate"),
          definition = function(object) {
            return(getGeneBasedData(object@data))
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


#-------------------------------------------------------------------------------#
# TCAReplicate::getGeneNameTCAData function
#-------------------------------------------------------------------------------#
setMethod("getGeneNameTCAData",
          signature = signature("TCAReplicate"),
          definition = function(object, geneName, col=NULL) {
            return(getGeneNameTCAData(object@data, geneName, col))
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
# TCAReplicate::getControls function
#-------------------------------------------------------------------------------#
setMethod("getControls",
          signature = signature("TCAReplicate"),
          definition = function(object, ...) {
            return(getControls(object@data))
          }
)