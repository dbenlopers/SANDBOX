###################################################################################
# class definition for TCA genesData
# author : Nicodeme Paul originaly, modified by Arnaud KOPP
###################################################################################
setClass(
  Class = "TCAGeneBasedData",
  representation = representation(
    data = "list"
  ),
  prototype = prototype(
    data = NULL
  )
)


#----------------------------------------------------------------------------------
# TCAGeneBasedData::print function
#----------------------------------------------------------------------------------
setMethod("print",
          signature = signature("TCAGeneBasedData"),
          definition = function(x, ...) {
            cat("\n*** Class TCAGeneBasedData - Method print ***\n\n")
            print(x@data)	 
          }
)


#----------------------------------------------------------------------------------
# TCAGeneBasedData::show function
#----------------------------------------------------------------------------------
setMethod("show",
          signature = signature("TCAGeneBasedData"),
          definition = function(object) {
            cat("\n*** Class TCAGeneBasedData - Method show ***\n\n")
            str(object@data)
          }
)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getContent function
# return the content of the of TCAGeneBasedData object
#-------------------------------------------------------------------------------#
setMethod("getContent",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, repId, ...) {
            return(object@data)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getGeneBasedData function
# return the data related to TCAGeneBasedData object
#-------------------------------------------------------------------------------#
setGeneric("getGeneBasedData",
           function(object, ...) {
             standardGeneric("getGeneBasedData")
           }
)

setMethod("getGeneBasedData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object) {
            return(object@data)	
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getThresholdValues function
#-------------------------------------------------------------------------------#
setGeneric("getThresholdValues",
           function(object, refSamp, threshold, columns, ...) {
             standardGeneric("getThresholdValues")
           }
)


setMethod("getThresholdValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, threshold, columns, ...) {
            refId <- which(names(object@data)==refSamp)
            fHelper <- function(x, refTh) {
              u <- as.numeric(as.vector(x))
              return(quantile(u, refTh, na.rm=TRUE))
            }
            if (isTRUE(refId>0))
              return(apply(as.matrix(object@data[[refId]][, columns]), 2, fHelper, 1-threshold))
            stop(paste(c("Failed to identify ", refSamp), sep=""))  
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getMannWhitneyPvalues function
#-------------------------------------------------------------------------------#
setGeneric("getMannWhitneyPvalues",
           function(object, refSamp, posSamp, columns, ...) {
             standardGeneric("getMannWhitneyPvalues")
           }
)


setMethod("getMannWhitneyPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, posSamp, columns, ...) {
            refId <- which(names(object@data)==refSamp)
            posId <- which(names(object@data)==posSamp)
            mwPvalues <- c()
            if ((refId > 0) && (posId > 0)) {
              #print(c(refId, posId))
              for (col in columns) {
                c_pos <- as.numeric(as.vector(object@data[[posId]][, col]))
                c_neg <- as.numeric(as.vector(object@data[[refId]][, col]))
                mwPvalues <- c(mwPvalues, wilcox.test(c_pos, c_neg, alternative=c("greater"))$p.value)
              }
              names(mwPvalues) <- names(columns)
              return(mwPvalues)
            }
            stop(paste(c("Failed to identify ", refSamp, " or ", posSamp), sep=""))
          }
)

getMannWhitneyPvalues_c <- compiler::cmpfun(getMannWhitneyPvalues)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getEstimatedThresholdValues function
#-------------------------------------------------------------------------------#
setGeneric("getEstimatedThresholdValues",
           function(object, refSamp, posSamp, columns, ...) {
             standardGeneric("getEstimatedThresholdValues")
           }
)


setMethod("getEstimatedThresholdValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, posSamp, columns, ...) {
            refId <- which(names(object@data)==refSamp)
            posId <- which(names(object@data)==posSamp)
            thresholdValues <- c()
            if ((refId > 0) && (posId > 0)) {
              #print(c(refId, posId))
              for (col in columns) {
                c_pos <- as.numeric(as.vector(object@data[[posId]][, col]))
                c_neg <- as.numeric(as.vector(object@data[[refId]][, col]))
                d_pos <- density(c_pos)
                d_neg <- density(c_neg)
                x_pos_x_neg <- sort(setdiff(d_pos$x, d_neg$x))
                y_x_pos_x_neg <- d_pos$y[which(d_pos$x %in% x_pos_x_neg)] 
                x_neg_x_pos <- setdiff(d_neg$x, d_pos$x)
                y_x_neg_x_pos <- d_neg$y[which(d_neg$x %in% x_neg_x_pos)]
                x_neg_pos <- intersect(d_pos$x, d_neg$x)
                xx <- sort(unique(c(d_pos$x, d_neg$x)))
                yy_pos <- rep(-1.0, length(xx))
                yy_pos[which(xx %in% d_pos$x)] <- d_pos$y
                yy_pos[which(yy_pos==-1.0)] <- approx(d_pos$x, d_pos$y, xout=x_neg_x_pos, method="linear", 0.0, 0.0)$y
                yy_neg <- rep(-1.0, length(xx))
                yy_neg[which(xx %in% d_neg$x)] <- d_neg$y
                yy_neg[which(yy_neg==-1.0)] <- approx(d_neg$x, d_neg$y, xout=x_pos_x_neg, method="linear", 0.0, 0.0)$y
                maxDelta = max(yy_pos-yy_neg, na.rm=TRUE)
                maxId = max(which(abs(yy_pos-yy_neg-maxDelta) < 1e-10))
                if (maxId > 1) {
                  idx <- which(yy_pos-yy_neg < 0)
                  idx <- idx[which(idx < maxId)]
                  lidx <- length(idx)
                  tidx <- idx[lidx]
                  for (ix in lidx:1) {
                    c_v <- yy_pos[idx[ix]]-yy_neg[idx[ix]]
                    p_v <- yy_pos[idx[ix]-1]-yy_neg[idx[ix]-1]
                    pp_v <- yy_pos[idx[ix]-2]-yy_neg[idx[ix]-2]
                    ppp_v <- yy_pos[idx[ix]-3]-yy_neg[idx[ix]-3]
                    if ((ix > 1) && (c_v < 0) && (p_v < 0 ) && (pp_v < 0) && (ppp_v < 0)) {
                      tidx <- idx[ix]
                      break
                    }
                  }
                  cutoff <- xx[tidx+1]
                }
                else {
                  if (xx[maxId] <= 0)
                    cutoff <- 0.0
                  else
                    cutoff <- xx[maxId]
                }
                thresholdValues <- c(thresholdValues, cutoff)
              }
              #names(thresholdValues) <- names(columns)
              return(thresholdValues)
            }
            stop(paste(c("Failed to identify ", refSamp, " or ", posSamp), sep=""))
          }
)


getEstimatedThresholdValues_c <- compiler::cmpfun(getEstimatedThresholdValues)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotControls function
#-------------------------------------------------------------------------------#
setGeneric("plotControls",
           function(object, refSamp, posSamp, threshold, column, file, w, h, ...) {
             standardGeneric("plotControls")
           }
)


setMethod("plotControls",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, posSamp, threshold, column, file, w, h, ...) {
            refId <- which(names(object@data)==refSamp)
            posId <- which(names(object@data)==posSamp)
            if ((refId > 0) && (posId > 0)) {
              c_pos <- as.numeric(as.vector(object@data[[posId]][, column]))
              c_neg <- as.numeric(as.vector(object@data[[refId]][, column]))
              d_pos <- density(c_pos)
              d_neg <- density(c_neg)
              x_pos_x_neg <- sort(setdiff(d_pos$x, d_neg$x))
              y_x_pos_x_neg <- d_pos$y[which(d_pos$x %in% x_pos_x_neg)] 
              x_neg_x_pos <- setdiff(d_neg$x, d_pos$x)
              y_x_neg_x_pos <- d_neg$y[which(d_neg$x %in% x_neg_x_pos)]
              x_neg_pos <- intersect(d_pos$x, d_neg$x)
              xx <- sort(unique(c(d_pos$x, d_neg$x)))
              yy_pos <- rep(-1.0, length(xx))
              yy_pos[which(xx %in% d_pos$x)] <- d_pos$y
              yy_pos[which(yy_pos==-1.0)] <- approx(d_pos$x, d_pos$y, xout=x_neg_x_pos, method="linear", 0.0, 0.0)$y
              yy_neg <- rep(-1.0, length(xx))
              yy_neg[which(xx %in% d_neg$x)] <- d_neg$y
              yy_neg[which(yy_neg==-1.0)] <- approx(d_neg$x, d_neg$y, xout=x_pos_x_neg, method="linear", 0.0, 0.0)$y
              pdf(file, width=w, height=h)
              main <- "Postive and negative controls"
              xlab <- "Cell intensities"
              ylab <- "Likelihood values"
              col <- c("green", "red", "blue")
              lwd <- 2.0
              legtext <- c("Positive", "Negative", "Cutoff")
              plot(xx, yy_pos, type="l", col=col[1], main=main, xlab=xlab, ylab=ylab)
              lines(xx, yy_neg, type="l", col=col[2], xlab=xlab, ylab=ylab)
              #plot(xx, yy_pos, type="l", col=col[1], xlim=c(0, 10000), main=main, xlab=xlab, ylab=ylab)
              #lines(xx, yy_neg, type="l", col=col[2], xlim=c(0, 10000), xlab=xlab, ylab=ylab)
              abline(v=threshold, col=col[3])
              legend("topright", inset=0.05, legend=legtext, col=col, text.col = col, pch="-")
              dev.off()	
              return(0)
            }
            stop(paste(c("Failed to identify ", refSamp, " or ", posSamp), sep=""))  
          }
)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getThresholdValue function
#-------------------------------------------------------------------------------#
setGeneric("getThresholdValue",
           function(object, refSamp, threshold, targetColumn, ...) {
             standardGeneric("getThresholdValue")
           }
)


