## Code for reading TCA data presented in CSV file
## Reading a directory given in argument, this directory must contains data from each plate and replicate
## and one plate setup file in csv
## Multi process version
## Author = KOPP Arnaud

if (! suppressPackageStartupMessages(require(foreach)))
  stop("Require foreach package")
if (! suppressPackageStartupMessages(require(doMC)))
  stop("Require doMC package")
if (! suppressPackageStartupMessages(require(data.table)))
  stop("Require data.table package")

readCSVDir_unop <- function(CsvDir, outputdir, redo, refSamp, refThr, colAnalyze, nb.process){
  ## read TCA data (at cell resolution) from all csv file of given directory
  ## data into CellTCA
  ## write data into .RData to outputdir

  
  if(is.na(CsvDir)) {
    stop("Invalid path")
  }
  if(!file.exists(outputdir)) {
    dir.create(file.path(outputdir))
  } 
  
  
  spnames <- dir(pattern="Rep", path=CsvDir, ignore.case=TRUE) #data file
  ppnames <- dir(pattern="PP", path=CsvDir, ignore.case=TRUE) #platesetup file
  #searchINF <- regexpr("INF",spnames)
  searchSUP <- regexpr("SUP",spnames)
  searchREP <- regexpr("rep", spnames)
  searchPP <- regexpr("PP", ppnames)
  replTy <- factor(substr(spnames,1,2+apply(cbind(searchREP,searchSUP),1,max))) #ensemble de replica de plaque
  ppTy <- factor(substr(ppnames,1,2+apply(cbind(searchPP,searchSUP),1,max))) #PP (PlanPlaque)
  mywarning <- character(0)
  outList <- list()
  
  #setup parallel backend to use X processors
  registerDoMC(nb.process) #change the X to your number of CPU cores
  
  ## the different types of plates
  foreach(i = 1:length(levels(replTy))) %dopar% {               
    if(!(redo == F & paste("CellTCA_", gsub(" ","",levels(replTy)[i]),".RData", sep="") %in% dir(path=outputdir))) {
      RepList <- list()
      replicateLst <- list()
      metaInfoLst <- list()
      infoLst <- list()
      plateSetupLst <- list()
      dataLst <- list()
      ppl.exist <- T
      dataValid <- T
      PlateFormat <- NULL
      l <- 0
      
      ppnum <- i
      ## reading plate setup for each type of plate
      pp.path.file <- ppnames[ppnum] 
      file.path <- paste(CsvDir,pp.path.file, sep="/")
      cat(paste("Opening file : ", file.path,"\n"))
      outList$plateSetup <- read.csv(file = file.path, header = TRUE, check.names=FALSE)
      PlateFormat <- nrow(outList$plateSetup)*(ncol(outList$plateSetup)-1)
      if(PlateFormat == 384) {
        dat.PlateSetup <- as.matrix(outList$plateSetup[1:16,2:25])
        colnames(dat.PlateSetup) <- 1:24
        rownames(dat.PlateSetup) <- LETTERS[1:16]
        ppl.exist <- T
      } else {
        if(PlateFormat == 96) {
          dat.PlateSetup <- as.matrix(outList$plateSetup[1:8,2:13])
          colnames(dat.PlateSetup) <- 1:12
          rownames(dat.PlateSetup) <- LETTERS[1:8]
          ppl.exist <- T
        }
        else {
          dat.PlateSetup <- matrix("Missing")
          PlateFormat <- NA
          ppl.exist <- F
        }
      }
      
      if(ppl.exist==T) {
        outList$PlateSetup <- dat.PlateSetup
      }
      
      
      
      ## the replicate of same plate
      mywarnings <- NULL
      dataValid <- T
      plateType <- factor(substr(spnames,1,2+apply(cbind(searchREP,searchSUP),1,max))) 
      for(j in which(replTy == levels(replTy)[i])) {   ##parcours de chaque replicat/fichier
        l <- l+1
        tmpDir <- spnames[j]
        in.pathFile <- tmpDir
        file.path <- paste(CsvDir,in.pathFile, sep="/")
        cat(paste("Opening file : ", file.path, "\n"))
        outList$Data <- read.csv(file = file.path, header =TRUE, stringsAsFactors=F, dec=".")
        #outList$Data <- as.data.frame(fread(file.path, header =TRUE, stringsAsFactors=F))
        outList$colnames <- colnames(outList$Data)
        outList$nrow <- nrow(outList$Data)
        outList$MetaInfo <- c(file=file.path,platetype=plateType,PlateFormat=PlateFormat, plateSetupDefined=ppl.exist,analyze=colAnalyze,refSamp=refSamp,
                              refThreshold=refThr, date=as.character(Sys.time()))
        
        ## convert to class CellTCA
        infoLst[[l]] <- new("TCADataInfo", info=c(outList$MetaInfo["file"],outList$MetaInfo["date"]))
        metaInfoLst[[l]] <- new("TCAMetaInfo", metaInfo=outList$MetaInfo)
        plateSetupLst[[l]] <- new("TCAPlateSetup", plateSetup=outList$PlateSetup)
        colsToAnalyze <- colAnalyze
        
        ColsName <- colnames(outList$Data)
        for ( j in 1:length(colsToAnalyze)) {
          if ( !colsToAnalyze[j] %in% ColsName) {
            cat("\nColumn not found, choose other :\n\n")
            print(ColsName)
            cat("\n")
            stop()
          }
        }
        
        if (length(colsToAnalyze) == 0) {
          mywarnings <- c(mywarnings, "No column found for analysis")
          print("No column found for analysis")
          dataValid <- FALSE
        } else {
          if (is.na(refSamp)) {
            mywarnings <- c(mywarnings, "No reference sample found")
            print("No reference sample found")
            dataValid <- FALSE
          } else {
            if(outList$MetaInfo["plateSetupDefined"]==TRUE) {
              genes <- getGenes(plateSetupLst[[l]])
              datatmp <- outList$Data
              wellIds <- datatmp$Well
              ## selection des columns
              datatmp <- datatmp[c("Well", colAnalyze)]
              ## Nommage des columns
              names(datatmp) <- c("wellIds", colAnalyze)

              datatmp$GeneName <- genes[match(datatmp$wellIds,genes[,1]),2]
              dataLst[[l]] <- new("TCAData", data=datatmp)
              replicateLst[[l]] <- new("TCAReplicate", data=dataLst[[l]], plateSetup=plateSetupLst[[l]], info=infoLst[[l]])
            } else {
              mywarnings <- c(mywarnings, "No plate setup found")
              print("No plate setup found")
              dataValid <- FALSE
            }
          }
        }
        if (dataValid) {
          names(replicateLst) <- paste("repl",1:length(replicateLst),sep="_")
          ## Check for consistencies
          if (l > 1) {
            for (j in 2:l) {
              mywarnings <- c(mywarnings, checkMetaInfo(metaInfoLst[[1]], metaInfoLst[[j]]))
            }
          }
          cellTCA <- new("CellTCA", metaInfo=metaInfoLst[[1]], replicates=replicateLst)     
          save(cellTCA, file=paste(outputdir,"/CellTCA_",gsub(" ","",levels(replTy)[i]),".RData",sep=""))
          cat(paste("writing file  CellTCA_",gsub(" ","",levels(replTy)[i]),".RData \n",sep="") )
          if (length(mywarnings) > 0) {
            cat(paste("Warning : ", mywarnings, collapse="\n"))
          }
        } 
      }
    }
  }
}



readCSVDir <- compiler::cmpfun(readCSVDir_unop)


