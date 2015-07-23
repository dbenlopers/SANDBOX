
###################################################################################
# class definition for TCA DataInfo
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
###################################################################################
setClass(
  Class = "TCADataInfo",
  representation = representation(
    info = "character"
  ),
  prototype = prototype(
    info = character(0)
  )
)



#--------------------------------------------------------------------------------
# TCADataInfo::print function
#--------------------------------------------------------------------------------
setMethod("print", 
          signature = signature("TCADataInfo"),
          definition = function(x, ...) {
            cat("\n***	Class TCADataInfo - Method print ****\n\n")
            print(x@info)
            cat("\n")
          }
)


#---------------------------------------------------------------------------------
# TCADataInfo::show function
#---------------------------------------------------------------------------------
setMethod("show",
          signature = signature("TCADataInfo"),
          definition = function(object) {
            cat("\n***  Class TCADataInfo - Method show ****\n\n")
            tnames <- names(object@info)
            l <- length(tnames)
            for (i in 1:l)
              print(paste(c(tnames[i], object@info[i]), collapse=" : "))
            cat("\n")
          }
)


#-------------------------------------------------------------------------------#
# TCADataInfo::getContent function
# return the Data Info content of the TCADataInfo object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("TCADataInfo"),
          definition = function(object, repId, ...) {
            return(object@info)
          }
)


#-------------------------------------------------------------------------------#
# TCADataInfo::getFileName function
#-------------------------------------------------------------------------------#
setGeneric("getFileName",
           function(object) {
             standardGeneric("getFileName")
           }
)


setMethod("getFileName",
          signature = signature("TCADataInfo"),
          definition = function(object) {
            fname <- rev(unlist(strsplit(object@info["file"], "/")))[1]
            return(fname)
          }
)

