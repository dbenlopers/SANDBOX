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
                #print(c_pos)
                c_neg <- as.numeric(as.vector(object@data[[refId]][, col]))
                d_pos <- density(c_pos, na.rm=T, n=2048)
                d_neg <- density(c_neg, na.rm=T, n=2048)
                x_pos_x_neg <- sort(setdiff(d_pos$x, d_neg$x))
                y_x_pos_x_neg <- d_pos$y[which(d_pos$x %in% x_pos_x_neg)] 
                x_neg_x_pos <- setdiff(d_neg$x, d_pos$x)
                y_x_neg_x_pos <- d_neg$y[which(d_neg$x %in% x_neg_x_pos)]
                x_neg_pos <- intersect(d_pos$x, d_neg$x)
                xx <- sort(unique(c(d_pos$x, d_neg$x)))
                yy_pos <- rep(-1.0, length(xx))
                yy_pos[which(xx %in% d_pos$x)] <- d_pos$y
                yy_pos[which(yy_pos==-1.0)] <- approx(d_pos$x, d_pos$y, xout=x_neg_x_pos, method="linear", yleft=0.0, yright=0.0)$y
                yy_neg <- rep(-1.0, length(xx))
                yy_neg[which(xx %in% d_neg$x)] <- d_neg$y
                yy_neg[which(yy_neg==-1.0)] <- approx(d_neg$x, d_neg$y, xout=x_pos_x_neg, method="linear", yleft=0.0, yright=0.0)$y
                maxDelta = max(yy_pos-yy_neg, na.rm=TRUE)
                maxId = max(which(abs(yy_pos-yy_neg-maxDelta) < 1e-10))
                #print(maxDelta)
                #print(maxId)
                if (maxId > 1) {
                  idx <- which(yy_pos-yy_neg < 0)
                  idx <- idx[which(idx < maxId)]
                  lidx <- length(idx)
                  if (lidx) {
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
                    cutoff <- quantile(c_pos, 0.05)
                  }
                }
                else {
                  if (xx[maxId] <= 0)
                    cutoff <- quantile(c_pos, 0.05)
                  else
                    cutoff <- xx[maxId]
                }
                thresholdValues <- c(thresholdValues, cutoff)
              }
              names(thresholdValues) <- names(columns)
              return(thresholdValues)
            }
            stop(paste(c("Failed to identify ", refSamp, " or ", posSamp), sep=""))
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPlotDistributionTest function
#-------------------------------------------------------------------------------#
setGeneric("getPlotDistributionTest",
           function(object, refSamp, columns, Gene, ...) {
             standartGeneric("getPlotDistributionTest")
           }
)

setMethod("getPlotDistributionTest",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, columns, Gene, ...) {
            refId <- which(names(object@data)==refSamp)
            posId <- which(names(object@data)==Gene)
            c <- 0
            for (col in columns) {
              ## Cell classe par gene
              c_pos <- as.numeric(as.vector(object@data[[posId]][, col]))
              c_neg <- as.numeric(as.vector(object@data[[refId]][, col]))
              
              ## Densité par gene
              d_pos <- density(c_pos, na.rm=T, n=2048)
              d_neg <- density(c_neg, na.rm=T, n=2048)
              
              ## Calculates the (nonsymmetric) set difference of subsets of a probability space. 
              x_pos_x_neg <- sort(setdiff(d_pos$x, d_neg$x)) 
              y_x_pos_x_neg <- d_pos$y[which(d_pos$x %in% x_pos_x_neg)] 
              x_neg_x_pos <- setdiff(d_neg$x, d_pos$x) 
              y_x_neg_x_pos <- d_neg$y[which(d_neg$x %in% x_neg_x_pos)]  
              x_neg_pos <- intersect(d_pos$x, d_neg$x) 
              
              xx <- sort(unique(c(d_pos$x, d_neg$x)))
              yy_pos <- rep(-1.0, length(xx))
              yy_pos[which(xx %in% d_pos$x)] <- d_pos$y
              yy_pos[which(yy_pos==-1.0)] <- approx(d_pos$x, d_pos$y, xout=x_neg_x_pos, method="linear", yleft=0.0, yright=0.0)$y
              yy_neg <- rep(-1.0, length(xx))
              yy_neg[which(xx %in% d_neg$x)] <- d_neg$y
              yy_neg[which(yy_neg==-1.0)] <- approx(d_neg$x, d_neg$y, xout=x_pos_x_neg, method="linear", yleft=0.0, yright=0.0)$y 
              
              plot(yy_pos, type='l', col=2, main=Gene)
              lines(yy_neg, col=3)
              
            }  
          }         
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getEstimatedThresholdValues function
#-------------------------------------------------------------------------------#
setGeneric("getEstimatedMultiThresholdValues",
           function(object, refSamp, uGenes, columns, ...) {
             standardGeneric("getEstimatedMultiThresholdValues")
           }
)


setMethod("getEstimatedMultiThresholdValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, uGenes, columns, ...) {
            #uGenes <- uGenes[-which(uGenes==refSamp)]
            refId <- which(names(object@data)==refSamp)
            thresholdValues <- matrix(,length(uGenes), length(columns))
            g <- 0
            for (posSamp in uGenes) {
              g <- g + 1
              posId <- which(names(object@data)==posSamp)
              if ((refId < 0) | (posId < 0)) {
                next
              }
              #print(c(refId, posId))
              c <- 0
              for (col in columns) {
                c <- c + 1
                ## Cell classe par gene
                c_pos <- as.numeric(as.vector(object@data[[posId]][, col]))
                c_neg <- as.numeric(as.vector(object@data[[refId]][, col]))
                ## Densité par gene
                d_pos <- density(c_pos, na.rm=T, n=2048)
                d_neg <- density(c_neg, na.rm=T, n=2048)
                
                ## Calculates the (nonsymmetric) set difference of subsets of a probability space. 
                x_pos_x_neg <- sort(setdiff(d_pos$x, d_neg$x)) 
                y_x_pos_x_neg <- d_pos$y[which(d_pos$x %in% x_pos_x_neg)] 
                x_neg_x_pos <- setdiff(d_neg$x, d_pos$x) 
                y_x_neg_x_pos <- d_neg$y[which(d_neg$x %in% x_neg_x_pos)]  
                x_neg_pos <- intersect(d_pos$x, d_neg$x) 
                
                xx <- sort(unique(c(d_pos$x, d_neg$x)))
                yy_pos <- rep(-1.0, length(xx))
                yy_pos[which(xx %in% d_pos$x)] <- d_pos$y
                yy_pos[which(yy_pos==-1.0)] <- approx(d_pos$x, d_pos$y, xout=x_neg_x_pos, method="linear", yleft=0.0, yright=0.0)$y
                yy_neg <- rep(-1.0, length(xx))
                yy_neg[which(xx %in% d_neg$x)] <- d_neg$y
                yy_neg[which(yy_neg==-1.0)] <- approx(d_neg$x, d_neg$y, xout=x_pos_x_neg, method="linear", yleft=0.0, yright=0.0)$y 
                
                
                ## max_XX equivaut à la densite max et max_XX_Id equivaut a l'intensite de la densite max
                max_Pos = max(yy_pos)
                max_Pos_Id = max(which(abs(yy_pos-max_Pos) < 1e-10))
                max_Neg = max(yy_neg)
                max_Neg_Id = max(which(abs(yy_neg-max_Neg) < 1e-10))
                if ((max_Neg_Id >= max_Pos_Id) | (max_Pos_Id < 1)) {
                  #print(c("Failed Up1", posSamp, max_Neg_Id, max_Neg, max_Pos_Id, max_Pos)) 
                  next  
                }
                
                maxId <- max_Pos_Id
                minId <- max_Neg_Id
                idx <- which(yy_pos-yy_neg < 0)
                idx <- idx[which((idx < maxId) & (idx > minId))]
                lidx <- length(idx)
                if (lidx) {
                  if (yy_pos[idx[lidx]+1]-yy_neg[idx[lidx]+1] < 0) {
                    #print(c("Failed Down1", posSamp, max_Neg_Id, max_Neg, max_Pos_Id, max_Pos))
                    next
                  }
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
                  #print(c("Success", posSamp, max_Neg_Id, max_Neg, max_Pos_Id, max_Pos))
                  thresholdValues[g,c] <- xx[tidx+1]
                }
                else {
                  #print(c("Failed Down2", posSamp, max_Neg_Id, max_Neg, max_Pos_Id, max_Pos))
                }
              }
            }
            thresholdValues <- as.data.frame(thresholdValues)
            names(thresholdValues) <- columns
            rownames(thresholdValues) <- uGenes
            #print(thresholdValues)
            return(thresholdValues)
          }
)