setMethod("getThresholdValue",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, threshold, targetColumn, ...) {
            refId <- which(names(object@data)==refSamp)
            if (isTRUE(refId>0))
              return(quantile(object@data[[refId]][, targetColumn], 1-threshold, na.rm=TRUE))
            stop(paste(c("Failed to identify ", refSamp), sep=""))  
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getCountAboveThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getCountAboveThreshold",
           function(object, threshold, column, ...) {
             standardGeneric("getCountAboveThreshold")
           }
)

setMethod("getCountAboveThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, threshold, column, ...) {
            counts = unlist(lapply(object@data, function(x) {
              val <- as.numeric(as.vector(x[,column]))
              val <- val[which(!is.na(val))] 
              return(sum(val>threshold, na.rm=T))
            }
            ))  
            return(counts)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getSummaries function
# returns summaries from the data
#-------------------------------------------------------------------------------#
setMethod("getSummaries",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, columns, ...) {
            summaries = lapply(getContent(object), function(x) apply(as.matrix(x[,columns]), 2, 
                                                                     function(col) c(len=length(which(!is.na(col))), 
                                                                                     sd= sd(col,na.rm=T),summary(as.numeric(col), na.rm=T))))
            return(new("TCASummaries", summaries=summaries))
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getChiqPvalues function
#-------------------------------------------------------------------------------#
setGeneric("getChisqPvalues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getChisqPvalues")
           }
)

