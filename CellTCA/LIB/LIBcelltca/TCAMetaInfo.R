#################################################################################
# class definition for TCA MetaInfo
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
#################################################################################
setClass(
  Class = "TCAMetaInfo",
  representation = representation(
    metaInfo = "character"
  ),
  prototype = prototype(
    metaInfo = character(0)
  )
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::print function
#-------------------------------------------------------------------------------#
setMethod("print",
          signature = signature("TCAMetaInfo"),
          definition = function(x, ...) {
            cat("\n**** Class TCAMetaInfo - Method print ****\n\n")
            tnames <- names(x@metaInfo)
            l <- length(tnames)
            for (i in 1:l)
              print(paste(c(tnames[i], x@metaInfo[i]), collapse=" : "))
            cat("\n")
          }
)

#---------------------------------------------------------------------------------#
# TCAMetaInfo::show function
#---------------------------------------------------------------------------------#
setMethod("show",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            cat("\n**** Class TCAMetaInfo - Method show ****\n\n")
            tnames <- names(object@metaInfo)
            l <- length(tnames)
            for (i in 1:l)
              print(paste(c(tnames[i], object@metaInfo[i]), collapse=" : "))
            cat("\n")
          }
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::getContent function
# return the content of the TCAMetaInfo object
#-------------------------------------------------------------------------------#
setGeneric("getContent",
           function(object, repId=1, ...) {
             standardGeneric("getContent")
           }
)

setMethod("getContent",
          signature = signature("TCAMetaInfo"),
          definition = function(object, repId, ...) {
            return(object@metaInfo)
          }
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::getColumnNamesToAnalyze function
# return a vector of columns to analyze
#-------------------------------------------------------------------------------#
setGeneric("getColumnNamesToAnalyze",
           function(object) {
             standardGeneric("getColumnNamesToAnalyze")
           }
)

setMethod("getColumnNamesToAnalyze",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            mInfo <- getContent(object)
            return(mInfo[grep("analyze", names(mInfo))])
          }
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::getModColumnNamesToAnalyze function
# return a vector of columns to analyze
#-------------------------------------------------------------------------------#
setGeneric("getModColumnNamesToAnalyze",
           function(object) {
             standardGeneric("getModColumnNamesToAnalyze")
           }
)

setMethod("getModColumnNamesToAnalyze",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            mInfo <- getContent(object)
            return(return(gsub("[\\s\\-]", "", mInfo[grep("analyze", names(mInfo))], , perl=TRUE)))
          }
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::getRefThreshold
# return threshold value
#-------------------------------------------------------------------------------#
setGeneric("getRefThreshold",
           function(object) {
             standardGeneric("getRefThreshold")
           }
)

setMethod("getRefThreshold",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            return(as.numeric(object@metaInfo["refThreshold"]))
          }
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::getRefSamp
# return reference sample name
#-------------------------------------------------------------------------------#
setGeneric("getRefSamp",
           function(object) {
             standardGeneric("getRefSamp")
           }
)

setMethod("getRefSamp",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            return(object@metaInfo["refSamp"])
          }
)


#--------------------------------------------------------------------------------#
# TCAMetaInfo::checkMetaInfo returns some warnings given
# each replicate should have the metaInfo data
#--------------------------------------------------------------------------------#
setGeneric("checkMetaInfo",
           function(object1, object2) {
             standardGeneric("checkMetaInfo")
           }
)

setMethod("checkMetaInfo",
          signature = signature("TCAMetaInfo"),
          definition = function(object1, object2) {
            columns <- names(object1)[c(-1, -10)]
            mywarnings <-character(0)
            for (name in columns) {
              if (object1@metaInfo[name] != object2@metaInfo[name]) {
                mywarnings <- c(mywarnings, paste(c(object1@metaInfo[name],
                                                    " and ", object2@metaInfo, " are not the same"), collapse=""))
              }
            }
            return(mywarnings)
          }
)


#-------------------------------------------------------------------------------#
# TCAMetaInfo::getSettings
#-------------------------------------------------------------------------------#
setGeneric("getSettings",
           function(object) {
             standardGeneric("getSettings")
           }
)

setMethod("getSettings",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            tnames <- names(object@metaInfo)
            results <- c()
            l <- length(tnames)
            for (i in 1:l)
              results <- c(results, (paste(c(tnames[i], object@metaInfo[i]), collapse=" : ")))
            return(results)
          }
)

#-------------------------------------------------------------------------------#
# TCAMetaInfo::getPlateSize
# return Plate Size
#-------------------------------------------------------------------------------#
setGeneric("getPlateSize",
           function(object) {
             standardGeneric("getPlateSize")
           }
)

setMethod("getPlateSize",
          signature = signature("TCAMetaInfo"),
          definition = function(object) {
            return(object@metaInfo["PlateFormat"])
          }
)