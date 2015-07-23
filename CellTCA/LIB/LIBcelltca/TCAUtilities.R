
plot_overscreen_percent <- function(d, data_file, wd, ht, addtitle=1) {
  maindat <- ""
  if (addtitle)
    maindat <- "Proportion of positive cells for positive control over the screening"
  xlabdat <- "Proportions"
  ylabdat <- "Likelihood values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d, na.rm=T), type="l", main=maindat, col="darkred", xlab=xlabdat, ylab=ylabdat)
  dev.off()
}  


plot_overscreen_cutoff <- function(d, data_file, wd, ht, addtitle=1) {
  maindat <- ""
  if (addtitle)
    maindat <- "Decision cutoff values over the screen"
  xlabdat <- "Cutoff Values"
  ylabdat <- "Density values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d, na.rm=T), type="l", main=maindat, col="darkred", xlab=xlabdat, ylab=ylabdat)
  dev.off()
}  


plot_infection_index <- function(d, data_file, wd, ht, addtitle=1) {
  maindat <- ""
  if (addtitle)
    maindat <- "Percent of positive control over the screening"
  xlabdat <- "Percent of control"
  ylabdat <- "Likelihood values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d, na.rm=T), type="l", main=maindat, col="darkred", xlab=xlabdat, ylab=ylabdat)
  dev.off()
}   


plot_toxicity_index <- function(d, data_file, wd, ht, addtitle=1) {
  maindat <- ""
  if (addtitle)
    maindat <- "Toxicity Index over the screening"
  xlabdat <- "Toxicity Index"
  ylabdat <- "Likelihood values"
  col <- c("green", "red", "blue")
  xlim <- c(0, 1)
  ylim <- c(0, 8)
  pdf(file=data_file, width=wd, height=ht)
  #plot(density(d), type="l", main=main, xlim=xlim, ylim=ylim, xlab=xlab, ylab=ylab) 
  plot(density(d, na.rm=T), type="l", main=maindat, col="darkred", xlab=xlabdat, ylab=ylabdat)
  dev.off()
}   


calculate_cutoffs <- function(values, percentile1, percentile2) {
  qqvalues <- qqnorm(values[!is.na(values)], plot.it=FALSE)
  qvals <- quantile(values[!is.na(values)], c(percentile1, percentile2))
  qnrms <- qnorm(c(percentile1, percentile2))
  slope <- diff(qvals)/diff(qnrms)
  int <- qvals[1] - slope * qnrms[1]
  x <- sort(qqvalues$x)
  y <- sort(qqvalues$y)
  distance <- abs(slope * x - y + int)/sqrt(1+slope*slope)
  
  n <- length(distance)
  z <- qt(0.975, df=n-1)
  s2 <- sd(log(distance))^2
  s4 <- s2^2
  delta <- z*sqrt((s2/n)+(s4/(2*(n-1))))
  avg <- mean(log(distance))+(s2/2)
  conf_int <- exp(c(avg-delta, avg+delta))
  mdistance <- conf_int[1]
  
  #mdistance <- mean(distance)
  #sdistance <- sd(distance)/sqrt(length(distance))
  #delta_max <- mdistance + sdistance 
  #delta_min <- mdistance - sdistance        
  idx_beg <- which(y <= qvals[1])
  idx_end <- which(y >= qvals[2])
  begs_x <- x[idx_beg]
  begs_y <- y[idx_beg]
  ends_x <- x[idx_end]
  ends_y <- y[idx_end]
  dist_beg <- abs((slope * begs_x - begs_y + int)/sqrt(1+slope*slope))
  dist_end <- abs((slope * ends_x - ends_y + int)/sqrt(1+slope*slope))
  if (length(which(dist_beg >= mdistance))) {
    M <- max(which(dist_beg >= mdistance))
    i_beg <- idx_beg[M]
  }
  else {
    i_beg <- idx_beg[1]
  }
  if (length(which(dist_end >= mdistance))) {  
    m <- min(which(dist_end >= mdistance))
    i_end <- idx_end[m]
  }
  else {
    i_end <- idx_end[length(idx_end)]
  }
  return(c(x[i_beg], y[i_beg], x[i_end], y[i_end]))
} 



plot_infection_index_cutoff <- function(values, data_file, wd, ht) {
  values <- values[!is.na(values)]
  dd <- density(values)
  maxVal <- max(dd$y)
  xVal <- dd$x[max(which(abs(dd$y-maxVal) < 1e-10))]
  cdFunction <- ecdf(values)
  refPercentile <- cdFunction(xVal)
  percentile1 <- refPercentile - 0.25
  percentile2 <- refPercentile + 0.25
  cutoffs <- calculate_cutoffs(values, percentile1, percentile2)
  pdf(file=data_file, width=wd, height=ht)
  qqnorm(values)
  qqline(values, col="red", lwd=2)
  abline(h=cutoffs[2], col="darkred")
  abline(h=cutoffs[4], col="darkred")
  text((cutoffs[1]+cutoffs[3])/2, cutoffs[2]+0.07, paste("Low cutoff = ", round(cutoffs[2], digits=3), sep=""), col="darkred", cex=0.8)
  text((cutoffs[1]+cutoffs[3])/2, cutoffs[4]+0.07, paste("High cutoff = ", round(cutoffs[4], digits=3), sep=""), col="darkred", cex=0.8)
  dev.off()
  return(cutoffs)
}   


