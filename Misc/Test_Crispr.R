source("/home/akopp/PROJECT/SandBox/Misc/binom.R")
source("/home/akopp/PROJECT/SandBox/Misc/RRA.R")


df = read.csv("/home/akopp/Documents/Crispr_DATA/CountTable/CountTable_Sum_Fold.csv")

Neg = "LTBN_34_NormMappedRead"
Pos = "LTBN_56_NormMappedRead"

pvalue = binomTest(df[Neg], df[Pos])
df <- cbind(df, pvalue)

print(head(df))

out <- split(df$pvalue, f=df$Gene)
rra <- aggregateRanks(glist=out, N=length(out))
