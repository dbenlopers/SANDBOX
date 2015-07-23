######################
### import library ###
######################

suppressMessages(library(fields))


#################
### functions ###
#################

PlateFit=function(x, Y, Y.mean, lambda=3.5, nx=80, ny=80){
  
  Y=as.numeric(Y)
  Y.mean=as.numeric(Y.mean)
  y=Y-Y.mean # y: spatial noise
  
  out=Krig(x=x, Y=y, cov.function="stationary.cov", lambda=lambda)
  surface=predictSurface(out, nx=nx, ny=ny)
  fit.1=as.numeric(out$residuals)
  
  Y.fit=fit.1+Y.mean # Y.fit: spatial noise free value
  
  rgb.palette <- colorRampPalette(c("green","black","red"), space = "rgb")

  Y.len=length(Y)
  color.code.Y=Y - min(Y)
  color.code.Y=color.code.Y/max(color.code.Y)
  color.code.Y=floor(color.code.Y*(Y.len - 1))+1
  color.code.Y=rgb.palette(Y.len)[color.code.Y]
  
  color.code.Y.fit=Y.fit - min(Y.fit)
  color.code.Y.fit=color.code.Y.fit/max(color.code.Y.fit)
  color.code.Y.fit=floor(color.code.Y.fit*(Y.len - 1))+1
  color.code.Y.fit=rgb.palette(Y.len)[color.code.Y.fit]
  
  y.len=length(y)
  color.code.y=y - min(y)  
  color.code.y=color.code.y/max(color.code.y)  
  color.code.y=floor(color.code.y*(y.len - 1))+1
  color.code.y=rgb.palette(y.len)[color.code.y]  
  
  return(list(x=x, Y=Y, Y.fit=Y.fit, y=y, surface=surface,color.code.Y=color.code.Y, 
              color.code.y=color.code.y, color.code.Y.fit=color.code.Y.fit))
}

PlotPlate= function(object, x.axis=NULL, y.axis=NULL, cex=10, cex.axis=1,
                    xlab="", ylab="", cex.lab=1.5, main=NULL, type="raw"){
  loc=object$x
  Y=object$Y
  y=object$y
  Y.fit=object$Y.fit
  color.code.y=object$color.code.y
  color.code.Y=object$color.code.Y
  color.code.Y.fit=object$color.code.Y.fit
  cn=length(unique(loc[, 1]))
  rn=length(unique(loc[, 2]))
  rgb.palette <- colorRampPalette(c("green","black","red"), space = "rgb")
  par(mar=c(5, 5, 1, 1))
  plot(c(0.5,cn+0.5), c(0.5,rn+0.5), type="n", xlab=xlab, ylab=ylab,
       xaxt="n", yaxt="n", cex.lab=cex.lab,  main=main)
  points(loc[, 1], loc[, 2], col=color.code.Y, pch=20, cex=cex)
  if(type  == "noise"){
    points(loc[, 1], loc[, 2], col=color.code.y, pch=20, cex=cex)
  }else if(type == "fitted"){
    points(loc[, 1], loc[, 2], col=color.code.Y.fit, pch=20, cex=cex)
  }else{
    points(loc[, 1], loc[, 2], col=color.code.Y, pch=20, cex=cex)
  }
  if(!is.null(x.axis)){
    axis(1, at=1:cn, lab=x.axis, cex.axis=cex.axis)
  }
  if(!is.null(y.axis)){
    axis(2, at=1:rn, lab=y.axis, cex.axis=cex.axis)
  }
}

PlotSurface = function(object, x.axis=NULL, y.axis=NULL, cex=9, cex.axis=1,
                       xlab="", ylab="", cex.lab=1.5, main=NULL  ){
  loc=object$x
  cn=length(unique(loc[, 1]))
  rn=length(unique(loc[, 2]))
  surface=object$surface
  par(mar=c(5, 7, 1, 5))
  plot.surface(surface, xlab=xlab, ylab=ylab, cex.axis=cex.axis, xaxt="n", yaxt="n", cex.lab=cex.lab,  main=main)
  if(!is.null(x.axis)){
    axis(1, at=1:cn, lab=x.axis)
  }
  if(!is.null(y.axis)){
    axis(2, at=1:rn, lab=y.axis)
  } 
}

heatmap.legend <- function(x, cex.axis=2)
{
  par(mar=c(1,1,1,6))
  ix <- 1
  nlevel=16
  minz <- min(x)
  maxz <- max(x)
  binwidth <- (maxz - minz)/nlevel
  midpoints <- seq(minz + binwidth/2, maxz - binwidth/2, by = binwidth)
  iy <- midpoints
  iz <- matrix(iy, nrow = 1, ncol = length(iy))
  rgb.palette <- colorRampPalette(c("green","black","red"), 
                                  space = "rgb")
  image(ix, iy, iz, xaxt = "n", yaxt = "n", xlab = "", 
        ylab = "", col = rgb.palette(16))
  axis(4, mgp = c(3, 1, 0), las = 2, cex.axis=cex.axis)
}

DateCheck=function(x){
  x=as.character(x)
  y=as.integer(substr(x, 1, 4))
  m=as.integer(substr(x, 5, 6))
  d=as.integer(substr(x, 7, 8))
  x=strsplit(x, split="")[[1]]
  if(length(x) != 8){
    return(FALSE)
  }else if(m < 1 | m > 12){
    return(FALSE)
  }else if(d <1 | d > 31){
    return(FALSE)
  }else{
    return(TRUE)
  }
}

