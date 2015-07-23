#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import os
import fnmatch

path = "/home/arnaud/Desktop/xavier_g/test/"
dataframe = None

for file in os.listdir(path):
    if fnmatch.fnmatch(file, '*.csv'):
        df = pd.read_csv(os.path.join(path, file), index_col=0)
        df = df.transpose()
        df.index = [str(file[0:-4])]
        if dataframe is None:
            dataframe = df
        else:
            dataframe = pd.concat([dataframe, df], axis=0)

dataframe.to_csv(os.path.join(path, 'Final_Output.csv'))