plot_toxicity_index_cutoff <- function(values, data_file, wd, ht) {
  values <- values[!is.na(values)]
  dd <- density(values)
  maxVal <- max(dd$y)
  xVal <- dd$x[max(which(abs(dd$y-maxVal) < 1e-10))]
  cdFunction <- ecdf(values)
  refPercentile <- cdFunction(xVal)
  percentile1 <- refPercentile - 0.25
  percentile2 <- refPercentile + 0.25
  cutoffs <- calculate_cutoffs(values, percentile1, percentile2)
  pdf(file=data_file, width=wd, height=ht)
  qqnorm(values)
  qqline(values, col="red", lwd=2)
  abline(h=cutoffs[4], col="darkred")
  text((cutoffs[1]+cutoffs[3])/2, cutoffs[4]+0.07, paste("Cutoff = ", round(cutoffs[4], digits=3), sep=""), col="darkred", cex=0.8)
  dev.off()
  return(cutoffs)
}   

save_plate_boxplot_without_outliers <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (! require("reshape2"))
    stop("Require reshape2 package")
  data <- melt(getGeneBasedData(geneBasedData))
  p <- ggplot(data, aes(factor(GeneName), value))
  p + geom_boxplot(outlier.shape = NA) + scale_y_continuous(limits = quantile(data$value, c(0,0.993))) + facet_wrap(~variable, scale="free")
  ggsave(filename=file_name, plot=last_plot(), path=file_path, width=25, height=20, dpi=400)
}


save_plate_boxplot <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (!require(reshape2))
    stop("Require reshape2 package")
  data <- melt(getGeneBasedData(geneBasedData))
  p <- ggplot(data, aes(factor(GeneName), value))
  p + geom_boxplot() + scale_y_continous(limits = quantile(data$value, c(0,0.993))) + facet_wrap(~variable, scale="free")
  ggsave(filename=file_name, plot = last_plot(), path=file_path, width=25, height=20, dpi=400) 
}


save_plate_boxplot_brut <- function(geneBasedData, file_name, file_path) {
  if (! require(ggplot2))
    stop("Require ggplot2 package")
  if (!require(reshape2))
    stop("Require reshape2 package")
  data <- melt(getGeneBasedData(geneBasedData))
  p <- ggplot(data, aes(factor(GeneName), value))
  p + geom_boxplot() + facet_wrap(~variable, scale="free")
  ggsave(filename=file_name, plot = last_plot(), path=file_path, width=25, height=20, dpi=400)
}


#-------------------------------------------------------------------------------

setGeneric("KLdist.matrix", function(x, ...) standardGeneric("KLdist.matrix"))

setMethod("KLdist.matrix",signature=signature("list"), 
          function(x,gridsize=NULL,symmetrize = FALSE, diag = FALSE,upper=FALSE){
            n <- length(x)
            clist <- vector("list", length=n)
            me <- .Machine$double.eps
            
            interpfunc <- function(x,y,...) {
              f <- function(w) approx(x,y, w, yleft=0, yright=0)$y
              class(f) <- "dfun"
              f
            }
            
            datRange <- matrix(ncol=2,nrow=n)
            binWidth <- vector(length=n)
            bins <- list()
            binCounts <-list()
            
            nc <- unlist(lapply(x,length))
            for( i in 1:n){
              if(nc[i] >10000){
                dat <- sample(x[[i]],nc[i]*0.1)
              }else{
                dat <- x[[i]]
              }
              if(!all(is.na(dat))){
                datRange[i,] <- range(dat)
                binWidth[i] <- dpih(dat,gridsize=if(is.null(gridsize))	max(401,length(dat)/10) else gridsize)
                bins[[i]] <- seq(datRange[i,1]-0.1, datRange[i,2]+0.1+binWidth[i], 
                                 by=binWidth[i])
                binCounts[[i]] <- KernSmooth:::linbin(x[[i]],bins[[i]],truncate=T)/
                  (nc[i]*binWidth[i])
              }
            }   
            
            distfun <- function(x,bins,binCounts,binWidth,i,j)
            {   
              step <- min(binWidth[i],binWidth[j])
              combRange <- datRange[c(i,j),]
              supp <- c(min(combRange[,1]),max(combRange[,2]))
              p<- seq(from= supp[1], to =supp[2], by= step)
              f <- interpfunc(bins[[i]],binCounts[[i]])
              g <- interpfunc(bins[[j]],binCounts[[j]])
              dist<-sum(log((f(p)+me)/(g(p)+me))*f(p))*step
              
              if(symmetrize)
              {
                dist <- (dist +  sum(log((g(p)+me)/(f(p)+me))*g(p))*step)/2
              }
              return(dist)
            }
            
            
            ans<-rep(NA, n*(n-1)/2)
            ct <- 1
            for(i in 1:(n-1))
              for(j in (i+1):n) {
                if(!is.na(x[[i]]) && !is.na(x[[j]]))
                  ans[ct] <- distfun(x,bins,binCounts,binWidth,i,j)
                else
                  ans[ct]=NA
                ct <- ct+1
              }
            attributes(ans) <- list(Size = n, Labels = names(x),
                                    Diag = diag, Upper = upper, 
                                    methods ="KLdist", 
                                    class = "dist")
            
            ans
          })


getNormPvalues = function(lengths, counts, negSamp) {
  # calculate abs(x_sample_bar - x_control_bar)
  num = abs((counts/lengths) - (counts[negSamp]/lengths[negSamp]))
  #print(counts)
  #print(lengths)
  #print(negSamp)
  #print(num)
  # calculate sqrt(x_total_bar(1-x_total_bar))*(1/n_sample + 1/n_control)
  c_s_plus_c_c = counts + counts[negSamp]
  n_s_plus_n_c = lengths + lengths[negSamp]
  n_s_times_n_c = lengths * lengths[negSamp]
  #print(c_s_plus_c_c)
  #print(n_s_plus_n_c)
  #print(n_s_times_n_c)
  #print(c_s_plus_c_c * (n_s_plus_n_c - c_s_plus_c_c))
  den = sqrt(c_s_plus_c_c * (n_s_plus_n_c - c_s_plus_c_c))/n_s_times_n_c
  return(pnorm(num/den, lower.tail=FALSE))
}


