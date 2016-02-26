#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import os

df = pd.read_csv("/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation A/150219 Valid dux4 3.1 (copy).csv")


for i in ["D", "E", "F", "G"]:
    for j in range(3, 23):
        df = df[df["Well"] != i+str(j)]


df.to_csv("/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation A/150219 Valid dux4 3.1.csv", index=False, header=True)




df = pd.read_csv("/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation A/150219 Valid dux4 3.2 (copy).csv")

for i in ["B", "C", "F", "G"]:
    for j in range(3, 23):
        df = df[df["Well"] != i+str(j)]

for i in range(3, 23):
    df.loc[df["Well"] == "D"+str(i), "Well"] = "B"+str(i)
    df.loc[df["Well"] == "E"+str(i), "Well"] = "C"+str(i)



df.to_csv("/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation A/150219 Valid dux4 3.2.csv", index=False, header=True)



df = pd.read_csv("/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation A/150219 Valid dux4 3.3 (copy).csv")

for i in ["B", "C", "D", "E"]:
    for j in range(3, 23):
        df = df[df["Well"] != i+str(j)]

for i in range(3, 23):
    df.loc[df["Well"] == "F"+str(i), "Well"] = "B"+str(i)
    df.loc[df["Well"] == "G"+str(i), "Well"] = "C"+str(i)

df.to_csv("/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation A/150219 Valid dux4 3.3.csv", index=False, header=True)
