###################################################################################
# class definition for TCA summaries
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
###################################################################################
setClass(
  Class = "TCASummaries",
  representation = representation(
    summaries = "list"
  ),
  prototype = prototype(
    summaries = NULL
  )
)


#----------------------------------------------------------------------------------
# TCASummaries::print function
#----------------------------------------------------------------------------------
setMethod("print",
          signature = signature("TCASummaries"),
          definition = function(x, ...) {
            cat("\n*** Class TCASummmaries - Method print ***\n\n")
            print(x@summaries)	 
          }
)


#----------------------------------------------------------------------------------
# TCASummaries::show function
#----------------------------------------------------------------------------------
setMethod("show",
          signature = signature("TCASummaries"),
          definition = function(object) {
            cat("\n*** Class TCA Summaries - Method show ***\n\n")
            str(object@summaries)
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getContent function
# return the content of the TCASummaries object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("TCASummaries"),
          definition = function(object, repId, ...) {
            return(object@summaries)
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getSummaries function
#-------------------------------------------------------------------------------#
setGeneric("getSummaries",
           function(object, ...) {
             standardGeneric("getSummaries")
           }
)


setMethod("getSummaries",
          signature = signature("TCASummaries"),
          definition = function(object, ...) {
            return(object@summaries)
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::setSummaries function
#-------------------------------------------------------------------------------#
setGeneric("setSummaries",
           function(object, ...) {
             standardGeneric("setSummaries")
           }
)


setMethod("setSummaries",
          signature = signature("TCASummaries"),
          definition = function(object, summaries, ...) {
            object@summaries = summaries
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::is.empty function
#-------------------------------------------------------------------------------#
setGeneric("is.empty",
           function(object, ...) {
             standardGeneric("is.empty")
           }
)

setMethod("is.empty",
          signature = signature("TCASummaries"),
          definition = function(object, ...) {
            return(is.null(object@summaries))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getSummary() function
# return a vector of a summary item
#-------------------------------------------------------------------------------#
setGeneric("getSummary",
           function(object, summaryId="Mean", columnId, ...) {
             standardGeneric("getSummary")
           }
)

setMethod("getSummary",
          signature = signature("TCASummaries"),
          definition = function(object, summaryId, columnId, ...) {
            if (is.null(object@summaries)) 
              stop("No summary available")
            fHelper <- function(x) {
              if (is.matrix(x))
                u <- x[summaryId, columnId]
              else
                u <- x[[columnId]][summaryId]
              names(u) <- NULL
              return(u)
            }
            return(unlist(lapply(object@summaries, fHelper)))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getCV() function
# return a vector of CV values
#-------------------------------------------------------------------------------#
setGeneric("getCV",
           function(object, ...) {
             standardGeneric("getCV")
           }
)

setMethod("getCV",
          signature = signature("TCASummaries"),
          definition = function(object, columnId) {
            if (is.null(object@summaries)) 
              stop("No summary available")
            fHelper <- function(x) {
              if (is.matrix(x))
                u <- x["sd", columnId]/x["Mean", columnId]
              else
                u <- x[[columnId]]["sd"]/x[[columnId]]["Mean"]    
              names(u) <- NULL
              return(u)
            }
            return(unlist(lapply(object@summaries, fHelper)))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getLengthSummary
#-------------------------------------------------------------------------------#
setGeneric("getLengthSummary",
           function(object, columnId, ...) {
             standardGeneric("getLengthSummary")
           }
)

setMethod("getLengthSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "len", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getSdSummary
#-------------------------------------------------------------------------------#
setGeneric("getSdSummary",
           function(object, columnId, ...) {
             standardGeneric("getSdSummary")
           }
)

setMethod("getSdSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "sd", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getMinSummary
#-------------------------------------------------------------------------------#
setGeneric("getMinSummary",
           function(object, columnId, ...) {
             standardGeneric("getMinSummary")
           }
)

setMethod("getMinSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "Min.", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getFirstQuantileSummary
#-------------------------------------------------------------------------------#
setGeneric("getFirstQuantileSummary",
           function(object, columnId, ...) {
             standardGeneric("getFirstQuantileSummary")
           }
)

setMethod("getFirstQuantileSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "1st Qu.", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getMeadianSummary
#-------------------------------------------------------------------------------#
setGeneric("getMedianSummary",
           function(object, columnId, ...) {
             standardGeneric("getMedianSummary")
           }
)

setMethod("getMedianSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "Median", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getMeanSummary
#-------------------------------------------------------------------------------#
setGeneric("getMeanSummary",
           function(object, columnId, ...) {
             standardGeneric("getMeanSummary")
           }
)

setMethod("getMeanSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "Mean", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getThirdQuantileSummary
#-------------------------------------------------------------------------------#
setGeneric("getThirdQuantileSummary",
           function(object, columnId, ...) {
             standardGeneric("getThirdQuantileSummary")
           }
)

setMethod("getThirdQuantileSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "3rd Qu.", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::getMaxSummary
#-------------------------------------------------------------------------------#
setGeneric("getMaxSummary",
           function(object, columnId, ...) {
             standardGeneric("getMaxSummary")
           }
)

setMethod("getMaxSummary",
          signature = signature("TCASummaries"),
          definition = function(object, columnId, ...) {
            return(getSummary(object, "Max.", columnId))
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotSummary
#-------------------------------------------------------------------------------#
setGeneric("plotSummary", 
           function (object, ...) {
             standardGeneric("plotSummary")
           }
)

setMethod("plotSummary",
          signature = signature("TCASummaries"), 
          function (object, columnId, columnName, sampName, threshold, fname, wd, ht, addtitle=1, ...) {
            pdf(fname, width=wd, height=ht)
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- paste("Average intensity for combined replicates for", columnName)
            averages <- getMeanSummary(object, columnId)
            lengths <- getLengthSummary(object, columnId)
            sds <- getSdSummary(object, columnId)
            MidPts <- barplot(averages,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab=columnName)
            axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            erEndPoints <- cbind(averages+sds/sqrt(lengths), averages-sds/sqrt(lengths))
            segments(MidPts, erEndPoints[, 1], MidPts, erEndPoints[, 2],lty = "solid", lwd = 1)
            segments(MidPts - 0.2, erEndPoints,MidPts + 0.2, erEndPoints, lty = 1, lwd=1)
            mtext("error bars : standard error of the average (SEM) for all wells of corresponding sample",cex=0.8,line=0.3)
            
            # If plate setup is defined 
            
            #refVal=averages[which(names(averages)==sampName)]
            #abline(h=refVal, lty=4,lwd=2, col="blue")
            #text(max(MidPts)*1.01,refVal,"reference",col="blue",adj=c(1,1),pos=1,cex=0.8)
            #text(MidPts[length(MidPts)-1],refVal,"reference",col="blue",adj=c(1,1),pos=1,cex=0.8)
            abline(h=averages[sampName],lty=4,lwd=1, col="darkred")
            text(MidPts[which(names(averages)==sampName)],threshold,"Negative control",col="darkred",adj=1,pos=3,cex=0.75)
            #refSd <- sds[which(names(sds)==sampName)]
            #abline(h=refVal + 2*refSd,lty=4,lwd=1, col="green2")
            #text(max(MidPts)*1.01,refVal+2*refSd,"mean + 2SD",col="green2",adj=c(1,1),pos=3,cex=0.60)
            #abline(h=refVal - 2*refSd,lty=4,lwd=1, col="green2")
            #text(max(MidPts)*1.01,refVal-2*refSd,"mean - 2SD",col="green2",adj=c(1,1),pos=3,cex=0.60)
            dev.off()
          }
)



#-------------------------------------------------------------------------------#
# TCASummaries::plotSummary
#-------------------------------------------------------------------------------#
setGeneric("plotMultiThresholdSummary", 
           function (object, ...) {
             standardGeneric("plotMultiThresholdSummary")
           }
)

setMethod("plotMultiThresholdSummary",
          signature = signature("TCASummaries"), 
          function (object, columnId, columnName, sampName, fname, wd, ht, addtitle=1, ...) {
            pdf(fname, width=wd, height=ht)
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- paste("Average intensity for combined replicates for", columnName)
            averages <- getMeanSummary(object, columnId)
            lengths <- getLengthSummary(object, columnId)
            sds <- getSdSummary(object, columnId)
            MidPts <- barplot(averages,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab=columnName)
            axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            erEndPoints <- cbind(averages+sds/sqrt(lengths), averages-sds/sqrt(lengths))
            segments(MidPts, erEndPoints[, 1], MidPts, erEndPoints[, 2],lty = "solid", lwd = 1)
            segments(MidPts - 0.2, erEndPoints,MidPts + 0.2, erEndPoints, lty = 1, lwd=1)
            mtext("error bars : standard error of the average (SEM) for all wells of corresponding sample",cex=0.8,line=0.3)
            
            # If plate setup is defined 
            
            #refVal=averages[which(names(averages)==sampName)]
            #abline(h=refVal, lty=4,lwd=2, col="blue")
            #text(max(MidPts)*1.01,refVal,"reference",col="blue",adj=c(1,1),pos=1,cex=0.8)
            #text(MidPts[length(MidPts)-1],refVal,"reference",col="blue",adj=c(1,1),pos=1,cex=0.8)
            #abline(h=averages[sampName],lty=4,lwd=1, col="darkred")
            #text(MidPts[which(names(averages)==sampName)],threshold,"Negative control",col="darkred",adj=1,pos=3,cex=0.75)
            #refSd <- sds[which(names(sds)==sampName)]
            #abline(h=refVal + 2*refSd,lty=4,lwd=1, col="green2")
            #text(max(MidPts)*1.01,refVal+2*refSd,"mean + 2SD",col="green2",adj=c(1,1),pos=3,cex=0.60)
            #abline(h=refVal - 2*refSd,lty=4,lwd=1, col="green2")
            #text(max(MidPts)*1.01,refVal-2*refSd,"mean - 2SD",col="green2",adj=c(1,1),pos=3,cex=0.60)
            dev.off()
          }
)



#-------------------------------------------------------------------------------#
# TCASummaries::plotPlainSummary
#-------------------------------------------------------------------------------#
setGeneric("plotPlainSummary", 
           function (object, ...) {
             standardGeneric("plotPlainSummary")
           }
)

setMethod("plotPlainSummary",
          signature = signature("TCASummaries"), 
          function (object, columnId, columnName, sampName, threshold, fname, wd, ht, addtitle=1, ...) {
            pdf(fname, width=wd, height=ht)
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- paste("Average intensity values for", columnName)
            averages <- getMeanSummary(object, columnId)
            lengths <- getLengthSummary(object, columnId)
            sds <- getSdSummary(object, columnId)
            MidPts <- barplot(averages,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab=columnName)
            axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            erEndPoints <- cbind(averages+sds/sqrt(lengths), averages-sds/sqrt(lengths))
            segments(MidPts, erEndPoints[, 1], MidPts, erEndPoints[, 2],lty = "solid", lwd = 1)
            segments(MidPts - 0.2, erEndPoints,MidPts + 0.2, erEndPoints, lty = 1, lwd=1)
            mtext("error bars : standard error of the average (SEM) for all wells of corresponding sample",cex=0.8,line=0.3)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotCV
#-------------------------------------------------------------------------------#
setGeneric("plotCV",
           function(object, ...) {
             standardGeneric("plotCV")
           }
)


setMethod("plotCV",
          signature = signature("TCASummaries"),
          definition = function(object, plateSetup, sampName, column, colName, addtitle=1) {
            tit <- ""
            if (addtitle)
              tit <- paste(c("CV values distribution per Well for ", colName), collapse="")
            plateS <- getContent(plateSetup)
            plate <- matrix(, nrow(plateS), ncol(plateS))
            cvalues <- getCV(object, column)
            plate[,] <- cvalues[match(plateS, names(cvalues))]
            labels <- rep(NA_character_, length(plateS))
            sname <- sampName
            if (length(sname) > 2) 
              sname <- "CT"
            labels[which(as.vector(t(plateS))==sampName)] <- sname
            plotPlate(as.vector(t(plate)), ncol=ncol(plate), nrow=nrow(plate),
                      char=labels, cex.char=0.8, na.action="xout", main=tit, 	
                      col=brewer.pal(9, "YlOrBr"), add=FALSE);
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::barPlots
#-------------------------------------------------------------------------------#
setGeneric("barPlots",
           function(object, ...) {
             standardGeneric("barPlots")
           }
)		


setMethod("barPlots",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, threshold, fname, wd, ht, cnt, pSamp, addtitle=1) {
            #jpeg(file="percent.jpg", width=1728, height=728)
            pdf(fname, width=wd, height=ht)
            #layout(1:1)
            #plotSummary(object, columnId, columnName, sampName, threshold)
            plotPercentData(gbobject, object, threshold, columnId, columnName, cnt, sampName, pSamp, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotPercentOfPositiveCells
#-------------------------------------------------------------------------------#
setGeneric("plotPercentOfPositiveCells",
           function(object, ...) {
             standardGeneric("plotPercentOfPositiveCells")
           }
)		


setMethod("plotPercentOfPositiveCells",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, threshold, fname, wd, ht, cnt, pSamp, addtitle=1) {
            jpeg(file=fname, width=1728, height=728)
            #pdf(fname, width=wd, height=ht)
            plotPercentOfPositiveCells(gbobject, object, threshold, columnId, columnName, cnt, sampName, pSamp, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotProbOfPositiveCells
#-------------------------------------------------------------------------------#
setGeneric("plotProbOfPositiveCells",
           function(object, ...) {
             standardGeneric("plotProbOfPositiveCells")
           }
)		


setMethod("plotProbOfPositiveCells",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, threshold, fname, wd, ht, cnt, pSamp, addtitle=1) {
            jpeg(file=fname, width=1728, height=728)
            #pdf(fname, width=wd, height=ht)
            plotProbOfPositiveCells(gbobject, object, threshold, columnId, columnName, cnt, sampName, pSamp, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotCountRelativeRiskValues
#-------------------------------------------------------------------------------#
setGeneric("plotCountRelativeRiskValues",
           function(object, ...) {
             standardGeneric("plotCountRelativeRiskValues")
           }
)		


setMethod("plotCountRelativeRiskValues",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, threshold, fname, wd, ht, cnt, pSamp, addtitle=1) {
            jpeg(file=fname, width=1728, height=728)
            #pdf(fname, width=wd, height=ht)
            plotCountRelativeRiskValues(gbobject, object, threshold, columnId, columnName, cnt, sampName, pSamp, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotProbRelativeRiskValues
#-------------------------------------------------------------------------------#
setGeneric("plotProbRelativeRiskValues",
           function(object, ...) {
             standardGeneric("plotProbRelativeRiskValues")
           }
)		


setMethod("plotProbRelativeRiskValues",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, threshold, fname, wd, ht, cnt, pSamp, addtitle=1) {
            jpeg(file=fname, width=1728, height=728)
            #pdf(fname, width=wd, height=ht)
            plotProbRelativeRiskValues(gbobject, object, threshold, columnId, columnName, cnt, sampName, pSamp, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::barMultiThresholdPlots
#-------------------------------------------------------------------------------#
setGeneric("barMultiThresholdPlots",
           function(object, ...) {
             standardGeneric("barMultiThresholdPlots")
           }
)		


setMethod("barMultiThresholdPlots",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, thresholds, fname, wd, ht, cnt, pSamp, addtitle=1) {
            #jpeg(file="percent.jpg", width=1728, height=728)
            pdf(fname, width=wd, height=ht)
            #layout(1:1)
            #plotSummary(object, columnId, columnName, sampName, threshold)
            plotMultiThresholdPercentData(gbobject, object, thresholds, columnId, columnName, cnt, sampName, pSamp, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::barPlots
#-------------------------------------------------------------------------------#
setGeneric("barPaperPlots",
           function(object, ...) {
             standardGeneric("barPaperPlots")
           }
)		


setMethod("barPaperPlots",
          signature = signature("TCASummaries"),
          definition = function(object, gbobject, columnId, columnName, sampName, threshold, fname, wd, ht, cnt, pSamp, addtitle=1) {
            jpeg(file=fname, width=1024, height=700, res=150, quality=100)
            #pdf(fname, width=wd, height=ht)
            #layout(1:1)
            #plotSummary(object, columnId, columnName, sampName, threshold)
            plotPaperPercentData(gbobject, object, threshold, columnId, columnName, cnt, pSamp, addtitle)
            dev.off()
          }
)

#-------------------------------------------------------------------------------#
# TCASummaries::cvPlot
#-------------------------------------------------------------------------------#
setGeneric("cvPlot",
           function(object, ...) {
             standardGeneric("cvPlot")
           }
)


setMethod("cvPlot",
          signature = signature("TCASummaries"),
          definition = function(object, plateSetup, sampName, column, colName, fname, wd, ht, addtitle=1) {
            pdf(fname, width=wd, height=ht)
            plotCV(object, plateSetup, sampName, column, colName, addtitle)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::spatialSummaryPlot
#-------------------------------------------------------------------------------#
setGeneric("spatialSummaryPlot",
           function(object, ...) {
             standardGeneric("spatialSummaryPlot")
           }
)


setMethod("spatialSummaryPlot",
          signature = signature("TCASummaries"),
          definition = function(object, plateSetup, sampName, column, colName, fname, wd, ht, addtitle=1) {
            pdf(fname, width=wd, height=ht)
            plotSpatialSummary(object, plateSetup, sampName, column, colName, addtitle)
            dev.off()
          }
)  


#-----------------------------------------------------------------------------#
# TCASummaries::plotSpatialSpatialSummary
#------------------------------------------------------------------------------#
setGeneric("plotSpatialSummary", 
           function (object, ...) {
             standardGeneric("plotSpatialSummary")
           }
)

setMethod("plotSpatialSummary",
          signature = signature("TCASummaries"), 
          function (object, plateSetup, sampName, columnId, columnName, addtitle=1) {
            tit <- ""
            if (addtitle)
              tit <- paste(c("Summary values distribution per Well for ", columnName), collapse="")
            plateS <- getContent(plateSetup)
            plate <- matrix(, nrow(plateS), ncol(plateS))
            averages <- getMeanSummary(object, columnId)
            plate[,] <- averages[match(plateS, names(averages))]
            labels <- rep(NA_character_, length(plateS))
            sname <- sampName
            if (length(sname) > 2) 
              sname <- "CT"
            labels[which(as.vector(t(plateS))==sampName)] <- sname
            plotPlate(as.vector(t(plate)), ncol=ncol(plate), nrow=nrow(plate),
                      char=labels, cex.char=0.8, na.action="xout", main=tit, 	
                      col=brewer.pal(9, "YlOrBr"));
          }
)  


#-------------------------------------------------------------------------------#
# TCASummaries::plotRelativeRiskSpatialSummary
#-------------------------------------------------------------------------------#
setGeneric("plotRelativeRiskSpatialSummary",
           function(object, ...) {
             standardGeneric("plotRelativeRiskSpatialSummary")
           }
)


setMethod("plotRelativeRiskSpatialSummary",
          signature = signature("TCASummaries"),
          definition = function(object, gobject, plateSetup, sampName, column, colName, threshold, fname, wd, ht, addtitle=1) {
            #pdf(fname, width=wd, height=ht)
            jpeg(file=fname, width=1728, height=650)
            plotRelativeRiskSpatialSummaryHelper(object, gobject, plateSetup, sampName, column, colName, threshold, addtitle)
            dev.off()
          }
)  


#-----------------------------------------------------------------------------#
# TCASummaries::plotRelativeRiskSpatialSummaryHelper
#------------------------------------------------------------------------------#
setGeneric("plotRelativeRiskSpatialSummaryHelper", 
           function (object, ...) {
             standardGeneric("plotRelativeRiskSpatialSummaryHelper")
           }
)

setMethod("plotRelativeRiskSpatialSummaryHelper",
          signature = signature("TCASummaries"), 
          function (object, gobject, plateSetup, sampName, columnId, columnName, threshold, addtitle=1) {
            tit <- ""
            if (addtitle)
              tit <- paste(c("Relative Risk values per Well for ", columnName), collapse="")
            plateS <- getContent(plateSetup)
            plate <- matrix(, nrow(plateS), ncol(plateS))
            
            lengths <- getLengthSummary(object, columnId)
            lengths <- lengths[which(lengths > 0)]
            count_data <- getCountAboveThreshold(gobject, threshold, columnName)
            refNames <- names(lengths)
            percent_data <- (count_data[refNames]+0.5)/(lengths[refNames]+0.5)
            percent_data <- log(percent_data) - log(percent_data[negSamp])
            #percent_data <- percent_data - min(percent_data)	
            #print(percent_data)	
            plate[,] <- percent_data[match(plateS, names(percent_data))]
            labels <- rep(NA_character_, length(plateS))
            sname <- sampName
            if (length(sname) > 2) 
              sname <- "CT"
            labels[which(as.vector(t(plateS))==sampName)] <- sname
            plotPlate(as.vector(t(plate)), ncol=ncol(plate), nrow=nrow(plate),
                      char=labels, cex.char=0.8, na.action="xout", main=tit, cex.main=0.9,	
                      col=brewer.pal(9, "YlOrBr"));
          }
)  


#-------------------------------------------------------------------------------#
# TCASummaries::plotProbRelativeRiskSpatialSummary
#-------------------------------------------------------------------------------#
setGeneric("plotProbRelativeRiskSpatialSummary",
           function(object, ...) {
             standardGeneric("plotProbRelativeRiskSpatialSummary")
           }
)


setMethod("plotProbRelativeRiskSpatialSummary",
          signature = signature("TCASummaries"),
          definition = function(object, gobject, plateSetup, sampName, column, colName, threshold, fname, wd, ht, addtitle=1) {
            #pdf(fname, width=wd, height=ht)
            jpeg(file=fname, width=1728, height=650)
            plotProbRelativeRiskSpatialSummaryHelper(object, gobject, plateSetup, sampName, column, colName, threshold, addtitle)
            dev.off()
          }
)  


#-----------------------------------------------------------------------------#
# TCASummaries::plotProbRelativeRiskSpatialSummaryHelper
#------------------------------------------------------------------------------#
setGeneric("plotProbRelativeRiskSpatialSummaryHelper", 
           function (object, ...) {
             standardGeneric("plotProbRelativeRiskSpatialSummaryHelper")
           }
)

setMethod("plotProbRelativeRiskSpatialSummaryHelper",
          signature = signature("TCASummaries"), 
          function (object, gobject, plateSetup, sampName, columnId, columnName, threshold, addtitle=1) {
            tit <- ""
            if (addtitle)
              tit <- paste(c("Soft Relative Risk values per Well for ", columnName), collapse="")
            plateS <- getContent(plateSetup)
            plate <- matrix(, nrow(plateS), ncol(plateS))
            
            lengths <- getLengthSummary(object, columnId)
            lengths <- lengths[which(lengths > 0)]
            mean_data <- getMeanSummary(object, columnId)
            sd_data <- getSdSummary(object, columnId)
            refNames <- names(lengths)
            var_data <- ((lengths[refNames]-1)/lengths[refNames]) * (sd_data[refNames])^2 
            alpha_data <- mean_data[refNames]*((mean_data[refNames]*(1-mean_data[refNames])/var_data[refNames])-1)
            beta_data <- (1-mean_data[refNames])*((mean_data[refNames]*(1-mean_data[refNames])/var_data[refNames])-1)
            percent_data <- log(mean_data) - log(mean_data[negSamp])		
            #percent_data <- percent_data - min(percent_data)
            #print(percent_data)
            plate[,] <- percent_data[match(plateS, names(percent_data))]
            labels <- rep(NA_character_, length(plateS))
            sname <- sampName
            if (length(sname) > 2) 
              sname <- "CT"
            labels[which(as.vector(t(plateS))==sampName)] <- sname
            plotPlate(as.vector(t(plate)), ncol=ncol(plate), nrow=nrow(plate),
                      char=labels, cex.char=0.8, na.action="xout", main=tit, 	cex.main=0.9,
                      col=brewer.pal(9, "YlOrBr"));
          }
)  



#-----------------------------------------------------------------------------#
# TCASummaries::plotSpatialSpatialSummary
#------------------------------------------------------------------------------#
setGeneric("lengthPlot", 
           function (object, ...) {
             standardGeneric("lengthPlot")
           }
)

setMethod("lengthPlot",
          signature = signature("TCASummaries"),
          definition = function(object, plateSetup, sampName, columnId, columnName, fname, wd, ht, cnt) {
            pdf(fname, width=wd, height=ht)
            tit <- paste(c("Number of Cells distribution per Well \n (sum of replicate plates) for ", columnName, "\n"), collapse="")
            plateS <- getContent(plateSetup)
            plate <- matrix(, nrow(plateS), ncol(plateS))
            lengths <- getLengthSummary(object, columnId)
            lengths <- floor(lengths/cnt[names(lengths)])
            plate[,] <- lengths[match(plateS, names(lengths))]
            labels <- rep(NA_character_, length(plateS))
            sname <- sampName
            if (length(sname) > 2) 
              sname <- "CT"
            labels[which(as.vector(t(plateS))==sampName)] <- sname
            plotPlate(as.vector(t(plate)), ncol=ncol(plate), nrow=nrow(plate),
                      char=labels, cex.char=0.8, na.action="xout", main=tit, 	
                      col=brewer.pal(9, "YlOrBr"));	  
            dev.off()
          }
)     


#-------------------------------------------------------------------------------#
# TCASummaries::plotTransIdx function
#-------------------------------------------------------------------------------#
setGeneric("plotTransIdx",
           function(object, values, fname, wd, ht,...) {
             standardGeneric("plotTransIdx")
           }
)

setMethod("plotTransIdx",
          signature = signature("TCASummaries"), 
          function (object, values, column, fname, wd, ht, addtitle=1, ...) {
            pdf(fname, width=wd, height=ht)
            #jpeg(file="infectIdx.jpg", width=1728, height=728)
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste(c("Infection efficiency for ", column), sep="")
            #MidPts <- barplot(values,main=tit,las=2,cex.main=1.5, cex.lab=1.5, cex.names=1.2,cex.axis=1,ylab=column)
            #axis(1,labels=FALSE, at=MidPts,las=2, cex.axis=2.0,tck=-0.012)
            #print(values)
            MidPts <- barplot(values,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab=column)
            axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            abline(h=1, lty=4, col="darkred") 
            text(1.05, "Top control", col="darkred", cex=0.5)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotPercentOfControl function
#-------------------------------------------------------------------------------#
setGeneric("plotPercentOfControl",
           function(object, values, column, fname, wd, ht,...) {
             standardGeneric("plotPercentOfControl")
           }
)

setMethod("plotPercentOfControl",
          signature = signature("TCASummaries"), 
          function (object, values, column, fname, wd, ht, addtitle=1, ...) {
            pdf(fname, width=wd, height=ht)
            #jpeg(file="infectIdx.jpg", width=1728, height=728)
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste(c("Percent of control for ", column), sep="")
            #MidPts <- barplot(values,main=tit,las=2,cex.main=1.5, cex.lab=1.5, cex.names=1.2,cex.axis=1,ylab=column)
            #axis(1,labels=FALSE, at=MidPts,las=2, cex.axis=2.0,tck=-0.012)
            #print(values)
            MidPts <- barplot(values,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab=column)
            axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            abline(h=1, lty=4, col="darkred") 
            text(1.15, "Top control", col="darkred", cex=0.5)
            dev.off()
          }
)


#-------------------------------------------------------------------------------#
# TCASummaries::plotToxIndex function
#-------------------------------------------------------------------------------#
setGeneric("plotToxIndex",
           function(object, values, fname, wd, ht, addtitle, ...) {
             standardGeneric("plotToxIndex")
           }
)

setMethod("plotToxIndex",
          signature = signature("TCASummaries"), 
          function (object, values, column, fname, wd, ht, count, addtitle=1, ...) {
            pdf(fname, width=wd, height=ht)
            #jpeg(file="toxIdx.jpg", width=1728, height=728)
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste("Toxicity Index for ", column)
            #MidPts <- barplot(values,main=tit,las=2,cex.main=1.5, cex.lab=1.5, cex.names=1.2,cex.axis=1,ylab=column)
            #axis(1,labels=FALSE, at=MidPts,las=2, cex.axis=2.0,tck=-0.012)
            MidPts <- barplot(values,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab=column)
            axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            abline(h=1, lty=4, col="darkred") 
            text(0.95, "Top control", col="darkred", cex=0.5)
            dev.off()
          }
)