WellCheck=function(x){
  x=as.character(x)
  raw.num=substr(x, 1, 1)
  col.num=as.integer(substr(x, 2, 3))
  x=strsplit(x, split="")[[1]]
  if(length(x) != 3){
    return(FALSE)
  }else if(!(raw.num %in% LETTERS)){
    return(FALSE)
  }else if(col.num < 1 | col.num > 24){
    return(FALSE)
  }else{
    return(TRUE)
  }
}

WellToLoc=function(WellNo){
  WellNo=as.character(WellNo)
  y.label=rev(sort(unique(substr(WellNo, 1, 1))))
  x.label=sort(unique(as.integer(substr(WellNo, 2, 3))))
  row.num=substr(WellNo, 1, 1)
  row.num=match(row.num, LETTERS)
  row.num=max(row.num)-row.num+1
  col.num=as.integer(substr(WellNo, 2, 3))
  col.num=col.num-min(col.num)+1
  loc=cbind(col.num, row.num)
  return(list(loc=loc, x.label=x.label, y.label=y.label))
}

OutlierDetect=function(y){
  y=as.numeric(y)
  y.max=median(y)+10*mad(y)
  y.min=median(y)-10*mad(y)
  if(sum(y > y.max | y < y.min) > 0){
    print("Outliers detected and modified (median plus or minus 6 times median absolute deviation)")
  }
  y[y > y.max]=y.max
  y[y < y.min]=y.min
  return(y)
}

PlateAnalysis=function(WellNo, RawDat, PlateNo){
  WellInfo=WellToLoc(WellNo)
  loc=WellInfo$loc
  x.label=WellInfo$x.label
  y.label=WellInfo$y.label
  NewDat=RawDat
  
  for(i in 1:ncol(NewDat)){
    NewDat[, i]=OutlierDetect(NewDat[, i])
  }
  
  raw.mean=apply(NewDat, 1, mean)
  for(i in 1:ncol(NewDat)){
    
    fit.1=PlateFit(loc, NewDat[, i], raw.mean)
    NewDat[, i]=fit.1$Y.fit
    PlateNum=paste(PlateNo, "replicate ", i, sep="_")
    
    
    jpeg(file=paste(PlateNum, "spatial_noise.jpeg", sep="_"), width=800, height=600)
    PlotPlate(fit.1, xlab="Col", ylab="Row", cex.lab=2, cex=15,
              x.axis=x.label, y.axis=y.label, cex.axis=1.5, type="noise")
    dev.off()

    jpeg(file=paste(PlateNum, "raw_data.jpeg", sep="_"), width=800, height=600)
    PlotPlate(fit.1, xlab="Col", ylab="Row", cex.lab=2, cex=15,
              x.axis=x.label, y.axis=y.label, cex.axis=1.5, type="raw")
    dev.off()
    
    jpeg(file=paste(PlateNum, "fitted_spatial_noise.jpeg", sep="_"), width=800, height=600)
    PlotSurface(fit.1, xlab="Col", ylab="Row", cex.lab=2,
                x.axis=x.label, y.axis=y.label, cex.axis=2)
    dev.off()
    
  }
  return(NewDat)
}

################
### Analysis ###
################

### data input ###

spatial.data=read.csv("/home/akopp/Bureau/SbacHTS/data.csv", header=T)
plate.date=spatial.data[, 1]
plate.number=spatial.data[, 2]
well.number=spatial.data[, 3]
raw.data=spatial.data[, 4:ncol(spatial.data)]

### data checking ###

if(sum(!apply(data.frame(plate.date), 1, DateCheck)) > 0){
  print("Date format is inappropriate!")
  quit()
}
if(sum(!apply(data.frame(well.number), 1, WellCheck)) > 0){
  print("Well number format is inappropriate!")
  quit()
}
if(sum(is.na(plate.number)) > 0){
  print("Missing value in plate number!")
  quit()
}
if(ncol(raw.data) < 2){
  print("Repliate data is needed!")
  quit()
}
if(sum(is.na(raw.data)) > 0){
  print("Missing value in experimental data!")
  quit()
}

### data analysis ###

PlateNo=plate.number[1]
WellNo=well.number[plate.number ==  PlateNo]
RawDat=raw.data[plate.number == PlateNo, ]

NewDat=PlateAnalysis(WellNo, RawDat, PlateNo)

new.data=raw.data
plate.number.unique=unique(plate.number)

for(i in 1:length(plate.number.unique)){
  PlateNo=plate.number.unique[i]
  print(paste(PlateNo, "Analyzing ...", sep=' '))
  WellNo=well.number[plate.number ==  PlateNo]
  RawDat=raw.data[plate.number == PlateNo, ]
  NewDat=PlateAnalysis(WellNo, RawDat, PlateNo)
  new.data[plate.number ==  PlateNo, ]=NewDat
}

output.new=cbind(plate.date, plate.number, well.number, new.data)
write.csv(output.new, "Corrected_Raw_Data.csv")

plate.col=aggregate(plate.date, by=list(plate.number), FUN=mean)[, 2]
ave=apply(new.data, 1, mean, na.rm=T)
par(mar=c(5, 8, 1, 1))
jpeg("Batch_effect.jpeg", width=1000, height=600)
boxplot(ave ~ plate.number, col=plate.col, cex.axis=1,
        xlab="Plate Number", ylab="Experimental Readout",cex.lab=1.5,)
dev.off()