general_ratio2normals <- function(x, mu_i, sigma_i, mu_c, sigma_c) {
  f1 <- ((mu_c*sigma_i^2) + (x*mu_i*sigma_c^2))/(sqrt(2*pi)*(sigma_i^2+sigma_c^2*x^2)^(3/2))
  f2 <- ((mu_i - mu_c*x)^2)/(2*((sigma_i^2)+(sigma_c^2)*x^2))
  y = f1 * exp(-f2)
  return(y)
}


general_ratio2normals_mean.1 <- function(x, mu_i, sigma_i, mu_c, sigma_c) {
  y = x * general_ratio2normals(x, mu_i, sigma_i, mu_c, sigma_c)
  return(y)      
}


general_ratio2normals_mean.2 <- function(x, mu_i, sigma_i, mu_c, sigma_c) {
  y = x^2 * general_ratio2normals(x, mu_i, sigma_i, mu_c, sigma_c)
  return(y)  
} 


general_ratio2normals_variance <- function(x, mu_i, sigma_i, mu_c, sigma_c) {
  m1 = integrate(general_ratio2normals_mean.1, lower=min(x), upper=max(x), mu_i=mu_i, sigma_i=sigma_i, mu_c=mu_c, sigma_c=sigma_c)$val
  m2 = integrate(general_ratio2normals_mean.2, lower=min(x), upper=max(x), mu_i=mu_i, sigma_i=sigma_i, mu_c=mu_c, sigma_c=sigma_c)$val
  y = m2 - (m1)^2
  return(y)
} 

null_ratio2normals = function(x, alpha, mu, sigma) {
  cst = mu/sigma
  f1 = (cst*alpha*(alpha+x))/(sqrt(2*pi)*((alpha^2)+(x^2))^(3/2))
  f2 = -((cst^2)*0.5*(alpha-x)^2)/((alpha^2)+(x^2))
  y = f1 * exp(f2)
  return(y)
}   

ratio2normals_mean.1 <- function(x, alpha, mu, sigma) {
  y = x * null_ratio2normals(x, alpha, mu, sigma)
  return(y)  
} 

ratio2normals_mean.2 <- function(x, alpha, mu, sigma) {
  y = x^2 * null_ratio2normals(x, alpha, mu, sigma)
  return(y)  
} 

ratio2normals_variance <- function(x, alpha, mu, sigma) {
  m1 = integrate(ratio2normals_mean.1, lower=min(x), upper=Inf, alpha=alpha, mu=mu, sigma=sigma)$val
  m2 = integrate(ratio2normals_mean.2, lower=min(x), upper=Inf, alpha=alpha, mu=mu, sigma=sigma)$val
  y = m2 - (m1)^2
  return(y)
}


get_h0_variances <- function(alpha, pPosCell, pPosCellsSigma) {
  tt <- seq(from=0.05, to=2, by=1/500)
  return(ratio2normals_variance(tt, alpha, pPosCell, pPosCellsSigma))  
} 

## Return mean and standart deviation
get_normal_parameters <- function(dat) {
  ddat <- density(dat, na.rm=T)
  mx <- ddat$x[which(ddat$y==max(ddat$y))]
  if (length(mx) > 1)
    mx <- mx[1]
  mx_b <- dat[which(dat<=mx)]
  mx_e <- dat[which(dat>=mx)]
  sx <- min(max(mx-mx_b),max(mx_e-mx))
  sm <- sd(dat[which((dat >= mx-sx) & (dat <= mx+sx))])
  return(c(mx, sm))
}  


## variante pour une dataframe
## Return mean and standart deviation
get_normal_parameters2 <- function(data) {
  ddata <- density(data, na.rm=T)
  mx <- ddata$x[which(ddata$y==max(ddata$y))]
  if (length(mx) > 1)
    mx <- mx[1]
  mx_b <- data[which(data<=mx)]
  mx_e <- data[which(data>=mx)]
  sx <- min(max(mx-mx_b),max(mx_e-mx))
  sm <- sd(data[which((data >= mx-sx) & (data <= mx+sx))])
  return(c(mx, sm))
}


getToxValues <- function(lengths, norm_pos, norm_neg) {
  return((lengths - norm_pos[1] - 3 * norm_pos[2])/abs(norm_neg[1] - norm_pos[1])) 
}

getZfactor <- function(norm_pos, norm_neg) {
  return(1 - ((3*(norm_pos[2]+norm_neg[2]))/abs(norm_pos[1]-norm_neg[1])))
}


#-------------------------------------------------------------------------------#
# medianPlot
#-------------------------------------------------------------------------------#

medianPlot <- function(medianValues, nr, nc, colName, fname, ht, wd, addtitle=1) {
  pdf(file=fname, width=wd, height=ht);
  tit <- ""
  if (addtitle)
    tit <- paste(c("Average Median Values over the screening for ", colName), collapse="")
  plotPlate(as.vector(t(medianValues)), ncol=nc, nrow=nr, cex.char=0.8, na.action="xout", main=tit, 	
            col=brewer.pal(9, "YlOrBr"), add=FALSE);
  dev.off()
}


plotZfactor <- function(sampleNumber, nparam_p, nparam_n, sample_counts, fname, wd, ht, addtitle=1) {
  #pdf(file=fname, width=wd, height=ht);
  jpeg(file=fname, width=1728, height=650, res=150, quality=100);
  tit <- ""
  if (addtitle)
    tit <- paste("Cell number distribution for positive and negative toxicity controls", sep="")
  legtext <- c("Toxicity Negative Control", "Samples", "Toxicity Positive Control")
  #legtext <- c("Toxicity Negative Control", "Toxicity Positive Control")
  cols <- c("blue", "darkred", "red")
  #cols <- c("blue", "red")
  xlim_t <- c(nparam_p[1]-2.5*nparam_p[2], nparam_n[1]+2.5*nparam_n[2])
  plot(density(rnorm(sampleNumber, mean=nparam_n[1], sd=nparam_n[2])),main="",xlab="Cell Counts", col=cols[1], xlim=xlim_t)
  lines(density(sample_counts, na.rm=T), col=cols[2])
  lines(density(rnorm(sampleNumber, mean=nparam_p[1], sd=nparam_p[2])), col=cols[3])
  legend("top", inset=0.05, legend=legtext, col=cols, lty=c(1,1))
  dev.off()
}