setMethod("getChisqPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, ...) {
            refId <- which(names(object@data)==refSamp)
            c_pos <- as.numeric(as.vector(object@data[[refId]][, column]))
            p0 <- sum(c_pos > thresholdValue, na.rm=T)/length(which(!is.na(c_pos)))
            chiq_test <- function(x, p) {
              val <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T)
              n <- length(which(!is.na(x[,column])))
              q <- ((val - n * p)^2)/(n * p *(1 - p)) 
              return(pchisq(q, 1, lower.tail=FALSE))
            }
            chisqPvalues = unlist(lapply(object@data, chiq_test, p0)) 
            return(chisqPvalues)
          }
)




#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPercentAboveThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getPercentPvalues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getPercentPvalues")
           }
)

setMethod("getPercentPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, ...) {
            refId <- which(names(object@data)==refSamp)
            c_pos <- as.numeric(as.vector(object@data[[refId]][, column]))
            p0 <- sum(c_pos > thresholdValue, na.rm=T)/length(which(!is.na(c_pos)))
            binomial_test <- function(x) {
              val <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T)
              n <- length(which(!is.na(x[,column])))
              return(binom.test(val, n, p0, alternative=c("two.sided"))$p.value)
            }
            percentPvalues = unlist(lapply(object@data, binomial_test)) 
            return(percentPvalues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPercentAboveThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getPercentAboveThreshold",
           function(object, threshold, column, ...) {
             standardGeneric("getPercentAboveThreshold")
           }
)

setMethod("getPercentAboveThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, threshold, column, ...) {
            percents = unlist(lapply(object@data, function(x) 
              sum(as.numeric(as.vector(x[,column]))>threshold, na.rm=T)/length(which(!is.na(x[,column])))))
            return(percents)
          }
)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotPercentData function
#-------------------------------------------------------------------------------#
setGeneric("plotPercentData",
           function(object, sobject, threshold, columnId, columnName, ...) {
             standardGeneric("plotPercentData")
           }
)

setMethod("plotPercentData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, threshold, columnId, columnName, cnt, posSamp) {
            lengths <- getLengthSummary(sobject, columnId)
            mydata <- getPercentAboveThreshold(object, threshold, columnName)
            eps <- sqrt(mydata*(1-mydata)[names(lengths)]/lengths)
            dataUp <- 100*(mydata+eps[names(mydata)]) 
            dataDn <- 100*(mydata-eps[names(mydata)])
            mydata <- 100*mydata
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- paste("Percent of intensity values above Threshold for", columnName)
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.axis=1.1,ylab="% above threshold")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=mydata[posSamp], lty=4, col="darkred") 
            text(mydata[posSamp]+1, "Top control", col="darkred", cex=0.5) 
            #axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=2.0,tck=-0.012)
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(mydata)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)
            #mtext(as.numeric(cnt[names(mydata)]), at=MidPts, col="blue", side=1, line=-1,cex=1.5)
            #mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=1.1)
          }
)

# for test
getClean <- function(object, col, genes) {
  data <- c()
  for (gene in genes) {
    data <- c(data, object@data[[gene]][2:3])
  }
  return(data)
}



## get content in well for given column
getWellContent_unop <- function(object, Id, column) {
  refId <- which(names(object@data)==Id)
  data <- as.numeric(as.vector(object@data[[refId]][, column]))
  return(data)
}

getWellContent <- compiler::cmpfun(getWellContent_unop)


## get content of well list for given colum
getWellsContent_unop <- function(object, Wells, column) {
  data <- c()
  for (gene in Wells) {
    data <- c(data, as.numeric(as.vector(object@data[[gene]][, column])))
  }
  return(data)
}

getWellsContent <- compiler::cmpfun(getWellsContent_unop)


## Get MAD by well
getMadWell_unop <- function(object, id, Wells, column) {
  wells <- getWellsContent(object, Wells, column)
  well <- getWellContent(object, id, column)
  mad <- 1.4826 * median(abs(well - median(wells)))
  return(mad)
}

getMadWell <- compiler::cmpfun(getMadWell_unop)


## Get MAD for all Well
getMAD_unop <- function(object, Wells, column) {
  wells = getWellsContent(object, Wells, column)
  mad = unlist(lapply(object@data, function(x)
    1.4826 * median(abs(as.numeric(as.vector(x[,column])) -median(wells)))))
  return(mad)
}

getMAD <- compiler::cmpfun(getMAD_unop)



## Get mean for all Well
getMean_unop <- function(object, Wells, column) {
  #wells = getWellsContent(object, Wells, column)
  mean = unlist(lapply(object@data, function(x)
    ((mean(as.numeric(as.vector(x[,column])), na.rm=T)))))
  return(mean)
}

getMean <- compiler::cmpfun(getMean_unop) 


