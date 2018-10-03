#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import numpy as np
pd.set_option('display.max_rows',75)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1000)



from numpy import mean, absolute

def mad(data, axis=None):
    return mean(absolute(data - mean(data, axis)), axis)


def without_outlier_mad_based(data, thresh=2):
    """
    Based on mad, determine outliers by row
    :param data:
    :param thresh:
    :return: true for 'correct' value, false for outlier
    """
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(data, pd.DataFrame):
        data = data.values
    or_shape = data.shape
    data = data.flatten()
    if len(data.shape) == 1:
        data = data[:, None]
    median = np.median(data, axis=0)
    diff = np.sum((data - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    # med_abs_deviation = mad(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    modified_z_score = modified_z_score.reshape(or_shape)
    return modified_z_score < thresh


def without_outlier_std_based(data, thresh=2):
    """
    Based on mad, determine outliers by row
    :param data:
    :param thresh:
    :return: true for 'correct' value, false for outlier
    """
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(data, pd.DataFrame):
        data = data.values
    or_shape = data.shape
    data = data.flatten()
    if len(data.shape) == 1:
        data = data[:, None]
    mean = np.mean(data, axis=0)
    diff = np.sum((data - mean) ** 2, axis=-1)
    diff = np.sqrt(diff)
    std = np.std(diff)
    modified_z_score = 0.6745 * diff / std
    modified_z_score = modified_z_score.reshape(or_shape)
    return modified_z_score < thresh



df = pd.read_csv("PooledData.csv")
# print(df.head())

y = df.iloc[:, 7:11].apply(without_outlier_mad_based, axis=1, thresh=1.5)
# Y = df.iloc[:, 3:7][y]
# print(pd.concat([df.iloc[:, 3:7], Y], axis=1))

df.iloc[:, 7:11] = df.iloc[:, 7:11][y]
y.columns = df.iloc[:, 3:7].columns
df.iloc[:, 3:7] = df.iloc[:, 3:7][y]

df.loc[:,"Mean_CellsCount"] = df.iloc[:, 3:7].mean(axis=1)
df.loc[:,"Std_CellsCount"] = df.iloc[:, 3:7].std(axis=1)
df.loc[:,"Mean_PositiveCells"] = df.iloc[:, 7:11].mean(axis=1)
df.loc[:,"Std_PositiveCells"] = df.iloc[:, 7:11].std(axis=1)

print(df)
df.to_csv("PooledDataOutlierRemovedV2.csv", index=False, header=True)
