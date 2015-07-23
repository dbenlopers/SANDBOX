## Script for making association file geneID <-> GO id 
## Arnaud KOPP, all right reserved.

start.time <- Sys.time()

options("width"=180)

if (! require(biomaRt))
  stop("biomaRt library is required to go any further.")

## search ensemble gene id with mirbase_id
ensembl = useMart("ensembl")
ensembl <- useDataset("hsapiens_gene_ensembl", mart = ensembl)

miRNA <- getBM(c("mirbase_id", "go_id"), values = list(TRUE), mart = ensembl)
entrez <- getBM(c("entrezgene", "go_id"), values = list(TRUE), mart = ensembl)
ensemble <- getBM(c("ensembl_gene_id", "go_id"), values = list(TRUE), mart = ensembl)

miRNA <- na.omit(miRNA)
entrez <- na.omit(entrez)
ensemble <- na.omit(ensemble)

end.time <- Sys.time()
time.taken <- end.time - start.time
print(time.taken)
