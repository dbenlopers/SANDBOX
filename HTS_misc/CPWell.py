#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import os

HelaList = ['HeLa HU 4h.csv', 'HeLa HU 24h.csv', 'HeLa NCS 2h.csv', 'HeLa NCS 16h.csv']
HelaMaster = 'HeLa no drug.csv'

U2osList = ['U2OS HU 4h.csv', 'U2OS HU 24h.csv', 'U2OS NCS 4h.csv', 'U2OS NCS 24h.csv']
U2osMaster = 'U2OS no drug.csv'

def replace_by_master(master, listwheretoreplace, well):
    path = '/home/arnaud/Desktop/Anne/Datas mini screen Federica/'
    master_df = pd.read_csv(os.path.join(path, master))
    dataMaster = pd.DataFrame()
    for i in well:
        print(i)
        dataMaster = dataMaster.append(master_df[master_df['Well'] == i])
    print(len(dataMaster))

    for file in listwheretoreplace:
        df = pd.read_csv(os.path.join(path, file))
        for j in well:
            df = df[df['Well'] != j]
        df = df.append(dataMaster)
        df.to_csv(os.path.join(path, 'Update_'+str(file)))

replace_by_master(HelaMaster, HelaList, ['B11', 'D11', 'F11'])
replace_by_master(U2osMaster, U2osList, ['B11', 'D11', 'F11'])
