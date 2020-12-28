#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

all_df = pd.read_csv('Weather_Xihu_201901-201902-201903-201904-201905-201906-201907-201908-201909-201910-201911-201912.csv')

all_df[all_df['Weekday'] >3]

index_all = all_df[all_df['Weekday'] > 3].index
all_df.drop(index_all,inplace = True)

def all_count(row):
    return row['in_count'] + row['out_count']

all_df['all_count'] = all_df.apply(all_count,axis = 1)

rain = all_df[all_df['R_label'] > 0]

rindex = all_df[all_df['R_label'] > 0].index

all_df.drop(rindex,inplace = True)

mean = all_df.groupby(['Time']).mean()

mean.drop(columns = ['Weekday'],inplace = True)

def var_count(row):
    return (row['all_count'] - mean['all_count'][row['Time']]) / mean['all_count'][row['Time']]

rain['Variety'] = rain.apply(var_count,axis = 1)

output = pd.DataFrame(columns =['Variety','Drop','R_label'])
output['Variety'] = rain['Variety']
output['Drop'] = rain['Drop']
output['R_label'] = rain['R_label']

output.to_csv('output_Xihu.csv',index = False)