my_xyplot <- function(y, x, groupname, colr, pchr, tnames, txlab, tylab, fname, wd, ht) {
  pdf(file=fname, width=wd, height=ht)
  xyplot(y ~ x, groups = groupname, col=colr, pch=pchr, xlab=txlab, ylab=tylab,
         key=list(points = list(pch=pchr),text=list(tnames),col=colr))
  dev.off()
} 


plotPCAData <- function(pcaInputData, pcaData, negSamp, posSamp, fname, wd, ht, addtitle=1) {
  scores <- as.data.frame(pcaData$ind$coord)
  scores$Response <- pcaInputData$Response
  colr <- c("red", "blue")
  pchr <- c(3,4)
  main.data <- ""
  if (addtitle)
    main.data <- "Individuals projection on 1st and 2nd principal components"
  pdf(fname, width=wd, height=ht)
  oplot <- xyplot(scores[, 2] ~ scores[, 1], groups = scores$Response, col=colr,
                  pch=pchr,xlab="1st Principal Component", ylab="2nd Principal Component",
                  key=list(points = list(pch=pchr),text=list(c(negSamp, posSamp)), main=main.data))
  plot(oplot)
  dev.off()
}


getLogisticModel <- function(pcaInputData, pcaData, nComp) {
  # predictive accuracy for incenp 0.959
  # predictive accuracy for aurkb 0.908
  # predictive accuracy for cul3 0.913
  scores <- as.data.frame(pcaData$ind$coord)
  cand_var <- names(scores)
  scores$Response <- pcaInputData$Response
  formul <- as.formula(paste("Response ~ ", paste(cand_var[nComp], collapse="+")))
  options(warn=-1)
  model <- glm(formul, data=scores, family=binomial())
  options(warn=0)
  return(model)
  #return(glm(Response ~ Dim.1 + Dim.2, data=scores, family=binomial()))
  #cand_var <- names(scores)
  #formul <- as.formula(paste("Response ~ ", paste(cand_var, collapse="+")))
  #model <- glm(formul, data=scores, family=binomial())
  #return(glm(Response ~ Dim.1 + Dim.2 + Dim.3 + Dim.4 + Dim.5, data=scores, family=binomial()))
  #return(glm(Response ~ Dim.1, data=scores, family=binomial()))
}

getLogisticModel_old <- function(pcaInputData, pcaData) {
  scores <- as.data.frame(pcaData$ind$coord)
  cand_var <- names(scores)
  scores$Response <- pcaInputData$Response
  formul <- as.formula(paste("Response ~ ", paste(cand_var[1:14], collapse="+")))
  return(glm(formul, data=scores, family=binomial()))
  #return(glm(Response ~ Dim.1 + Dim.2, data=scores, family=binomial()))
  #cand_var <- names(scores)
  #formul <- as.formula(paste("Response ~ ", paste(cand_var, collapse="+")))
  #model <- glm(formul, data=scores, family=binomial())
  #return(glm(Response ~ Dim.1 + Dim.2 + Dim.3 + Dim.4 + Dim.5, data=scores, family=binomial()))
  #return(glm(Response ~ Dim.1, data=scores, family=binomial()))
}

select_variable <- function(pcaInputData, pcaData) {
  scores <- as.data.frame(pcaData$ind$coord)
  variables <- names(scores)
  scores$Response <- pcaInputData$Response
  total <- rep(0.0, length(variables))
  for (v in 1:10) {
    results <- c()
    for (i in 1:length(variables)) {
      formul <- as.formula(paste("Response ~ ", paste(variables[1:i], collapse="+")))
      options(warn=-1)
      model <-  glm(formul, data=scores, family=binomial())
      options(warn=0)
      my.cv <- CVbinary(model)
      results <- c(results, my.cv$acc.cv)
    }
    total <- total + results
  } 
  return(total/10) 
}


getOptimalPrincipalComponents <- function(pcaInputData, pcaData) {
  r <- select_variable(pcaInputData, pcaData)
  ind <- which(max(r)==r)
  scores <- as.data.frame(pcaData$ind$coord)
  cand_var <- names(scores)
  scores$Response <- pcaInputData$Response
  formul <- as.formula(paste("Response ~ ", paste(cand_var, collapse="+")))
  options(warn=-1)
  model <- glm(formul, data=scores, family=binomial())
  options(warn=0)
  comp <- which(summary(model)$coefficients[,4] <0.05)-1
  if (comp[1] == 0)
    comp <- comp[-1]
  formul <- as.formula(paste("Response ~ ", paste(cand_var[comp], collapse="+")))
  options(warn=-1)
  model <- glm(formul, data=scores, family=binomial())
  options(warn=0)
  acc <- CVbinary(model)$acc.cv
  if (acc > r) {
    print(c("Max Predictive acc: ", acc))
    return(c(acc, comp))
  }
  print(c("Max Predictive acc: ", max(r)))
  return(c(max(r), 1:ind))
}