## Get median for all Well
getMedian_unop <- function(object, Wells, column) {
  #wells = getWellsContent(object, Wells, column)
  median = unlist(lapply(object@data, function(x)
    ((median(as.numeric(as.vector(x[,column])), na.rm=T)))))
  return(median)
}

getMedian <- compiler::cmpfun(getMedian_unop) 



## Get Z-score for all Well
getZScore_unop <- function(object, Wells, column) {
  wells = getWellsContent(object, Wells, column)
  zscore = unlist(lapply(object@data, function(x)
    ((mean(as.numeric(as.vector(x[,column])))) - mean(wells)) / sd(wells)))
  return(zscore)
}

getZScore <- compiler::cmpfun(getZScore_unop) 


## Get robust Z-score for all Well 
getRobustZScore_unop <- function(object, Wells, column) {
  wells = getWellsContent(object, Wells, column)
  zscore = unlist(lapply(object@data, function(x)
    ((median(as.numeric(as.vector(x[,column])))) - median(wells)) / (1.4826 * median(abs(wells - median(wells))))))
  return(zscore)
}

getRobustZScore <- compiler::cmpfun(getRobustZScore_unop)


## Get SSMD for all Well
getSSMD_unop <- function(object, Wells, column) {
  wells = getWellsContent(object, Wells, column)
  ssmd = unlist(lapply(object@data, function(x)
    ((mean(as.numeric(as.vector(x[,column])))) - mean(wells)) / (sqrt(2)*sd(wells))))
  return(ssmd)
}

getSSMD <- compiler::cmpfun(getSSMD_unop)


## Get robust SSMD for all Well
getRobustSSMD_unop <- function(object, Wells, column) {
  wells = getWellsContent(object, Wells, column)
  ssmd = unlist(lapply(object@data, function(x)
    ((median(as.numeric(as.vector(x[,column])))) - median(wells)) / (sqrt(2)*(1.4826 * median(abs(wells - median(wells)))))))
  return(ssmd)
}

getRobustSSMD <- compiler::cmpfun(getRobustSSMD_unop)


## Get control Normalization ( normalized percent inhibition) for all Well
getContNorm_unop <- function(object, Wells, neg, pos, column) {
  neg = getWellContent(object, neg, column)
  pos = getWellContent(object, pos, column)
  contnorm = unlist(lapply(object@data, function(x)
    ((mean(pos) - (mean(as.numeric(as.vector(x[, column]))))) / ( mean(pos) - mean(neg))*100)))
  return(contnorm)
}

getContNorm <- compiler::cmpfun(getContNorm_unop)


## Get Robust control Normalization ( normalized percent inhibition) for all Well
getRobustContNorm_unop <- function(object, Wells, neg, pos, column) {
  neg = getWellContent(object, neg, column)
  pos = getWellContent(object, pos, column)
  contnorm = unlist(lapply(object@data, function(x)
    ((median(pos) - (median(as.numeric(as.vector(x[, column]))))) / ( median(pos) - median(neg))*100)))
  return(contnorm)
}

getRobustContNorm <- compiler::cmpfun(getRobustContNorm_unop)



## Get fold change for all Well
getFoldChange_unop <- function(object, Wells, neg, column) {
  neg = getWellContent(object, neg, column)
  foldchange = unlist(lapply(object@data, function(x)
    ((mean(as.numeric(as.vector(x[,column])))) - mean(neg))))
  return(foldchange)
}

getFoldChange <- compiler::cmpfun(getFoldChange_unop)

## Get Robsut fold change for all Well
getFoldChangeR_unop <- function(object, Wells, neg, column) {
  neg = getWellContent(object, neg, column)
  foldchange = unlist(lapply(object@data, function(x)
    ((median(as.numeric(as.vector(x[,column])))) - median(neg))))
  return(foldchange)
}

getFoldChangeR <- compiler::cmpfun(getFoldChangeR_unop)

## get log median for all Well
getMedianLog_unop <- function(object, column) {
  mean = unlist(lapply(object@data, function(x)
    (median(as.numeric(as.vector(x[, column]))))))
  return(mean)
}

getMedianLog <- compiler::cmpfun(getMedianLog_unop)


## Compute the B-score 
getBScoreSSMDr_unop <- function(object, platesetup, column, size, neg) {
  
  
  ## function to tranform Well in B3 to 2,3
  WellToLoc=function(WellNo) {
    WellNo=as.character(WellNo)
    row.num=match(substr(WellNo, 1, 1), LETTERS)
    col.num=as.integer(substr(WellNo, 2, 3))
    loc=cbind(row.num, col.num)
    return(list(loc=loc))
  }
  
  
  gene_well <- as.matrix(getGenes(platesetup))
  bscore <- unlist(lapply(object@data, function(x) x=0))
  if (size == 96) {
    data <- matrix(-9999, nrow=8, ncol=12)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H"),         # row names 
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")) # column names
  } else {
    data <- matrix(-9999, nrow=16, ncol=24)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"),       
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24")) 
  } 
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      data_well <- getWellContent(object, gene, column)
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      data[row, col] <- data[row, col] + median(data_well) 
    }
  }
  data[data == -9999] <- NA
  median_polish <- medpolish(data, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  residual <- median_polish$residuals
  bscore_tmp = apply(residual, 1:2, function(x) (x/mad(residual, na.rm=T)))

  
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      bscore[gene] <- bscore_tmp[row, col]
    }
  } 
  
  ## search number of neg well for SSMDr
  platesetup.content <-getContent(platesetup)
  cnt <- table(platesetup.content)
  neg.cnt <- cnt[names(cnt)==neg]
  
  ## neg data for SSMDr calcul
  neg.data = bscore[neg]
  
  ##performed SSMDr on bscore normalized data
  ssmdr <- unlist(lapply(bscore, function(x) (x- median(bscore))/ (sqrt(2)*mad(bscore, na.rm=T))))
  #ssmdr <- unlist(lapply(bscore, function(x) ((x-neg.data)/(1.4826*neg.data*sqrt((neg.cnt-1)/neg.cnt-2.48)))))    1.4826 * median(abs(bscore - median(bscore)))
  return(ssmdr)
}

