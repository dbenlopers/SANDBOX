# coding=utf-8
"""
The rank product is a biologically motivated test for the detection of differentially expressed genes
http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy.stats.rankdata.html
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


import pandas as pd
from scipy.stats import rankdata
import numpy as np

pd.set_option('display.max_rows',75)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 1000)

DF = pd.read_csv("/home/akopp/Documents/Crispr_DATA/CountTable/CountTable_Sum_Fold.csv")
Col = "FoldChange_34/56_NMR"

DF[Col+"_Ranked"] = DF.loc[:, Col].rank()
print(DF.head())

gb = DF.groupby(by="Gene")

Mean = gb.mean().loc[:,Col+"_Ranked"]
Std = gb.std().loc[:,Col+"_Ranked"]

x = pd.DataFrame(Mean.copy())
x.columns=["Gene Ranking Mean"]
y = pd.DataFrame(Std.copy())
y.columns=["Gene Ranking Std"]

z = pd.merge(x, y, left_index=True, right_index=True, how='outer').sort_values(by="Gene Ranking Mean")
print(z.head())