getEstimatedMultiThresholdValues_c <- compiler::cmpfun(getEstimatedMultiThresholdValues)

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
          definition = function(object, refSamp, posSamp, threshold, column, file, w, h, addtitle=1, ...) {
            if (is.na(threshold))
              return(0)
            refId <- which(names(object@data)==refSamp)
            posId <- which(names(object@data)==posSamp)
            if ((refId > 0) && (posId > 0)) {
              c_pos <- as.numeric(as.vector(object@data[[posId]][, column]))
              c_neg <- as.numeric(as.vector(object@data[[refId]][, column]))
              d_pos <- density(c_pos, na.rm=T)
              d_neg <- density(c_neg, na.rm=T)
              x_pos_x_neg <- sort(setdiff(d_pos$x, d_neg$x))
              y_x_pos_x_neg <- d_pos$y[which(d_pos$x %in% x_pos_x_neg)] 
              x_neg_x_pos <- setdiff(d_neg$x, d_pos$x)
              y_x_neg_x_pos <- d_neg$y[which(d_neg$x %in% x_neg_x_pos)]
              x_neg_pos <- intersect(d_pos$x, d_neg$x)
              xx <- sort(unique(c(d_pos$x, d_neg$x)))
              yy_pos <- rep(-1.0, length(xx))
              yy_pos[which(xx %in% d_pos$x)] <- d_pos$y
              yy_pos[which(yy_pos==-1.0)] <- approx(d_pos$x, d_pos$y, xout=x_neg_x_pos, method="linear", yleft=0.0, yright=0.0)$y
              yy_neg <- rep(-1.0, length(xx))
              yy_neg[which(xx %in% d_neg$x)] <- d_neg$y
              yy_neg[which(yy_neg==-1.0)] <- approx(d_neg$x, d_neg$y, xout=x_pos_x_neg, method="linear", yleft=0.0, yright=0.0)$y
              pdf(file, width=w, height=h)
              main <- ""
              if (addtitle)
                main <- paste("Postive and negative controls ", posSamp, sep="")
              xlab <- "Cell intensities"
              ylab <- "Likelihood values"
              col <- c("green", "red", "blue")
              lwd <- 2.0
              legtext <- c("Positive", "Negative", "Cutoff")
              xmax <- max(xx)
              if (xmax >= 1000)
                xmax <- quantile(xx, 0.9)
              plot(xx, yy_pos, type="l", col=col[1], xlim=c(0, xmax), main=main, xlab=xlab, ylab=ylab)
              lines(xx, yy_neg, type="l", col=col[2], xlim=c(0, xmax), xlab=xlab, ylab=ylab)
              abline(v=threshold, col=col[3])
              text(threshold, 0.001, paste("Threshold = ", round(threshold, digits=3), sep=""), pos=4, col=col[3], cex=0.8) 
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
# TCAGeneBasedData::getPCASummaries function
#-------------------------------------------------------------------------------#
setGeneric("getPCAGeneBasedData",
           function(object, pcaData, nC, columns, center, ...) {
             standardGeneric("getPCAGeneBasedData")
           }
)

setMethod("getPCAGeneBasedData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, pcaData, nC, columns, center, ...) {
            dat.f <- getContent(object)
            out.list = list()
            nbOfGenes <- length(names(dat.f))
            for (i in 1:nbOfGenes) {
              dd <- dat.f[[i]][, -ncol(dat.f[[i]])]
              dd <- dd[, columns]
              ## Check for constant columns
              ##for (col in columns) {
              ##  if (sd(dd[, col], na.rm=T)==0) {
              ##    dd[, col]  <- dd[, col] + rnorm(nrow(dd), mean=0, sd=0.0001)
              ##  } 
              ##}
              # DS diagonal matrix of the inverse standard deviations
              # Y centered data matrix 
              # Z standardized data matrix
              # Z = Y %*% DS
              # Id identity matrix
              # In vector with all the components equal to 1
              # Dn diagonal matrix with all components equal 1/n
              # Y = (Id - In %*% t(In) %*% Dn) %*% X
              n <- nrow(dd)
              ##xn <- rep(1/n, n)
              ##Dn <- diag(xn)
              In <- rep(1, n)
              ##Id <- diag(n)
              ##Y <- (Id - (In %*% t(In) %*% Dn)) %*% as.matrix(dd)
              ##s <- apply(dd, 2, function(x) sd(x))
              ##s <- sqrt((n-1)/n) * s
              ##s <- 1/s
              ##Ds <- diag(s)
              ##Z <- Y %*% Ds
              # Calculate new coordinates on pricipal components
              # W new coord in principal component basis
              # Ds diagonal matrix with the inverse of principal component inertia
              s <- 1/sqrt(pcaData$eig[,1])
              Ds <- diag(s)
              Z <- as.matrix(dd) - (In %*% t(center)) 
              W = Z %*% as.matrix(pcaData$var$coord) %*% Ds   
              W = as.data.frame(W[, nC])
              names(W) <- paste("Dim.", nC, sep="")  
              W$GeneName <- rep(names(dat.f)[i], nrow(W))
              out.list[[i]] <- W
            } 
            names(out.list) <- names(dat.f)
            return(out.list)
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
# TCAGeneBasedData::getNormalPvalues function
#-------------------------------------------------------------------------------#
setGeneric("getNormalPvalues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getNormalPvalues")
           }
)

setMethod("getNormalPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, ...) {
            refId <- which(names(object@data)==refSamp)
            x_pos <- as.numeric(as.vector(object@data[[refId]][, column]))
            x_pos_cnt <- sum(x_pos > thresholdValue, na.rm=T)
            x_pos_length <- length(which(!is.na(x_pos)))
            p_pos <- x_pos_cnt / x_pos_length
            normal_test <- function(x) {
              x_cnt <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T)
              x_length <- length(which(!is.na(x)))
              p_x <- x_cnt / x_length
              p_tot <- (x_pos_cnt+x_cnt)/(x_pos_length+x_length)
              val <- abs(p_pos-p_x)/(sqrt(p_tot*(1-p_tot))*((1/x_pos_length)+(1/x_length)))
              return(2*(1-pnorm(val, mean=0, sd=1)))
            }
            normalPvalues = unlist(lapply(object@data, normal_test)) 
            return(normalPvalues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPercentPvalues function
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
# TCAGeneBasedData::getFisherPvalues function
#-------------------------------------------------------------------------------#
setGeneric("getFisherPvalues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getFisherPvalues")
           }
)

setMethod("getFisherPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, side) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_cnt1 <- sum(ctr_data > thresholdValue, na.rm=T)
            ctr_cnt2 <- length(which(!is.na(ctr_data))) - ctr_cnt1
            fisher_test <- function(x) {
              x_cnt1 <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T)
              x_cnt2 <- length(which(!is.na(x[,column]))) - x_cnt1
              return(fisher.test(matrix(c(x_cnt1, ctr_cnt1, x_cnt2, ctr_cnt2), nrow=2), alternative=c(side))$p.value)
            }
            fPvalues = unlist(lapply(object@data, fisher_test)) 
            return(fPvalues)
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
# TCAGeneBasedData::getRelativeRiskPvalues function
#-------------------------------------------------------------------------------#
setGeneric("getRelativeRiskPvalues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getRelativeRiskPvalues")
           }
)

setMethod("getRelativeRiskPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, side=FALSE, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_cnt1 <- sum(ctr_data > thresholdValue, na.rm=T) + 0.5
            ctr_len1 <- length(which(!is.na(ctr_data))) + 0.5
            relative_risk_pvalue <- function(x) {
              x_cnt1 <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T) + 0.5
              x_len1 <- length(which(!is.na(x[,column])))  + 0.5
              s <-  sqrt(1/x_cnt1-1/x_len1+1/ctr_cnt1-1/ctr_len1)
              return(pnorm((log(x_cnt1*ctr_len1)-log(x_len1*ctr_cnt1))/s, lower.tail=side))
            }
            rrPvalues = unlist(lapply(object@data, relative_risk_pvalue)) 
            return(rrPvalues)
          }
)

#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getOddsRatioValues function
#-------------------------------------------------------------------------------#
setGeneric("getOddsRatioValues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getOddsRatioValues")
           }
)