getBScoreSSMDr <- compiler::cmpfun(getBScoreSSMDr_unop)



## Compute the B-score median value
getBScoreMed_unop <- function(object, platesetup, column, size, neg) {
  
  
  ## function to tranform Well in B3 to 2,3
  WellToLoc=function(WellNo) {
    WellNo=as.character(WellNo)
    row.num=match(substr(WellNo, 1, 1), LETTERS)
    col.num=as.integer(substr(WellNo, 2, 3))
    loc=cbind(row.num, col.num)
    return(list(loc=loc))
  }
  
  
  gene_well <- as.matrix(getGenes(platesetup))
  bscore <- unlist(lapply(object@data, function(x) x=0))
  if (size == 96) {
    data <- matrix(-9999, nrow=8, ncol=12)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H"),         # row names 
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")) # column names
  } else {
    data <- matrix(-9999, nrow=16, ncol=24)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"),       
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24")) 
  } 
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      data_well <- getWellContent(object, gene, column)
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      data[row, col] <- data[row, col] + median(data_well) 
    }
  }
  data[data == -9999] <- NA
  median_polish <- medpolish(data, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  residual <- median_polish$residuals
  bscore_tmp = apply(residual, 1:2, function(x) (x/mad(residual, na.rm=T)))
  
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      bscore[gene] <- bscore_tmp[row, col]
    }
  } 
  
  ## search number of neg well for median
  platesetup.content <-getContent(platesetup)
  cnt <- table(platesetup.content)
  neg.cnt <- cnt[names(cnt)==neg]
  
  ## neg data for median calcul
  neg.data = bscore[neg]
  
  ##performed median on bscore normalized data
  med <- unlist(lapply(bscore, function(x) median(x, na.rm=T)))
  return(med)
}

getBScoreMed <- compiler::cmpfun(getBScoreMed_unop)




## Compute the B-score norm Fold Change
getBScoreFoldChange_unop <- function(object, platesetup, column, size, neg) {
  
  
  ## function to tranform Well in B3 to 2,3
  WellToLoc=function(WellNo) {
    WellNo=as.character(WellNo)
    row.num=match(substr(WellNo, 1, 1), LETTERS)
    col.num=as.integer(substr(WellNo, 2, 3))
    loc=cbind(row.num, col.num)
    return(list(loc=loc))
  }
  
  
  gene_well <- as.matrix(getGenes(platesetup))
  bscore <- unlist(lapply(object@data, function(x) x=0))
  if (size == 96) {
    data <- matrix(-9999, nrow=8, ncol=12)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H"),         # row names 
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")) # column names
  } else {
    data <- matrix(-9999, nrow=16, ncol=24)
    dimnames(data) = list( c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"),       
                           c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24")) 
  } 
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      data_well <- getWellContent(object, gene, column)
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      data[row, col] <- data[row, col] + median(data_well) 
    }
  }
  data[data == -9999] <- NA
  median_polish <- medpolish(data, eps = 1e-5, maxiter = 200, na.rm=T, trace.iter=F)
  residual <- median_polish$residuals
  bscore_tmp = apply(residual, 1:2, function(x) (x/mad(residual, na.rm=T)))
  
  for (i in 1:nrow(gene_well)) {
    puits <- gene_well[i,1]
    gene <- gene_well[i,2]
    if (gene == "") {
      next
    } else {
      pos <- WellToLoc(puits)
      row <- pos$loc[1,][1]
      col <- pos$loc[1,][2]
      bscore[gene] <- bscore_tmp[row, col]
    }
  } 
  
  ## search number of neg well for median
  platesetup.content <-getContent(platesetup)
  cnt <- table(platesetup.content)
  neg.cnt <- cnt[names(cnt)==neg]
  
  ## neg data for median calcul
  neg.data = bscore[neg]
  
  ##performed median on bscore normalized data
  FC <- unlist(lapply(bscore, function(x) median(x, na.rm=T)-median(neg.data, na.rm=T)))
  return(FC)
}

getBScoreFoldChange <- compiler::cmpfun(getBScoreFoldChange_unop)