pcaBarPlots <- function(pPositiveCells, cellCountPerWell, posSamp, sampName, fname, wd, ht, countRepPerGene, addtitle) {
  pdf(fname, width=wd, height=ht)
  eps <- sqrt(pPositiveCells*(1-pPositiveCells)[names(cellCountPerWell)]/cellCountPerWell)
  dataUp <- 100*(pPositiveCells+eps[names(pPositiveCells)]) 
  dataDn <- 100*(pPositiveCells-eps[names(pPositiveCells)])
  pPositiveCells <- 100*pPositiveCells
  par(mar = c(6.5,3.9,3,0) +0)
  tit <- ""
  if (addtitle)
    tit <- "Percent of Positive Cells"
  MidPts <- barplot(pPositiveCells,main=tit,las=2,ylim=c(0,100),cex.names=0.8,cex.axis=1.1,ylab="% positive cells")
  segments(MidPts, dataDn, MidPts, dataUp, lty = "solid", lwd = 1)
  segments(MidPts-0.2, dataDn, MidPts+0.2, dataDn, lty = 1, lwd = 1)
  segments(MidPts-0.2, dataUp, MidPts+0.2, dataUp, lty = 1, lwd = 1)
  abline(h=pPositiveCells[posSamp], lty=4, col="darkred") 
  text(pPositiveCells[posSamp]+2, "Positive control", col="darkred", cex=0.5) 
  abline(h=pPositiveCells[negSamp], lty=4, col="darkred", cex=0.5)
  text(pPositiveCells[negSamp]+2, "Negative control", col="darkred", cex=0.5) 
  axis(1,labels=FALSE,at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
  mtext(as.numeric(countRepPerGene[names(pPositiveCells)]), at=MidPts, col="blue", side=1, line=-1,cex=0.5)
  if (addtitle)
    mtext("number of replicate-wells shown in blue at bottom of bars ; error bars : SEM of replicate-wells",side=3,line=0,cex=0.7)
  dev.off()
}

screePCAPlot <- function(pcaData, fname, wd, ht, addtitle) {
  pdf(fname, width=wd, height=ht)
  tit <- ""
  if (addtitle)
    tit <- "Scree plot" 
  barplot(pcaData$eig[,1], axes=T, xlab="Principal Components", ylab="Fraction od variance", names.arg=rep(1:length(pcaData$eig[,1])), main=tit)
  dev.off()
}


correlationDisplay <- function(pcaData, fname, wd, ht, addtitle) {
  pdf(fname, width=wd, height=ht)
  tit <- ""
  if (addtitle)
    tit <- "Correlation Display"
  plot(pcaData, axes=c(1, 2), choix="var", col.var="blue", new.plot=FALSE, cex=0.5, main=tit)
  dev.off()
}

plotPercentOfControlUtilities <- function(percentOfControl, fname, wd, ht, addtitle) {
  pdf(fname, width=wd, height=ht)
  tit <- ""
  if (addtitle)
    tit <- "Percent of control plot"
  par(mar = c(6.5,3.9,3,0) +0)
  MidPts <- barplot(percentOfControl,main=tit,las=2,cex.names=0.8,cex.axis=1,ylab="Percent of control")
  axis(1,labels=FALSE, at=MidPts,las=2,cex.axis=0.8,tck=-0.012)
  abline(h=1, lty=4, col="darkred") 
  text(1.15, "Top control", col="darkred", cex=0.5)
  dev.off()
}


getPercentErrorValues <- function(n, pGenes, pControls, sdGenes, sdControls) {
  results <- rep(0, length(pGenes))
  names(results) <- names(pGenes)
  for (g in names(pGenes)) {
    if (!(pGenes[g]==1 | pControls[g]==1 | pGenes[g] == 0 | pControls[g]==0)) { 
      x <- rnorm(n, mean=pGenes[g], sd=sdGenes[g])/rnorm(n, pControls[g], sdControls[g])
      results[g] <- sqrt(general_ratio2normals_variance(x, pGenes[g], sdGenes[g], pControls[g], sdControls[g]))
    }   
  }
  return(results)  
}


get_correlation <- function(pcaData, nComp) {
  for (item in nComp) {
    dimp <- paste("Dim.", item, sep="")
    r <- pcaData$var$cor[, dimp][which(pcaData$var$cor[, dimp]==max(pcaData$var$cor[, dimp]))]
    print(c(dimp, r))
  }
}


getLogisticModel2 <- function(controlsData, cols) {
  models <- list()
  for (col in cols) {
    formul <- as.formula(paste("Response ~ ", col)) 
    model <- glm(formul, data=controlsData, family=binomial())
    models[[col]] <- model
  }
  return(models)
}

getPredictivityAccuracy <- function(logisticModel) {
  p.acc <- c()
  cols <- names(logisticModel)
  for (col in cols) {
    my.cv <- CVbinary(logisticModel[[col]], print.details=FALSE)
    p.acc <- c(p.acc,  my.cv$acc.cv)
  }
  names(p.acc) <- cols
  return(p.acc)
}


pVal2lfdr <- function(x,silent=T) {     ##
  require(fdrtool)
  if(sum(is.na(x)) >0 & !silent)
    message(" (pVal2lfdr:) omitting ",sum(is.na(x))," NAs !")
  z <- as.numeric(na.omit(x))
  z <- as.numeric(fdrtool(z, statistic="pvalue",plot=F,verbose=!silent)$lfdr)
  y <- rep(NA,length(x))
  y[!is.na(x)] <- z
  return(y)
}


################################################################################
## create Output folder after ensuring that there will not be accidental file deletion
createOutputFolder <- function(outdir)
{
  ## See if output directory exists. If not, create. If yes, check if it is empty,
  ## and if not, depending on parameter 'force', throw an error or clean it up.	
  if(missing(outdir))
  {
    stop("Provide aa ouput directory name")
  }
  
  if(file.exists(outdir))
  {
    if(!file.info(outdir)$isdir)
      stop(sprintf("'%s' must be a directory.", outdir))
    outdirContents <- dir(outdir, all.files=TRUE)
    outdirContents <- setdiff(outdirContents, c(".", ".."))  
    if(length(outdirContents)>0)
      stop(sprintf("'%s' is not empty.", outdir))
  }
  else
  {
    dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
  }
  ## create "in" and "html" folder
  dir.create(file.path(outdir, "css"), showWarnings=FALSE)
  dir.create(file.path(outdir, "img"), showWarnings=FALSE)
}


###############################################################################
## Create Description HTML file
description2html <- function (inputDesc, outputDesc, headerFile, bottomFile) {
  html <- c()
  conInputDesc <- file(inputDesc)
  conOutputDesc <- file(outputDesc)
  conHeader <- file(headerFile)
  html <- c(html, readLines(conHeader))
  close(conHeader)
  html <- c(html, "<h1 class=\"block\">Project Description</h1>", "<div class=\"column1-unit\">")
  words <- readLines(conInputDesc)
  close(conInputDesc)
  justStart <- TRUE
  for (word in words) {
    if (length(grep("\\[", word))) {
      if (justStart) {
        justStart = FALSE
      } else {
        html <- c(html, "</div>", "<hr class=\"clear-contentunit\" /> <div class=\"column1-unit\">")
      }
      word <- gsub("(\\[|\\])", "", word)
      if (length(grep("description", word)) | length(grep("Files", word))) {
        html <- c(html, paste("<h1>", word, "</h1>"))
      }
    } else {
      html <- c(html, paste("<p>", word, "</p>"))
    }
  }
  html <- c(html, "</div>", "<hr class=\"clear-contentunit\" />")
  conBottom <- file(bottomFile)
  html <- c(html, readLines(conBottom))
  close(conBottom)
  cat(paste(html, collapse="\n"), file=conOutputDesc, append=TRUE)
  close(conOutputDesc)
}


###############################################################################
## Create an HTML plate layout
plate2html <- function(plateId, plateSetup, outputFile, headerFile, bottomFile) {
  html <- c()
  conHeader <- file(headerFile)
  html <- c(html, readLines(conHeader))
  close(conHeader)
  html[13] <- "  \t\t<link rel=\"stylesheet\" type=\"text/css\" media=\"screen,projection,print\" href=\"../css/layout_setup.css\" />"
  html[14] <- "  \t\t<link rel=\"stylesheet\" type=\"text/css\" media=\"screen,projection,print\" href=\"../css/layout_text.css\" />"
  html[61] <- "            \t\t\t\t<li><a href=\"../index.html\">Project Description</a></li>"
  html[66] <- "            \t\t\t\t<li><a href=\"../plateconf.html\">Plate Configuration</a></li>"
  html[71] <- "            \t\t\t\t<li><a href=\"../platelist.html\">Plate List</a></li>"
  html[76] <- "            \t\t\t\t<li><a href=\"../screensummary.html\">Screen Summary</a></li>"
  html[81] <- "            \t\t\t\t<li><a href=\"../screenresults.html\">Screen Results</a></li>"
  nImages <- 6
  titles <- c("Percent of positive cells per well", "Probalities of positive wells")
  captions <- c("Percent of positive cells", "Probalities of positive wells")
  titles <- c(titles, "Relative risk per well", "Soft Relative risk per well")
  captions <- c(captions, "Relative risk per well", "Soft Relative risk per well")
  titles <- c(titles, "Spatial  disposition of Relative risk per well", "Spatial  disposition of Soft Relative risk per well")
  captions <- c(captions, "Spatial disposition of Relative risk per well", "Spatial disposition of Soft Relative risk per well")
  html <- c(html, paste("<h1 class=\"block\">Plate ",plateId,"</h1>"))
  # Create plate setup table
  html <- c(html, "<div class=\"column1-unit\">", "<table>")
  for (i in 1:nrow(plateSetup)) {
    html <- c(html, "<tr>")
    for (j in 1:ncol(plateSetup)) {
      if (nchar(plateSetup[i,j]) > 8) {
        tmp <- strsplit(plateSetup[i,j], "")[[1]]
        beg <- paste(tmp[1:8], collapse="")
        end <- paste(tmp[9:length(tmp)], collapse="")
        html <- c(html, paste("<td>", beg, " ", end, "</td>", sep=""))
      } else {
        html <- c(html, paste("<td>", plateSetup[i,j], "</td>", sep=""))
      }
    }
    html <- c(html, "</tr>")
  }
  html <- c(html, "</table>", "<p class=\"caption\">Plate Setup</strong></p>", "</div>", "<hr class=\"clear-contentunit\" />")
  for (i in 1:nImages) {
    html <- c(html, "<div class=\"column1-unit\">")
    html <- c(html, paste("<h1>", titles[i], "</h1>", sep=""))
    html <- c(html, "<table>")
    html <- c(html, paste("<tr><td><img src=\"", plateId, "_", i, ".jpg", "\" height=\"450\" width=\"750\"></td></tr>", sep=""))
    html <- c(html, "</table>")
    html <- c(html, paste("<p class=\"caption\"><strong>", captions[i], "</strong></p>", sep=""))
    html <- c(html, "</div>")          
    html <- c(html, "<hr class=\"clear-contentunit\" />")
  } 
  conBottom <- file(bottomFile)
  html <- c(html, readLines(conBottom))
  close(conBottom)
  conOutputFile <- file(outputFile)
  cat(paste(html, collapse="\n"), file=conOutputFile, append=TRUE)
  close(conOutputFile)  
}


################################################################################
## Create HTML output for the plate list
plateList2html <- function(nPlates, outputFile, headerFile, bottomFile) {
  if (nPlates <= 5)
    nPlatesPerRow <- nPlates
  else
    nPlatesPerRow <- 5
  nRows <- nPlates %/% nPlatesPerRow
  nRowsColumns <-  nRows *  nPlatesPerRow
  nCellsLeft <- nPlates -  nRowsColumns
  html <- c()
  conHeader <- file(headerFile)
  html <- c(html, readLines(conHeader))
  close(conHeader)
  html <- c(html, "<h1 class=\"block\">Plate List</h1>", "<div class=\"column1-unit\">", "<table>")
  for (i in 1:nRows) {
    html <- c(html, "<tr>")
    for (j in 1:nPlatesPerRow) {
      num <- j + (i-1)*nPlatesPerRow
      plateName <- paste(paste(rep('0', 5-nchar(num)), collapse=""), num, sep="")
      html <- c(html, paste("<td>Plate <a href=\"./p", plateName, "/p", plateName, ".html\">",plateName,"</a></td>", sep=""))
    }
    html <- c(html, "</tr>")
  }
  if (nCellsLeft > 0) {
    html <- c(html, "<tr>")
    for (i in (1:nCellsLeft)) {
      num <- nRowsColumns + i
      plateName <- paste(paste(rep('0', 5-nchar(num)), collapse=""), num, sep="")
      html <- c(html, paste("<td>Plate <a href=\"./p", plateName, "/p", plateName, ".html\">", plateName,"</a></td>", sep=""))
    }
    if (nCellsLeft < nPlatesPerRow) {
      for (i in ((nCellsLeft+1):nPlatesPerRow)) {
        html <- c(html, paste("<td></td>"))  
      }
    }
    html <- c(html, "</tr>")
  }
  html <- c(html, "</table>", "<p class=\"caption\"><strong>List of Plates</strong></p>", "</div>", "<hr class=\"clear-contentunit\" />") 
  conBottom <- file(bottomFile)
  html <- c(html, readLines(conBottom))
  close(conBottom)
  conOutputFile <- file(outputFile)
  cat(paste(html, collapse="\n"), file=conOutputFile, append=TRUE)
  close(conOutputFile)  
}


################################################################################
## Screen Summary html file
################################################################################
## Create HTML output screen summary
screensummary2html <- function(outputFile, headerFile, bottomFile) {
  html <- c()
  conHeader <- file(headerFile)
  html <- c(html, readLines(conHeader))
  close(conHeader)
  nImages <- 6
  titles <- c("Predictive Accuracy per Plate", "Number of genes per plate with phenotypic effects higher than control (Count)")
  captions <- c("Predictive Accuracy per Plate", "Number of genes per plate with phenotypic effects higher than control (Count)")
  titles <- c(titles, "Number of genes per plate with phenotypic effects higher than control (Soft)")
  captions <- c(captions, "Number of genes per plate with phenotypic effects higher than control (Soft)")
  titles <- c(titles, "Number of genes per plate with phenotypic effects lower than control (Count)")
  captions <- c(captions, "Number of genes per plate with phenotypic effects lower than control")
  titles <- c(titles, "Number of genes per plate with phenotypic effects lower than control (Soft)")
  captions <- c(captions, "Number of genes per plate with phenotypic effects lower than control (Soft)")  
  titles <- c(titles, "Positive and negative toxicity control")
  captions <- c(captions, "Positive and negative toxicity control") 
  images <- c("predictive_acc.jpg", "positive_genes_pp.jpg", "positive_genes_pp_soft.jpg")
  images <- c(images, "negative_genes_pp.jpg", "negative_genes_pp_soft.jpg", "zfactor.jpg")
  html <- c(html, paste("<h1 class=\"block\">Screen Summary Plots</h1>"))
  for (i in 1:nImages) {
    html <- c(html, "<div class=\"column1-unit\">")
    html <- c(html, paste("<h1>", titles[i], "</h1>", sep=""))
    html <- c(html, "<table>")
    html <- c(html, paste("<tr><td><img src=\"", images[i], "\" height=\"450\" width=\"750\"></td></tr>", sep=""))
    html <- c(html, "</table>")
    html <- c(html, paste("<p class=\"caption\"><strong>", captions[i], "</strong></p>", sep=""))
    html <- c(html, "</div>")          
    html <- c(html, "<hr class=\"clear-contentunit\" />")
  } 
  conBottom <- file(bottomFile)
  html <- c(html, readLines(conBottom))
  close(conBottom)
  conOutputFile <- file(outputFile)
  cat(paste(html, collapse="\n"), file=conOutputFile, append=TRUE)
  close(conOutputFile)  
}


################################################################################
## Screen results html file
################################################################################
## Create HTML output screen summary
screenresults2html <- function(outputFile, highCount, lowCount, reportFilename, headerFile, bottomFile) {
  html <- c()
  conHeader <- file(headerFile)
  html <- c(html, readLines(conHeader))
  close(conHeader)
  html <- c(html, paste("<h1 class=\"block\">Screen Results</h1>"))
  html <- c(html, "<div class=\"column1-unit\">")
  html <- c(html, "<br />")
  html <- c(html, paste("<p>Please refer to this <a href=\"", reportFilename, ".pdf\" >", sep=""))
  html <- c(html, "document </a> for any question related to the mathematical formulation ")  
  html <- c(html, "used throughout the analysis pipeline.</p>")
  b_html <- "<p><a href=\"highTargets.html\">" 
  e_html <- "</a> Target genes whith higher phenotypic effects than the negative control are found."
  html <- c(html, paste(b_html, highCount, e_html, sep=""))
  txt1 <- "These genes can be retrieved in <a href=\"./results/high_targets_genes.csv\">"
  txt2 <- "csv </a> format with additional information</p>"
  html <- c(html, paste(txt1, txt2, sep=""))
  
  b_html <- "<p><a href=\"lowTargets.html\">" 
  e_html <- "</a> Target genes whith lower phenotypic effects than the negative control are found."
  txt1 <- "These genes can be retrieved in <a href=\"./results/low_targets_genes.csv\">"
  txt2 <- "csv </a> format with additional information</p>"
  html <- c(html, paste(b_html, lowCount, e_html, sep=""))
  html <- c(html, paste(txt1, txt2, sep="")) 
  html <- c(html, "<p>The <a href=\"./results/raw_results.csv\">raw results</a> are available for further investigation.")
  html <- c(html, "Here is a short description of the various fields available in the raw results file</p>")
  html <- c(html, "<p><b>Gene</b> - The name of the gene</p>")
  html <- c(html, "<p><b>fisher-fdr</b> - The FDR value of the Fisher exact test</p>")
  html <- c(html, "<p><b>rel-riskValue</b> - The relative risk value using the counts of positive and negative cells</p>")
  html <- c(html, "<p><b>rel-risk-fdr</b> - The FDR of the relative risk </p>")
  html <- c(html, "<p><b>rel-risk-fdr</b> - The FDR of the relative risk </p>")
  html <- c(html, "<p><b>odds-ratioValue</b> - The odds ratio using the counts of positive and negative cells </p>")
  html <- c(html, "<p><b>odds-ratio-fdr</b> - The FDR values for the the odds-ratio </p>")
  html <- c(html, "<p><b>prValue</b> - The probability for a condition to be positive </p>")
  html <- c(html, "<p><b>rel-probMM</b> - The soft relative risk using the estimated probability values by the method of moments</p>")
  html <- c(html, "<p><b>rel-probMM-fdr</b> - The FDR values for the soft relative risk </p>")
  html <- c(html, "<p><b>prob-oddsRatioMM</b> - The odds ratio values based on the estimated probMM values </p>")
  html <- c(html, "<p><b>prob-oddsRatioMM-fdr</b> - The FDR values for soft odds ratio values </p>")
  html <- c(html, "<p><b>Viavility</b> - Proximity value to the positive toxicity control </p>")
  html <- c(html, "<p><b>Zfactor</b> - The Z-factor value calculated using the positive and the negative toxicity controls </p>")
  html <- c(html, "<p><b>Column</b> -  The data column name used in the analysis</p>")
  html <- c(html, "<p><b>PlateName</b> - Name of plate related to the data </p>")
  conBottom <- file(bottomFile)
  html <- c(html, readLines(conBottom))
  close(conBottom)
  conOutputFile <- file(outputFile)
  cat(paste(html, collapse="\n"), file=conOutputFile, append=TRUE)
  close(conOutputFile)  
}



my_stem <- function(x,y,pch=16,linecol=1,clinecol=1,...) {
  if (missing(y)){
    y = x
    x = 1:length(x) }
  plot(x,y,pch=pch,...)
  for (i in 1:length(x)){
    lines(c(x[i],x[i]), c(0,y[i]),col=linecol)
  }
  lines(c(x[1]-2,x[length(x)]+2), c(0,0),col=clinecol)
}

plotPredictiveAcc <- function(values, fname, xlabel, ylabel) {
  #pdf(file=fname, width=wd, height=ht);
  jpeg(file=fname, width=1728, height=650, res=150, quality=100);
  my_stem(c(1:length(values)), values, pch=15, col="darkred", xlab=xlabel, ylab=ylabel)
  dev.off()
}


plotTargetGenePerPlate <- function(values, fname, xlabel, ylabel) {
  #pdf(file=fname, width=wd, height=ht);
  jpeg(file=fname, width=1728, height=650, res=150, quality=100);
  my_stem(c(1:length(values)), values, col="darkred", xlab=xlabel, ylab=ylabel)
  dev.off()
}


################################################################################
## Create HTML output for the target gene list
targetList2html <- function(outputFile, targetTable, targetTitle, headerFile, bottomFile) {
  columns <- c('Gene', 'rel-probMM', 'rel-probMM-fdr', 'viability', 'zfactor', 'column', 'plateName')
  nRows <- nrow(targetTable)
  html <- c()
  conHeader <- file(headerFile)
  html <- c(html, readLines(conHeader))
  close(conHeader)
  html <- c(html, paste("<h1 class=\"block\">", targetTitle, "</h1>",sep=""), "<div class=\"column1-unit\">", "<table>")
  html <- c(html, "<tr>")
  html <- c(html, paste("<th>", "Gene Name", "</th>", sep=""))
  html <- c(html, paste("<th>", "Relative Risk", "</th>", sep=""))
  html <- c(html, paste("<th>", "Relative Risk FDR", "</th>", sep=""))
  html <- c(html, paste("<th>", "Viability Score", "</th>", sep=""))
  html <- c(html, paste("<th>", "Zfactor", "</th>", sep=""))
  html <- c(html, paste("<th>", "Column Name", "</th>", sep=""))
  html <- c(html, paste("<th>", "Plate Name", "</th>", sep=""))
  html <- c(html, "</tr>")
  for (i in 1:nRows) {
    html <- c(html, "<tr>")
    for (c in columns) {
      if ((c!='Gene') & (c!='column') & (c!='plateName'))
        html <- c(html, paste("<td>", sprintf("%.7f",targetTable[i, c]), "</td>", sep=""))
      else
        html <- c(html, paste("<td>", targetTable[i, c], "</td>", sep=""))
    }
    html <- c(html, "</tr>")
  }
  html <- c(html, "</table>", paste("<p class=\"caption\"><strong>", targetTitle, "</strong></p>", sep=""), "</div>", "<hr class=\"clear-contentunit\" />") 
  conBottom <- file(bottomFile)
  html <- c(html, readLines(conBottom))
  close(conBottom)
  conOutputFile <- file(outputFile)
  cat(paste(html, collapse="\n"), file=conOutputFile, append=TRUE)
  close(conOutputFile)  
}


getPCAProbData <- function(pcaData, logisticModel) {
  nbOfGenes <- length(names(pcaData))
  for (i in 1:nbOfGenes) {
    xx <- predict(logisticModel,  newdata=pcaData[[i]], type="response")
    pcaData[[i]] <- data.frame(Comp=as.vector(xx), CellIds=rep(NA, length(xx)))
  } 
  return(pcaData)
}
