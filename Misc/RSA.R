#!/usr/bin/env Rscript

options("width"=250)
# R Users:
# --------
#   Usage of RSA.R:
#   ===============
#     --l: lower_bound, defaults to 0
#     --u: upper bound, defaults to 1
#     --r: reverse hit picking, the higher the score the better
#          if -r flag is off, the lower the score the better
#     --i: input file name
#     --o: output file name, STDOUT if not specified
#     -b:  turn on Bonferroni correction, conceptually useful
#          when there are different number of siRNAs per gene.

# Input and Output Format:
# ========================
#   Gene_ID,Well_ID,Score: columns from input spreadsheet
#   LogP: OPI p-value in log10, i.e., -2 means 0.01;
#   OPI_Hit: whether the well is a hit, 1 means yes, 0 means no;
#   #hitWell: number of hit wells for the gene
#   #totalWell: total number of wells for the gene
#     if gene A has three wells w1, w2 and w3, and w1 and w2 are hits,
#     #totalWell should be 3, #hitWell should be 2, w1 and w2 should have OPI_Hit set as 1
#     and w3 should have OPI_Hit set as 0.
#   OPI_Rank: ranking column to sort all wells for hit picking
#   Cutoff_Rank: ranking column to sort all wells based on Score in the simple activity-based method
#
#   Note: a rank value of 999999 means the well is not a hit. We put a large rank number here
#   for the convenient of spreadsheet sorting.
#
#   Examples A in output.csv:
#   -------------------------
#   1221200,7_O20,0.0541,-6.810,1,3,3,1,33
#   1221200,18_A21,0.0626,-6.810,1,3,3,2,43
#   1221200,41_A21,0.0765,-6.810,1,3,3,3,72
#
#   Gene ID 1221200 has three wells, 7_O20, 18_A21 and 41_A21. All show good scores.
#   Therefore 3 out of 3 wells are hits (#totalWell=3, #hitWell=3, OPI_Hit=1 for all three wells)
#   LogP is -6.810. These three wells are ranked as the best three wells by OPI.
#   However, they are ranked as the 33th, 43th and 73th well by the traditional cutoff method.
#
#   Examples B in output.csv:
#   -------------------------
#   3620,21_I17,0.0537,-2.344,1,1,2,162,31
#   3620,44_I17,0.7335,-2.344,0,1,2,999999,4113
#
#   Gene ID 3620 has two wells, 21_I17 is active, while 44_I17 is relative inactive.
#   OPI decides that only 1 out of the 2 wells is a hit. Therefore one well has OPI_Hit set as 1,
#   and the other 0. #totalWell=2, but #hitWell=1.
#   The first well is the 162th hit by OPI, 31th by cutoff method.
#   The second well is not a hit by OPI, 4113th by cutoff method.

handleOneGroup <- function(i,dataset, optsb, t.rank = NULL)
{
	## how many of them are up or low than cut-off.
	if(optsb$reverse)
	{
  		i_max = sum(dataset$Score[i]>=optsb$LB, na.rm=TRUE)
  		i_min = max(1,sum(dataset$Score[i]>=optsb$UB, na.rm=TRUE), na.rm=TRUE)
	}else
	{
  		i_max = sum(dataset$Score[i]<=optsb$UB, na.rm=TRUE)
  		i_min = max(1,sum(dataset$Score[i]<=optsb$LB, na.rm=TRUE), na.rm=TRUE)
	}
	## t.r is the true rank, instead of order.
    if (is.null(t.rank))
    {
	t.r = i
    } else {
        t.r = t.rank[i]
    }
	r = OPIScore(t.r,nrow(dataset),i_min,i_max,optsb$bonferroni)
	return ( cbind(
  				LogP = r["logp"]
				,OPI_Hit=as.numeric(seq(length(i))<=r["cutoff"])
  				,"#hitWell"=i_max
				,"#totalWell"=length(i)
				,rank = i))
}