## compute QC data for plate
getQC_unop <- function(object, plateName, sampName, posSamp, column, uGenes) {
  Plate <- c()
  SN <- c()
  Zprimefactor <- c()
  Zfactor <- c()
  SSMD <- c()
  QC.data <- data.frame()
  neg = getWellContent(object, sampName, column)
  pos = getWellContent(object, posSamp, column)
  wells = getWellsContent(object, uGenes, column)
  Plate <- c(Plate, plateName)
  
  s.n = ((mean(pos,na.rm=T)-mean(neg,na.rm=T))/(sd(neg,na.rm=T)))
  SN <- c(SN, s.n)
  
  zprimefactor = 1-((3*sd(pos,na.rm=T)+3*sd(neg,na.rm=T))/(abs(mean(pos,na.rm=T)-mean(neg,na.rm=T))))
  Zprimefactor <- c(Zprimefactor, zprimefactor)
  
  zfactor = 1-((3*sd(pos,na.rm=T)+3*sd(wells,na.rm=T))/(abs(mean(pos,na.rm=T)-mean(wells,na.rm=T))))
  Zfactor <- c(Zfactor, zfactor)
  
  ssmd = ((median(pos,na.rm=T)-median(neg,na.rm=T))/(1.4828*(sqrt(mad(pos,na.rm=T)^2+mad(neg,na.rm=T)^2))))
  SSMD <- c(SSMD, ssmd)
  
  QCdata <- c(Plate, SN, Zfactor, Zprimefactor, SSMD)
  return(QCdata)
}

getQCData <- compiler::cmpfun(getQC_unop)


#-----------------------------------------------------------------------------------------#
# TCAGeneBasedData::getControlsData function
#-----------------------------------------------------------------------------------------#
setGeneric("getControlsData",
           function(object, negSamp, posSamp, ...) {
             standardGeneric("getControlsData")
           }
)


setMethod("getControlsData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, negSamp, posSamp, ...) {
            dat.f <- getContent(object)
            pos.id <- which(names(dat.f)==posSamp)
            neg.id <- which(names(dat.f)==negSamp)
            dat <- rbind(dat.f[[neg.id]], dat.f[[pos.id]])
            pos.nrow <- nrow(dat.f[[pos.id]])
            neg.nrow <- nrow(dat.f[[neg.id]])
            dat$Response <- as.vector(c(rep(0, neg.nrow), rep(1, pos.nrow)))
            gene.id <- which(names(dat)=="GeneName")
            dat <- dat[, -gene.id]
            return(dat)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getProbData function
#-------------------------------------------------------------------------------#
setGeneric("getProbData",
           function(object, logisticModel, columns, ...) {
             standardGeneric("getProbData")
           }
)

setMethod("getProbData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, logisticModel, columns, ...) {
            dat.f <- getContent(object)
            nbOfGenes <- length(names(dat.f))
            for (i in 1:nbOfGenes) {
              for (col in columns) {
                xx <- predict(logisticModel[[col]],  newdata=dat.f[[i]], type="response")
                dat.f[[i]][, col] <- as.vector(xx)
              }
            } 
            return(dat.f)
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getFisherValues function
#-------------------------------------------------------------------------------#
setGeneric("getFisherValues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getFisherValues")
           }
)

setMethod("getFisherValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_cnt1 <- sum(ctr_data > thresholdValue, na.rm=T)
            ctr_cnt2 <- length(which(!is.na(ctr_data))) - ctr_cnt1
            # Calculate pvalues
            fisher_test <- function(x, side) {
              x_cnt1 <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T)
              x_cnt2 <- length(which(!is.na(x[,column]))) - x_cnt1
              return(fisher.test(matrix(c(x_cnt1, ctr_cnt1, x_cnt2, ctr_cnt2), nrow=2), alternative=c(side))$p.value)
            }
            fPvalues_greater = unlist(lapply(object@data, fisher_test, 'greater'))
            fPvalues_less = unlist(lapply(object@data, fisher_test, 'less'))
            fValues <- as.data.frame(cbind(fpval_greater=fPvalues_greater, fpval_less=fPvalues_less)) 
            return(fValues)
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getRelativeRiskValues function
#-------------------------------------------------------------------------------#
setGeneric("getRelativeRiskValues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getRelativeRiskValues")
           }
)

