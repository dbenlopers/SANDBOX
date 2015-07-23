#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd
import os
import fnmatch

path = '/home/arnaud/Desktop/Schneider/BatchV2/'


for file in os.listdir(path):
	if fnmatch.fnmatch(file, '*.csv'):
		df = pd.read_csv(os.path.join(path, file))
		df['Well'] = df['Well'].str.replace(' - ', '')
		df['Well'] = df['Well'].str.replace(r"\(.*\)", "")
		df.to_csv(os.path.join(path, file))
