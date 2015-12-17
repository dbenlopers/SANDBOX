#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import scipy.stats
import numpy as np

pd.set_option('display.max_rows', 60)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True, precision=4)


def test(file):
    df = pd.read_csv(file, index_col=0)
    df = df*100
    df['ks'] = 0
    df['p'] = 0
    for i in range(len(df)):
        cs = scipy.stats.ks_2samp(df.iloc[i,:].values, df.iloc[0,:].values)
        #cs = scipy.stats.ks_2samp(df.iloc[i,:].values, scipy.stats.norm.rvs(size=25, loc=50, scale=1))
        df.iloc[i, 20] = cs[0]
        df.iloc[i, 21] = cs[1]
        print(scipy.stats.chisquare(f_obs=df.iloc[i,:].tolist(), f_exp=df.iloc[0,:].tolist()))
    print(df)
    #df.to_csv()

#test('/home/arnaud/Desktop/spotcount.csv')
test('/home/arnaud/Desktop/spotarea.csv')
