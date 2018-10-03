#!/usr/bin/env python3
# coding=utf-8

import pandas as pd
import numpy as np

pd.set_option('display.max_rows',75)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 500)

DF = pd.read_csv("/home/akopp/Documents/Crispr_DATA/CountTable/CNT.csv")

lst = ["LTBN1_MappedRead","LTBN2_MappedRead","LTBN3_MappedRead",
        "LTBN4_MappedRead","LTBN5_MappedRead","LTBN6_MappedRead"]
lstNorm = [chan+"_MedianNorm" for chan in lst]

## Read count normalization by mageck method (median ratio method)
for chan in lst:
    tmp = DF.loc[:, chan]/DF.loc[:, lst].median(axis=1)
    DF.loc[:, chan+"_MedianNorm"] = DF.loc[:, chan] / tmp.median()

print(DF.iloc[:, 2:8].head())
print(DF.iloc[:, 8:].head())
print(DF.iloc[:, 2:].sum())

def estimateSizeFactorsForMatrix(counts):
    loggeomeans  = np.log(counts).mean(axis=1)

    counts.apply(lambda  x: np.log(x) - loggeomeans, axis=1)

# estimateSizeFactorsForMatrix <- function( counts, locfunc = median )
# {
#    loggeomeans <- rowMeans( log(counts) )
#    apply( counts, 2, function(cnts)
#       exp( locfunc( ( log(cnts) - loggeomeans )[ is.finite(loggeomeans) ] ) ) )
# }
