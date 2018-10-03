#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import os
import fnmatch
import logging

MASTER = '/home/arnaud/Desktop/HDV/DATA/'
SLAVE = '/home/arnaud/Desktop/HDV/DATA/new_well/'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

for file in os.listdir(SLAVE):
    if fnmatch.fnmatch(file, '*.csv'):
        slave_df = pd.read_csv(SLAVE+file)
        well = slave_df.Well.unique()

        logging.info('Read {}'.format(file))
        master_df = pd.read_csv(MASTER+file, engine='c')
        for i in well:
            logging.info('Remove well {}: '.format(i))
            master_df = master_df[master_df['Well'] != i]

        master_df = master_df.append(slave_df)
        logging.info('Save file')
        master_df.to_csv(SLAVE+'NEW'+file, index=False)