setMethod("getOddsRatioValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_cnt1 <- sum(ctr_data > thresholdValue, na.rm=T) + 0.5
            ctr_cnt2 <- length(which(!is.na(ctr_data))) - ctr_cnt1 + 0.5
            odds_ratio <- function(x) {
              x_cnt1 <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T) + 0.5
              x_cnt2 <- length(which(!is.na(x[,column]))) - x_cnt1 + 0.5
              return(log(x_cnt1*ctr_cnt2)-log(x_cnt2*ctr_cnt1))
            }
            orValues = unlist(lapply(object@data, odds_ratio)) 
            return(orValues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getOddsRatioValues function
#-------------------------------------------------------------------------------#
setGeneric("getOddsRatioPvalues",
           function(object, refSamp, thresholdValue, column, ...) {
             standardGeneric("getOddsRatioPvalues")
           }
)

setMethod("getOddsRatioPvalues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, thresholdValue, column, side=FALSE, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_cnt1 <- sum(ctr_data > thresholdValue, na.rm=T) + 0.5
            ctr_cnt2 <- length(which(!is.na(ctr_data))) - ctr_cnt1 + 0.5
            odds_ratio_pvalue <- function(x) {
              x_cnt1 <- sum(as.numeric(as.vector(x[,column]))>thresholdValue, na.rm=T) + 0.5
              x_cnt2 <- length(which(!is.na(x[,column]))) - x_cnt1 + 0.5
              s <- sqrt(1/x_cnt1+1/x_cnt2+1/ctr_cnt1+1/ctr_cnt2)
              return(pnorm((log(x_cnt1*ctr_cnt2)-log(x_cnt2*ctr_cnt1))/s, lower.tail=side))
            }
            orPvalues = unlist(lapply(object@data, odds_ratio_pvalue)) 
            return(orPvalues)
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
# TCAGeneBasedData::getRelativeProbValuesML function
#-------------------------------------------------------------------------------#
setGeneric("getRelativeProbValuesML",
           function(object, refSamp, column, ...) {
             standardGeneric("getRelativeProbValuesML")
           }
)

setMethod("getRelativeProbValuesML",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            refNames <- names(object@data)
            refId <- which(refNames==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            ctr_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            shape1 <- ctr_bar*((ctr_bar*(1-ctr_bar)/v)-1)
            shape2 <- (1-ctr_bar)*((ctr_bar*(1-ctr_bar)/v)-1)
            #print(c(shape1, shape2))
            options(warn=-1)                                                 
            set.seed(123)
            results <- fitdist(ctr_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
            names(results) <- NULL
            ctr_alpha <- results[1]
            ctr_beta <- results[2]
            options(warn=0)
            #ctr_prob <- sum(ctr_data)/ctr_len
            ctr_prob <- ctr_alpha/(ctr_alpha+ctr_beta)
            ctr_var <- ctr_beta/(ctr_len*ctr_alpha*(ctr_alpha+ctr_beta+1))
            ctr_var_od <- ((ctr_alpha+ctr_beta)^2)/(ctr_len*ctr_alpha*ctr_beta*(ctr_alpha+ctr_beta+1)) 
            
            rr_ml_val <- c()
            rr_ml_pval_high <- c()
            rr_ml_pval_low <- c()
            od_ml_val <- c()
            od_ml_pval_high <- c()
            od_ml_pval_low <- c()
            for (i in 1:length(refNames)) {
              x_data <- as.numeric(as.vector(object@data[[i]][, column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
              shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              #print(c(shape1, shape2))
              options(warn=-1)
              set.seed(123)
              results <- fitdist(x_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
              names(results) <- NULL
              x_alpha <- results[1]
              x_beta <- results[2]
              options(warn=0)
              #x_prob <- sum(x_data)/x_len
              x_prob <- x_alpha/(x_alpha+x_beta)
              x_var <- x_beta/(x_len*x_alpha*(x_alpha+x_beta+1))
              rr = log(x_prob)-log(ctr_prob)
              rr_ml_val <- c(rr_ml_val, rr)
              rr_ml_pval_high <- c(rr_ml_pval_high, pnorm(rr/sqrt(x_var+ctr_var), lower.tail=FALSE))
              rr_ml_pval_low <- c(rr_ml_pval_low, pnorm(rr/sqrt(x_var+ctr_var), lower.tail=TRUE))
              od <- log(x_prob*(1-ctr_prob)) - log(ctr_prob*(1-x_prob))
              od_ml_val <- c(od_ml_val, od)
              x_var_od <- ((x_alpha+x_beta)^2)/(x_len*x_alpha*x_beta*(x_alpha+x_beta+1))
              std <- sqrt(x_var_od+ctr_var_od)
              od_ml_pval_high <- c(od_ml_pval_high, pnorm(od/std, lower.tail=FALSE))
              od_ml_pval_low <- c(od_ml_pval_low, pnorm(od/std, lower.tail=TRUE))
            }
            
            prob_relativeValues <- as.data.frame(cbind(rr_ml_val=rr_ml_val,
                                                       rr_ml_pval_high=rr_ml_pval_high,
                                                       rr_ml_pval_low=rr_ml_pval_low,
                                                       od_ml_val=od_ml_val,
                                                       od_ml_pval_high=od_ml_pval_high,
                                                       od_ml_pval_low=od_ml_pval_low))
            row.names(prob_relativeValues) <- refNames
            return(prob_relativeValues) 
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPercentValuesMM function
#-------------------------------------------------------------------------------#
setGeneric("getPercentValuesMM",
           function(object, refSamp, column, ...) {
             standardGeneric("getPercentValuesMM")
           }
)

setMethod("getPercentValuesMM",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            refNames <- names(object@data)
            pPositiveCells <- c()
            pPositiveCells[refNames] <- 0
            pPositiveCellsSd <- c()
            pPositiveCellsSd[refNames] <- 0
            for (i in 1:length(refNames)) {
              dat <- as.numeric(as.vector(object@data[[i]][, column]))
              dat <- dat[!is.na(dat)]
              x_len <- length(dat)
              x_bar <- mean(dat)
              pPositiveCells[refNames[i]] <- x_bar 
              v <- ((x_len-1)/x_len)*(sd(dat))^2
              x_alpha <- x_bar*((x_bar*(1-x_bar)/v)-1)
              x_beta <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              x_var <- (x_alpha*x_beta)/(x_len*((x_alpha+x_beta)^2)*(x_alpha+x_beta+1))
              pPositiveCellsSd[refNames[i]] <- sqrt(x_var)
            }
            percentOfControl <- pPositiveCells[refNames]/pPositiveCells[refSamp]
            
            alphaValue <- 1
            percentOfControlPvalue <- c()
            percentOfControlPvalue[refNames] <- 1 
            percentOfControl_pos <- percentOfControl[which(percentOfControl>=alphaValue)]
            if (length(percentOfControl_pos)) {
              percentPvalue_pos_tmp <- sapply(percentOfControl_pos, function(x) integrate(null_ratio2normals, lower=x, upper=Inf, alpha=alphaValue, mu=pPositiveCells[refSamp], sigma=pPositiveCellsSd[refSamp]))  
              percentPvalue_pos <- unlist(percentPvalue_pos_tmp[seq(from=1, to=length(percentPvalue_pos_tmp), by=5)])
              names(percentPvalue_pos) <- colnames(percentPvalue_pos_tmp) 
            }
            percentOfControlPvalue[names(percentPvalue_pos)] <- percentPvalue_pos[names(percentPvalue_pos)]
            percentOfControlPvalue[which(percentOfControlPvalue>1)] <- 1
            results <- as.data.frame(cbind(percent=percentOfControl[refNames], pvalue=percentOfControlPvalue[refNames]))
            return(results)
          }
)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPercentValues function
#-------------------------------------------------------------------------------#
setGeneric("getPercentValues",
           function(object, refSamp, column, ...) {
             standardGeneric("getPercentValues")
           }
)

setMethod("getPercentValues",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            refNames <- names(object@data)
            pPositiveCells <- c()
            pPositiveCells[refNames] <- 0
            pPositiveCellsSd <- c()
            pPositiveCellsSd[refNames] <- 0
            for (i in 1:length(refNames)) {
              dat <- as.numeric(as.vector(object@data[[i]][, column]))
              dat <- dat[!is.na(dat)]
              x_len <- length(dat)
              x_bar <- mean(dat)
              v <- ((x_len-1)/x_len)*(sd(dat))^2
              shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
              shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              options(warn=-1)                                                 
              set.seed(123)
              results <- fitdist(dat, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
              names(results) <- NULL
              x_alpha <- results[1]
              x_beta <- results[2]
              options(warn=0)
              x_var <- (x_alpha*x_beta)/(x_len*((x_alpha+x_beta)^2)*(x_alpha+x_beta+1))
              pPositiveCells[refNames[i]] <- x_alpha/(x_alpha+x_beta)
              pPositiveCellsSd[refNames[i]] <- sqrt(x_var)
            }
            percentOfControl <- pPositiveCells[refNames]/pPositiveCells[refSamp]
            
            alphaValue <- 1
            percentOfControlPvalue <- c()
            percentOfControlPvalue[refNames] <- 1 
            percentOfControl_pos <- percentOfControl[which(percentOfControl>=alphaValue)]
            if (length(percentOfControl_pos)) {
              percentPvalue_pos_tmp <- sapply(percentOfControl_pos, function(x) integrate(null_ratio2normals, lower=x, upper=Inf, alpha=alphaValue, mu=pPositiveCells[refSamp], sigma=pPositiveCellsSd[refSamp]))  
              percentPvalue_pos <- unlist(percentPvalue_pos_tmp[seq(from=1, to=length(percentPvalue_pos_tmp), by=5)])
              names(percentPvalue_pos) <- colnames(percentPvalue_pos_tmp) 
            }
            percentOfControlPvalue[names(percentPvalue_pos)] <- percentPvalue_pos[names(percentPvalue_pos)]
            percentOfControlPvalue[which(percentOfControlPvalue>1)] <- 1
            results <- as.data.frame(cbind(percent=percentOfControl[refNames], pvalue=percentOfControlPvalue[refNames]))
            return(results)
          }
)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getRelativeProbPvaluesMM function
#-------------------------------------------------------------------------------#
setGeneric("getRelativeProbPvaluesMM",
           function(object, refSamp, column, ...) {
             standardGeneric("getRelativeProbPvaluesMM")
           }
)

setMethod("getRelativeProbPvaluesMM",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, side=FALSE, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            x_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            ctr_alpha <- x_bar*((x_bar*(1-x_bar)/v)-1)
            ctr_beta <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
            ctr_prob <- log(x_bar)
            ctr_var <- ctr_beta/(ctr_len*ctr_alpha*(ctr_alpha+ctr_beta+1))   
            
            prob_relative_pvalue <- function(x) {
              x_data <- as.numeric(as.vector(x[,column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              x_alpha <- x_bar*((x_bar*(1-x_bar)/v)-1)
              x_beta <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              x_prob <- log(x_bar)
              x_var <- x_beta/(x_len*x_alpha*(x_alpha+x_beta+1))
              s <- sqrt(x_var+ctr_var)
              return(pnorm((x_prob-ctr_prob)/s, lower.tail=side))
            }
            prob_relativePvalues = unlist(lapply(object@data, prob_relative_pvalue)) 
            return(prob_relativePvalues)
          }
)



#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getRelativeProbPvaluesML function
#-------------------------------------------------------------------------------#
setGeneric("getRelativeProbPvaluesML",
           function(object, refSamp, column, ...) {
             standardGeneric("getRelativeProbPvaluesML")
           }
)

setMethod("getRelativeProbPvaluesML",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, side=FALSE, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            x_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
            shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
            #print(c(shape1, shape2))
            options(warn=-1)                                                 
            set.seed(123)
            results <- fitdist(ctr_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
            names(results) <- NULL
            ctr_alpha <- results[1]
            ctr_beta <- results[2]
            options(warn=0)
            #ctr_prob <- sum(ctr_data)/ctr_len
            ctr_prob <- log(ctr_alpha/(ctr_alpha+ctr_beta))
            ctr_var <- ctr_beta/(ctr_len*ctr_alpha*(ctr_alpha+ctr_beta+1)) 
            prob_relative_pvalue <- function(x) {
              x_data <- as.numeric(as.vector(x[,column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
              shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              #print(c(shape1, shape2))
              options(warn=-1)
              set.seed(123)
              results <- fitdist(x_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
              names(results) <- NULL
              x_alpha <- results[1]
              x_beta <- results[2]
              options(warn=0)
              #x_prob <- sum(x_data)/x_len
              x_prob <- log(x_alpha/(x_alpha+x_beta))
              x_var <- x_beta/(x_len*x_alpha*(x_alpha+x_beta+1))
              s <- sqrt(x_var+ctr_var)
              return(pnorm((x_prob-ctr_prob)/s, lower.tail=side))
            }
            prob_relativePvalues = unlist(lapply(object@data, prob_relative_pvalue)) 
            return(prob_relativePvalues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getProbOddsRatioValuesMM function
#-------------------------------------------------------------------------------#
setGeneric("getProbOddsRatioValuesMM",
           function(object, refSamp, column, ...) {
             standardGeneric("getProbOddsRatioValuesMM")
           }
)

setMethod("getProbOddsRatioValuesMM",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            ctr_prob <- sum(ctr_data)/ctr_len
            prob_ratio <- function(x) {
              x_data <- as.numeric(as.vector(x[,column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_prob <- sum(x_data)/x_len
              return(log(x_prob/(1-x_prob))-log(ctr_prob/(1-ctr_prob)))
            }
            prob_oddsRatioValues = unlist(lapply(object@data, prob_ratio)) 
            return(prob_oddsRatioValues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getProbOddsRatioValuesML function
#-------------------------------------------------------------------------------#
setGeneric("getProbOddsRatioValuesML",
           function(object, refSamp, column, ...) {
             standardGeneric("getProbOddsRatioValuesML")
           }
)

setMethod("getProbOddsRatioValuesML",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            x_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
            shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
            options(warn=-1)
            set.seed(123)
            results <- fitdist(ctr_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
            names(results) <- NULL
            ctr_alpha <- results[1]
            ctr_beta <- results[2]
            options(warn=0)
            ctr_prob <- ctr_alpha/(ctr_alpha+ctr_beta)
            prob_odds_ratio_value <- function(x) {
              x_data <- as.numeric(as.vector(x[,column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
              shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              options(warn=-1)
              set.seed(123)
              results <- fitdist(x_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
              names(results) <- NULL
              x_alpha <- results[1]
              x_beta <- results[2]
              options(warn=0)
              #x_prob <- sum(x_data)/x_len
              x_prob <- x_alpha/(x_alpha+x_beta)
              return(log(x_prob/(1-x_prob))-log(ctr_prob/(1-ctr_prob)))
            }
            prob_oddsRatioValues = unlist(lapply(object@data, prob_odds_ratio_value)) 
            return(prob_oddsRatioValues)
          }	
)




#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getProbOddsRatioPvaluesMM function
#-------------------------------------------------------------------------------#
setGeneric("getProbOddsRatioPvaluesMM",
           function(object, refSamp, column, ...) {
             standardGeneric("getProbOddsRatioPvaluesMM")
           }
)

setMethod("getProbOddsRatioPvaluesMM",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, side=FALSE, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            x_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            ctr_alpha <- x_bar*((x_bar*(1-x_bar)/v)-1)
            ctr_beta <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
            ctr_prob <- sum(ctr_data)/ctr_len
            ctr_var <- ((ctr_alpha+ctr_beta)^2)/(ctr_len*ctr_alpha*ctr_beta*(ctr_alpha+ctr_beta+1)) 
            prob_odds_ratio_pvalue <- function(x) {
              x_data <- as.numeric(as.vector(x[,column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              x_alpha <- x_bar*((x_bar*(1-x_bar)/v)-1)
              x_beta <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              x_prob <- sum(x_data)/x_len
              x_var <- ((x_alpha+x_beta)^2)/(x_len*x_alpha*x_beta*(x_alpha+x_beta+1))
              s <- sqrt(x_var+ctr_var)
              return(pnorm((log(x_prob/(1-x_prob))-log(ctr_prob/(1-ctr_prob)))/s, lower.tail=side))
            }
            prob_oddsRatioPvalues = unlist(lapply(object@data, prob_odds_ratio_pvalue)) 
            return(prob_oddsRatioPvalues)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getProbOddsRatioPvaluesML function
#-------------------------------------------------------------------------------#
setGeneric("getProbOddsRatioPvaluesML",
           function(object, refSamp, column, ...) {
             standardGeneric("getProbOddsRatioPvaluesML")
           }
)

setMethod("getProbOddsRatioPvaluesML",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, refSamp, column, side=FALSE, ...) {
            refId <- which(names(object@data)==refSamp)
            ctr_data <- as.numeric(as.vector(object@data[[refId]][, column]))
            ctr_data <- ctr_data[!is.na(ctr_data)]
            ctr_len <- length(ctr_data)
            x_bar <- mean(ctr_data) 
            v <- ((ctr_len-1)/ctr_len)*(sd(ctr_data))^2
            shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
            shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
            options(warn=-1)
            set.seed(123)
            results <- fitdist(ctr_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
            names(results) <- NULL
            ctr_alpha <- results[1]
            ctr_beta <- results[2]
            options(warn=0)
            ctr_prob <- ctr_alpha/(ctr_alpha+ctr_beta)
            ctr_var <- ((ctr_alpha+ctr_beta)^2)/(ctr_len*ctr_alpha*ctr_beta*(ctr_alpha+ctr_beta+1)) 
            prob_odds_ratio_pvalue <- function(x) {
              x_data <- as.numeric(as.vector(x[,column]))
              x_data <- x_data[!is.na(x_data)]
              x_len <- length(x_data)
              x_bar <- mean(x_data) 
              v <- ((x_len-1)/x_len)*(sd(x_data))^2
              shape1 <- x_bar*((x_bar*(1-x_bar)/v)-1)
              shape2 <- (1-x_bar)*((x_bar*(1-x_bar)/v)-1)
              options(warn=-1)
              set.seed(123)
              results <- fitdist(x_data, "beta", start=list(shape1=shape1, shape2=shape2))$estimate
              names(results) <- NULL
              x_alpha <- results[1]
              x_beta <- results[2]
              options(warn=0)
              #x_prob <- sum(x_data)/x_len
              x_prob <- x_alpha/(x_alpha+x_beta)
              x_var <- ((x_alpha+x_beta)^2)/(x_len*x_alpha*x_beta*(x_alpha+x_beta+1))
              s <- sqrt(x_var+ctr_var)
              return(pnorm((log(x_prob/(1-x_prob))-log(ctr_prob/(1-ctr_prob)))/s, lower.tail=side))
            }
            prob_oddsRatioPvalues = unlist(lapply(object@data, prob_odds_ratio_pvalue)) 
            return(prob_oddsRatioPvalues)
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
            percents = unlist(lapply(object@data, function(x) {
              val <- as.numeric(as.vector(x[,column]))
              val <- val[which(!is.na(val))] 
              lg <- length(val)
              #print(val)
              if (lg)  
                return(sum(val>threshold, na.rm=T)/lg)
            }
            ))  
            return(percents)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPercentAboveMultiThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getPercentAboveMultiThreshold",
           function(object, sampName, thresholds, column, ...) {
             standardGeneric("getPercentAboveMultiThreshold")
           }
)

setMethod("getPercentAboveMultiThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sampName, thresholds, column, ...) {
            percents = unlist(lapply(object@data, function(x) {
              g = unique(x$GeneName)
              if (g == sampName)
                return(0.5)        
              if (is.null(thresholds[g, column]))
                return(0)
              val <- as.numeric(as.vector(x[,column]))
              val <- val[which(!is.na(val))] 
              lg <- length(val)
              #print(val)
              if (lg)  
                return(sum(val>thresholds[g,column], na.rm=T)/lg)
            }
            ))  
            return(percents)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getControlPercentAboveMultiThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getControlPercentAboveMultiThreshold",
           function(object, sampName, thresholds, column, ...) {
             standardGeneric("getControlPercentAboveMultiThreshold")
           }
)

setMethod("getControlPercentAboveMultiThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sampName, thresholds, column, ...) {
            dat <- getContent(object)
            nt <- dat[[which(names(dat)==sampName)]]
            val <- as.numeric(as.vector(nt[,column]))
            val <- val[which(!is.na(val))] 
            percents = unlist(lapply(object@data, function(x) {
              g = unique(x$GeneName)
              if (g == sampName)
                return(0.5)
              if (is.null(thresholds[g, column]))
                return(1)
              lg <- length(val)
              #print(val)
              if (lg)  
                return(sum(val>thresholds[g,column], na.rm=T)/lg)
            }
            ))  
            return(percents)
          }
)




#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPCAPercentAboveThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getPCAPercentAboveThreshold",
           function(object, pcaData, logisticModel, ...) {
             standardGeneric("getPCAPercentAboveThreshold")
           }
)

setMethod("getPCAPercentAboveThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, pcaData, logisticModel, ...) {
            percents = unlist(lapply(object@data, function(x) {
              probs <- predict(logisticModel,  newdata=x, type="response")
              lg <- length(probs)
              #print(val)
              if (lg)  
                return(sum(probs>0.5, na.rm=T)/lg)
            }
            ))  
            return(percents)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getPCACountAboveThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getPCACountAboveThreshold",
           function(object, pcaData, logisticModel, ...) {
             standardGeneric("getPCACountAboveThreshold")
           }
)

setMethod("getPCACountAboveThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, pcaData, logisticModel, ...) {
            percents = unlist(lapply(object@data, function(x) {
              probs <- predict(logisticModel,  newdata=x, type="response")
              lg <- length(probs)
              #print(val)
              if (lg)  
                return(sum(probs>0.5, na.rm=T))
            }
            ))  
            return(percents)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getMedianAboveThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getMedianAboveThreshold",
           function(object, threshold, column, ...) {
             standardGeneric("getMedianAboveThreshold")
           }
)

setMethod("getMedianAboveThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, threshold, column, ...) {
            medians = unlist(lapply(object@data, function(x) {
              val <- as.numeric(as.vector(x[,column]))
              val <- val[which(!is.na(val))]
              if (length(val))
                return(median(val[which(val>threshold)]))
              else
                return(NA) 
            }
            ))  
            return(medians)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::getMedians function
#-------------------------------------------------------------------------------#
setGeneric("getMedians",
           function(object, column, ...) {
             standardGeneric("getMedians")
           }
)

setMethod("getMedians",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, column, ...) {
            medians = unlist(lapply(object@data, function(x) {
              val <- as.numeric(as.vector(x[,column]))
              val <- val[which(!is.na(val))]
              if (length(val))
                return(median(val))
              else
                return(NA) 
            }
            ))  
            return(medians)
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
# TCAGeneBasedData::getCountAboveMultiThreshold function
#-------------------------------------------------------------------------------#
setGeneric("getCountAboveMultiThreshold",
           function(object, thresholds, column, ...) {
             standardGeneric("getCountAboveMultiThreshold")
           }
)

setMethod("getCountAboveMultiThreshold",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, thresholds, column, ...) {
            counts = unlist(lapply(object@data, function(x) {
              g = unique(x$GeneName)
              if (is.null(thresholds[g, column]))
                return(0)
              val <- as.numeric(as.vector(x[,column]))
              val <- val[which(!is.na(val))] 
              return(sum(val>thresholds[g, column], na.rm=T))
            }
            ))  
            return(counts)
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
              tit <- paste("Percent of intensity values above Threshold for", columnName)
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.axis=1.1,ylab="% above threshold")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=mydata[posSamp], lty=4, col="darkred") 
            text(mydata[posSamp]+2, "Positive control", col="darkred", cex=0.5) 
            abline(h=mydata[negSamp], lty=4, col="darkred", cex=0.5)
            text(mydata[negSamp]+2, "Negative control", col="darkred", cex=0.5) 
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(mydata)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            if (addtitle)
              mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotMultiThresholdPercentData function
#-------------------------------------------------------------------------------#
setGeneric("plotMultiThresholdPercentData",
           function(object, sobject, thresholds, columnId, columnName, ...) {
             standardGeneric("plotMultiThresholdPercentData")
           }
)

setMethod("plotMultiThresholdPercentData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, thresholds, columnId, columnName, cnt, negSamp, posSamp, addtitle=1) {
            lengths <- getLengthSummary(sobject, columnId)
            lengths <- lengths[which(lengths > 0)]
            mydata <- getPercentAboveMultiThreshold(object, negSamp, thresholds, columnName)
            #print(mydata)
            eps <- sqrt(mydata*(1-mydata)[names(lengths)]/lengths)
            dataUp <- 100*(mydata+eps[names(mydata)]) 
            dataDn <- 100*(mydata-eps[names(mydata)])
            mydata <- 100*mydata
            par(mar = c(6.5,3.9,3,0) +0)
            tit <- ""
            if (addtitle)
              tit <- paste("Percent of intensity values above Threshold for", columnName)
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.axis=1.1,ylab="% above threshold")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            #abline(h=mydata[posSamp], lty=4, col="darkred") 
            #text(mydata[posSamp]+2, "Positive control", col="darkred", cex=0.5) 
            #abline(h=mydata[negSamp], lty=4, col="darkred", cex=0.5)
            #text(mydata[negSamp]+2, "Negative control", col="darkred", cex=0.5) 
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            mtext(as.numeric(cnt[names(mydata)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
            if (addtitle)
              mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)
          }
)


#-------------------------------------------------------------------------------#
# TCAGeneBasedData::plotPercentData function
#-------------------------------------------------------------------------------#
setGeneric("plotPaperPercentData",
           function(object, sobject, threshold, columnId, columnName, ...) {
             standardGeneric("plotPaperPercentData")
           }
)

setMethod("plotPaperPercentData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, sobject, threshold, columnId, columnName, cnt, posSamp, addtitle=1) {
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
              tit <- paste("Percent of intensity values above Threshold")
            #MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.main=1.5, cex.axis=1.5, cex.lab=1.5,cex.names=1.2,ylab="% above thrshold")
            MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.lab=1.5,ylab="% above threshold")
            segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
            segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
            segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
            abline(h=mydata[posSamp], lty=4) 
            text(5, mydata[posSamp]+1, "Negative control", cex=1.2) 
            #axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=2.0,tck=-0.012)
            axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
            #mtext(as.numeric(cnt[names(mydata)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
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
            MidPts <- barplot(mydata,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.main=0.9, cex.lab=1.5,ylab="% of positive cells")
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
            MidPts <- barplot(mean_data,main=tit,las=2,ylim=c(0,1),cex.names=0.8,cex.lab=1.5,cex.main=0.9, ylab="Probabilities of positive wells")
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


#-----------------------------------------------------------------------------------------#
# TCAGeneBasedData::getPCAInputData function
#-----------------------------------------------------------------------------------------#
setGeneric("getPCAInputData",
           function(object, negSamp, posSamp, ...) {
             standardGeneric("getPCAInputData")
           }
)


setMethod("getPCAInputData",
          signature = signature("TCAGeneBasedData"),
          definition = function(object, negSamp, posSamp, ...) {
            dat.f <- getContent(object)
            pos.id <- which(names(dat.f)==posSamp)
            neg.id <- which(names(dat.f)==negSamp)
            gene.id <- which(names(dat.f[[pos.id]])=="GeneName")
            dat <- rbind(dat.f[[neg.id]], dat.f[[pos.id]])
            pos.nrow <- length(which(dat[, gene.id]==posSamp))
            neg.nrow <- length(which(dat[, gene.id]==negSamp))
            dat <- dat[, -gene.id]
            dat$Response <- c(rep(0, neg.nrow), rep(1, pos.nrow))
            return(dat)
          }
)


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