OPIScore <- function(I_rank, N, i_min=1, i_max=-1, bonferroni=FALSE)
{
	n_drawn = length(I_rank) # number of black
	if(i_max == -1)
	{
    	i_max=n_drawn
	}
	r1 = c(logp=1.0,cutoff=0)
	if( i_max < i_min) return (r1)
	# phyper(x, lower.tail = F), x = x-1, when lower.tail = F
        best_logp=1.0
        cutoff=0
        for (i in i_min:i_max) {
            if (i<i_max && I_rank[i]==I_rank[i+1]) { next; }
            logp=phyper(i-1,I_rank[i],N-I_rank[i], n_drawn,lower.tail = F,log.p=T)
            logp = max(logp/log(10), -100)
            if (logp<=best_logp) {
                best_logp=logp
                cutoff=i
            }
        }
        if (bonferroni) {
            best_logp=best_logp+log(i_max-i_min+1)/log(10)
        }
        return (c(logp=best_logp, cutoff=cutoff))
}

## Changed Here.
OPI<-function(Groups,Scores,opts,Data=NULL)
{
	t = data.frame(cbind(Gene_ID = Groups, Score= Scores))
	Sorted_Order = order(t$Score,decreasing=opts$reverse);
	Data = Data[Sorted_Order,]
	t = t[Sorted_Order,]

	## get the ranks, "max" for the tie.
	t.rank <- rank(t$Score, ties.method="max")
	t = do.call("rbind", tapply(seq(nrow(t)), list(t$Gene_ID), handleOneGroup, dataset = t, opts, t.rank))
	t = cbind(Data, t[order(t[,"rank"]),])

	# add OPI_Rank
	t = t[order(t$LogP,t$Score*ifelse(opts$reverse,-1,1)),]
	t$OPI_Rank = cumsum(t$OPI_Hit)
	t$OPI_Rank[t$OPI_Hit == 0] = 999999

	# add Cutoff_Rank
	t = t[order(t$Score*(ifelse(opts$reverse,-1,1)),t$LogP),]

	if(opts$reverse){tmp = t$Score>=opts$LB} else {tmp = t$Score<=opts$UB}
	t$Cutoff_Rank = cumsum(tmp)
	t$Cutoff_Rank[!tmp] = 999999

	# add EXP_Rank
	t$EXP_Rank = pmin(t$OPI_Rank,t$Cutoff_Rank)
        t$EXP_Rank = pmin(t$OPI_Rank,t$Cutoff_Rank)
        if(opts$reverse) {
                return(t[order(t$OPI_Rank, -t$Score),])
        } else {
                return(t[order(t$OPI_Rank, t$Score),])
        }
}

opts = list(LB=0,
			UB=1,
			outputFile=NA,
			inputFile="/home/akopp/Documents/Crispr_DATA/CountTable/CountTable_Sum_Fold.csv",
			reverse=FALSE,
			bonferroni=TRUE)

df = read.csv(opts$inputFile);
colNames = dimnames(t)[[2]]

Gene_ID <- "Gene"
Well_ID <- "GeneID"
Score <- "FoldChange_34.56_NMR"

if(!( (Gene_ID %in% colNames) & (Well_ID %in% colNames) &(Score %in% colNames)))
{
	warnings(" not colname")
	return(NA)
}
#filter out bad record
df = subset(df, !is.na(Gene_ID) & Gene_ID != "" & !is.na(Score) & !is.finite(Score))

t = df[c(Gene_ID, Well_ID, Score)]
colnames(t) <- c("Gene_ID", "Well_ID", "Score")

r = OPI(t$Gene_ID,t$Score,opts,t)

DF <- cbind(df[row.names(r),], r)

#output result
if(is.na(opts$outputFile))
{
    print(head(DF,50))
}else
{
	write.csv(DF,opts$outputFile,row.names = FALSE,quote = FALSE)
}

print(paste("Total #Genes = ", length(unique(r$Gene_ID)), collapse=""));
print(paste("Total #data = ", nrow(r), collapse=""));
