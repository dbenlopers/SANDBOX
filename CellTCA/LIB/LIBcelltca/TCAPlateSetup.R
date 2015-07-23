
##################################################################################
# class definition for TCA PlateSetup
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
##################################################################################
setClass(
  Class = "TCAPlateSetup",
  representation = representation(
    plateSetup = "matrix"
  ),
  prototype = prototype(
    plateSetup = matrix(0)
  )
)


#----------------------------------------------------------------------------------
# TCAPlateSetup::print function
#----------------------------------------------------------------------------------
setMethod("print",
          signature = signature("TCAPlateSetup"),
          definition = function(x, ...) {
            cat("\n*** Class TCAPlateSetup - Method print ***\n\n")
            print(x@plateSetup)
            cat("\n")
          }
)


#----------------------------------------------------------------------------------
# TCAPlateSetup::show function
#----------------------------------------------------------------------------------
setMethod("show",
          signature = signature("TCAPlateSetup"),
          definition = function(object) {
            cat("\n*** Class TCAPlateSetup - Method show ***\n\n")
            print(object@plateSetup)
            cat("\n")
          }
)


#-------------------------------------------------------------------------------#
# TCAPlateSetup::getContent function
# return the content of the TCAPlateSetup object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("TCAPlateSetup"),
          definition = function(object, repId, ...) {
            return(object@plateSetup)
          }
)


#-------------------------------------------------------------------------------#
# TCAPlateSetup::getGenes function
# return a matrix[position, geneName]
# position is relative to the plate Setup, the position of a well "F1"
# geneName is the name of the gene assigned to that well
#-------------------------------------------------------------------------------#
setGeneric("getGenes",
           function(object, ...) {
             standardGeneric("getGenes")
           }
)

setMethod("getGenes",
          signature = signature("TCAPlateSetup"),
          definition = function(object) {
            pSetup = getContent(object)
            d <- nrow(pSetup)*ncol(pSetup)
            genes <- matrix(rep(NA, d), nrow=d, ncol=2)
            i <- 1
            for (row in rownames(pSetup)) {
              for (col in colnames(pSetup)) {
                genes[i,] <- c(paste(c(row, col), collapse=""), pSetup[row, col])
                i <- i+1
              }
            }
            # Remove NA genes before returning
            return(genes[which(!is.na(genes[,2])),])
          }
)


#-----------------------------------------------------------------------------#
# TCAPlateSetup::checkPlateSetup  return warnings in case of inconsistencies
#  each replicate should have the same plateSetup
#-----------------------------------------------------------------------------#
setGeneric("checkPlateSetup",
           function(object1, object2) {
             standardGeneric("checkPlateSetup")
           }
)


setMethod("checkPlateSetup",
          signature = signature("TCAPlateSetup"),
          definition = function(object1, object2) {
            mywarnings <- character(0)
            if (ncol(object1@plateSetup) != ncol(object2@plateSetup)) {
              mywarnings <- c(mywarnings, "The plate setups are different")
              return(mywarnings)
            }
            if (nrow(object1@plateSetup) != nrow(object2@plateSetup)) {
              mywarnings <- c(mywarnings, "The plate setups are different")
              return(mywarnings)
            }
            for (i in 1:nrow(object1@plateSetup)) {
              for (j in 1:ncol(object1@plateSetup)) {
                if (is.na(object1@plateSetup[i, j])) {
                  if (! is.na(object2@plateSetup[i, j])) {
                    mywarnings <- c(mywarnings, paste(c("Plate setups disagree on ", LETTERS[i], j), collapse=""))
                    return(mywarnings)
                  }
                }
                else {
                  if (is.na(object2@plateSetup[i, j])) {
                    mywarnings <- c(mywarnings, paste(c("Plate setups disagree on ", LETTERS[i], j), collapse=""))
                    return(mywarnings)
                  }	 
                  else if (object1@plateSetup[i, j] != object2@plateSetup[i, j]) {
                    mywarnings <- c(mywarnings, paste(c("Plate setups disagree on ", LETTERS[i], j), collapse=""))
                    return(mywarnings)
                  }
                }
              }
            }
            return(mywarnings)
          }
)



#-----------------------------------------------------------------------------#
# TCAPlateSetup::getPlateSetupAsTable
#-----------------------------------------------------------------------------#
setGeneric("getPlateSetupAsTable",
           function(object) {
             standardGeneric("getPlateSetupAsTable")
           }
)


setMethod("getPlateSetupAsTable",
          signature = signature("TCAPlateSetup"),
          definition = function(object) {
            fHelper <- function(x) {
              y <- paste(x, collapse=" ")
              return(y)
            }
            tmp <- apply(object@plateSetup, 1 , fHelper)
            return(paste(tmp, collapse="\n"))
          }
)


#-------------------------------------------------------------------------------#
# TCAPlateSetup::getFormattedPlateSetup
#-------------------------------------------------------------------------------#
setGeneric("getFormattedPlateSetup",
           function(object, ...) {
             standardGeneric("getFormattedPlateSetup")
           }
)


setMethod("getFormattedPlateSetup",
          signature = signature("TCAPlateSetup"),
          definition = function(object) {
            dat <- getContent(object)
            di_m <- dim(dat)
            n_r <- di_m[1]
            n_c <- di_m[2]
            cols <- paste(rep('l', n_c+1), collapse="")
            preamble <- paste(c("\\begin{table}[!hb]\n\\scriptsize\n\\begin{tabular}{", cols, "}\n"), collapse="")
            l_0 <- paste(c(" ", 1:n_c), collapse=" & ")
            res <- c(l_0)
            for (i in 1:n_r) {
              res <- c(res, paste(c(LETTERS[i], gsub("_", "\\\\_", dat[i,])), collapse=" & "))
            }
            postamble <- "\\end{tabular}\n \\caption{Plate Setup with gene identifiers} \\end{table}\n"
            return(paste(c(preamble, paste(c(res, postamble), collapse=" \\\\ \\\\ \n")), collapse=""))
          }
)


#-------------------------------------------------------------------------------#
# TCAPlateSetup::getNumberOfReplicatesPerGene
#-------------------------------------------------------------------------------#
setGeneric("getNumberOfReplicatesPerGene",
           function(object, ...) {
             standardGeneric("getNumberOfReplicatesPerGene")
           }
)

setMethod("getNumberOfReplicatesPerGene",
          signature = signature("TCAPlateSetup"),
          definition = function(object) {
            return(table(object@plateSetup))
          }
)