setMethod("getRelativeRiskValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, ...) {
            refNames <- names(object@data) 
            refId <- which(refNames==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_cnt1 <- sum(ctr_data > thresholdValue, na.rm=T) + 1
            ctr_len <- length(which(!is.na(ctr_data))) + 2
            ctr_cnt2 <- ctr_len - ctr_cnt1
            rr_val <- c()
            rr_pval_high <- c()
            rr_pval_low <- c()
            od_val <- c()
            od_pval_high <- c()
            od_pval_low <- c()
            for (i in 1:length(refNames)) {
              dat <- as.numeric(as.vector(object@data[[i]][, column]))
              dat <- dat[!is.na(dat)]
              x_cnt1 <- sum(dat > thresholdValue) + 1
              x_len <- length(dat) + 2
              x_cnt2 <- x_len - x_cnt1
              rr <- log(x_cnt1*ctr_len)-log(x_len*ctr_cnt1)
              od <- log(x_cnt1*ctr_cnt2)-log(ctr_cnt1*x_cnt2)
              rr_val <- c(rr_val, rr) 
              od_val <- c(od_val, od)
              std <-  sqrt((1/x_cnt1)-(1/x_len)+(1/ctr_cnt1)-(1/ctr_len))
              rr_pval_high <- c(rr_pval_high, pnorm(rr/std, lower.tail=FALSE))
              rr_pval_low <- c(rr_pval_low, pnorm(rr/std, lower.tail=TRUE))
              std <- sqrt((1/x_cnt1)+(1/x_cnt2)+(1/ctr_cnt1)+(1/ctr_cnt2))
              od_pval_high <- c(od_pval_high, pnorm(od/std, lower.tail=FALSE))
              od_pval_low <- c(od_pval_low, pnorm(od/std, lower.tail=TRUE))
            }
            rrValues <- as.data.frame(cbind(rr_val=rr_val,
                                            rr_pval_high=rr_pval_high,
                                            rr_pval_low=rr_pval_low,
                                            od_val=od_val,
                                            od_pval_high=od_pval_high,
                                            od_pval_low=od_pval_low))
            row.names(rrValues) <- refNames                                  
            return(rrValues)
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getProbValues function
#-------------------------------------------------------------------------------#
setGeneric("getProbValues",
           function(object, refSamp, column, ...) {
             standardGeneric("getProbValues")
           }
)

setMethod("getProbValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            prob_value <- function(x) {
              x_len <- length(which(!is.na(x[,column])))
              x_prob <- sum(as.numeric(as.vector(x[,column])), na.rm=T)
              return(x_prob/x_len)
            }
            probValues = unlist(lapply(object@data, prob_value)) 
            return(probValues)
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getRelativeProbValuesMM function
#-------------------------------------------------------------------------------#
setGeneric("getRelativeProbValuesMM",
           function(object, refSamp, column, ...) {
             standardGeneric("getRelativeProbValuesMM")
           }
)

setMethod("getRelativeProbValuesMM",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            refNames <- names(object@data) 
            refId <- which(refNames==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            ctr_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            ctr_alpha <- ctr_bar*((ctr_bar*(1-ctr_bar)/v)-1)
            ctr_beta <- (1-ctr_bar)*((ctr_bar*(1-ctr_bar)/v)-1)
            ctr_prob <- ctr_bar
            ctr_var <- ctr_beta/(ctr_len*ctr_alpha*(ctr_alpha+ctr_beta+1))
            ctr_var_od <- ((ctr_alpha+ctr_beta)^2)/(ctr_len*ctr_alpha*ctr_beta*(ctr_alpha+ctr_beta+1)) 
            rr_mm_val <- c()
            rr_mm_pval_high <- c()
            rr_mm_pval_low <- c()
            od_mm_val <- c()
            od_mm_pval_high <- c()
            od_mm_pval_low <- c()
            for (i in 1:length(refNames)) {
              x_data <- as.numeric(as.vector(object@data[[i]][, column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              x_alpha <- x_bar*((x_bar*(1-x_bar)/v)-1)
              x_beta <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              x_prob <- x_bar
              x_var <- x_beta/(x_len*x_alpha*(x_alpha+x_beta+1))
              rr <- log(x_prob)-log(ctr_prob)
              rr_mm_val <- c(rr_mm_val, rr)
              rr_mm_pval_high <- c(rr_mm_pval_high, pnorm(rr/sqrt(x_var+ctr_var), lower.tail=FALSE))
              rr_mm_pval_low <- c(rr_mm_pval_low, pnorm(rr/sqrt(x_var+ctr_var), lower.tail=TRUE))
              od <- log(x_prob*(1-ctr_prob)) - log(ctr_prob*(1-x_prob))
              od_mm_val <- c(od_mm_val, od)
              x_var_od <- ((x_alpha+x_beta)^2)/(x_len*x_alpha*x_beta*(x_alpha+x_beta+1))
              std <- sqrt(x_var_od+ctr_var_od)
              od_mm_pval_high <- c(od_mm_pval_high, pnorm(od/std, lower.tail=FALSE))
              od_mm_pval_low <- c(od_mm_pval_low, pnorm(od/std, lower.tail=TRUE))
            }
            
            prob_relativeValues <- as.data.frame(cbind(rr_mm_val=rr_mm_val,
                                                       rr_mm_pval_high=rr_mm_pval_high,
                                                       rr_mm_pval_low=rr_mm_pval_low,
                                                       od_mm_val=od_mm_val,
                                                       od_mm_pval_high=od_mm_pval_high,
                                                       od_mm_pval_low=od_mm_pval_low))
            row.names(prob_relativeValues) <- refNames
            return(prob_relativeValues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotProbRelativeRiskValues function
#-------------------------------------------------------------------------------#
setMethod("plotProbRelativeRiskValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, threshold, columnId, columnName, cnt, negSamp, posSamp, addtitle=1) {
            lengths <- getLengthSummary(sobject, columnId)
            lengths <- lengths[which(lengths > 0)]
            mean_data <- getMeanSummary(sobject, columnId)
            sd_data <- getSdSummary(sobject, columnId)
            refNames <- names(lengths)
            var_data <- ((lengths[refNames]-1)/lengths[refNames]) * (sd_data[refNames])^2 
            alpha_data <- mean_data[refNames]*((mean_data[refNames]*(1-mean_data[refNames])/var_data[refNames])-1)
            beta_data <- (1-mean_data[refNames])*((mean_data[refNames]*(1-mean_data[refNames])/var_data[refNames])-1)
            percent_data <- log(mean_data) - log(mean_data[negSamp])
            var_data <- beta_data[refNames]/(lengths[refNames]*alpha_data[refNames]*(alpha_data[refNames]+beta_data[refNames]+1))
            
            eps <- sqrt(var_data[refNames]+var_data[negSamp])      
            dataUp <- percent_data+eps[names(percent_data)] 
            dataDn <- percent_data-eps[names(percent_data)]
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste("Soft Relative Risk per well")
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            MidPts <- barplot(percent_data,main=tit,las=2,ylim=c(min(percent_data)-0.25,max(percent_data)+0.25),cex.names=0.9,cex.lab=1.5,ylab="log(Soft Relative Risk)")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=percent_data[negSamp], lty=4) 
            text(5, percent_data[negSamp]+0.05, "Negative control", cex=1.2) 
            abline(h=percent_data[posSamp], lty=4) 
            text(5, percent_data[posSamp]+0.05, "Positive control", cex=1.2) 
            #axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=2.0,tck=-0.012)
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(percent_data)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            #if (addtitle)
            #  mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)  	
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotCountRelativeRiskValues function
#-------------------------------------------------------------------------------#
setMethod("plotCountRelativeRiskValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, threshold, columnId, columnName, cnt, negSamp, posSamp, addtitle=1) {
            lengths <- getLengthSummary(sobject, columnId)
            lengths <- lengths[which(lengths > 0)]
            count_data <- getCountAboveThreshold(object, threshold, columnName)
            refNames <- names(lengths)
            percent_data <- (count_data[refNames]+0.5)/(lengths[refNames]+0.5)
            percent_data <- log(percent_data) - log(percent_data[negSamp])
            eps <- sqrt(1/count_data[refNames]-1/lengths[refNames]+1/count_data[negSamp]-1/lengths[negSamp])      
            dataUp <- percent_data+eps[names(percent_data)] 
            dataDn <- percent_data-eps[names(percent_data)]
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste("Relative Risk per well")
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            MidPts <- barplot(percent_data,main=tit,las=2,ylim=c(min(percent_data)-0.25,max(percent_data)+0.25),cex.names=0.9,cex.lab=1.5,ylab="log(Relative Risk)")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=percent_data[negSamp], lty=4) 
            text(5, percent_data[negSamp]+0.1, "Negative control", cex=1.2) 
            abline(h=percent_data[posSamp], lty=4) 
            text(5, percent_data[posSamp]+0.1, "Positive control", cex=1.2) 
            #axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=2.0,tck=-0.012)
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(percent_data)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            #if (addtitle)
            #  mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)  	
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotProbOfPositiveCells function
#-------------------------------------------------------------------------------#
setMethod("plotProbOfPositiveCells",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, threshold, columnId, columnName, cnt, negSamp, posSamp, addtitle=1) {
            lengths <- getLengthSummary(sobject, columnId)
            lengths <- lengths[which(lengths > 0)]
            mean_data <- getMeanSummary(sobject, columnId)
            sd_data <- getSdSummary(sobject, columnId)
            refNames <- names(lengths)
            var_data <- ((lengths[refNames]-1)/lengths[refNames]) * (sd_data[refNames])^2 
            alpha_data <- mean_data[refNames]*((mean_data[refNames]*(1-mean_data[refNames])/var_data[refNames])-1)
            beta_data <- (1-mean_data[refNames])*((mean_data[refNames]*(1-mean_data[refNames])/var_data[refNames])-1)
            eps <- sqrt((alpha_data[refNames]*beta_data[refNames])/(lengths[refNames]*((alpha_data[refNames]+beta_data[refNames])^2)*(alpha_data[refNames]+beta_data[refNames]+1))) 
            dataUp <- mean_data+eps[names(mean_data)] 
            dataDn <- mean_data-eps[names(mean_data)]
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste("Probalities of positive wells")
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            #MidPts <- barplot(mean_data,main=tit,las=2,ylim=c(0,1),cex.names=0.8,cex.lab=1.5,cex.main=0.9, ylab="Probabilities of positive wells")
            MidPts <- barplot(mean_data,main=tit,las=2,cex.names=0.8,cex.lab=1.5,cex.main=0.9, ylab="Probabilities of positive wells")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=mean_data[negSamp], lty=4) 
            text(5, mean_data[negSamp]+0.04, "Negative control", cex=1.2) 
            abline(h=mean_data[posSamp], lty=4) 
            text(5, mean_data[posSamp]+0.04, "Positive control", cex=1.2) 
            #axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=2.0,tck=-0.012)
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(mean_data)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            #if (addtitle)
            #  mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)  	
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotPercentOfPositiveCells function
#-------------------------------------------------------------------------------#
setMethod("plotPercentOfPositiveCells",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, threshold, columnId, columnName, cnt, negSamp, posSamp, addtitle=1) {
            lengths <- getLengthSummary(sobject, columnId)
            lengths <- lengths[which(lengths > 0)]
            mydata <- getPercentAboveThreshold(object, threshold, columnName)
            eps <- sqrt(mydata*(1-mydata)[names(lengths)]/lengths)
            dataUp <- 100*(mydata+eps[names(mydata)]) 
            dataDn <- 100*(mydata-eps[names(mydata)])
            mydata <- 100*mydata
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste("Percent of positive cells")
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.main=0.9, cex.lab=1.5,ylab="% of positive cells")
            MidPts <- barplot(mydata,main=tit,las=2,cex.names=0.8,cex.main=0.9, cex.lab=1.5,ylab="% of positive cells")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=mydata[negSamp], lty=4) 
            text(5, mydata[negSamp]+1, "Negative control", cex=1.2) 
            abline(h=mydata[posSamp], lty=4) 
            text(5, mydata[posSamp]+1, "Positive control", cex=1.2)
            #axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=2.0,tck=-0.012)
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(mydata)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            #if (addtitle)
            #  mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)  	
          }
)
