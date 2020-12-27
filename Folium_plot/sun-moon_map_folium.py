#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import folium
import json
import argparse
import time
from selenium import webdriver
from pandas import json_normalize 

def utf2asc(s):
    return str(str(s).encode('ascii', 'xmlcharrefreplace'))[2:-1]


parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='final_201709.csv')
parser.add_argument('--output_path', type=str, default='fmap-201709.csv')

args = parser.parse_args()

input_path, output_path = args.input_path, args.output_path

df = pd.read_csv(input_path)


fmap = folium.Map(location=[25.09124,121.5344], tiles='CartoDB positron', zoom_start=12.5)
for n in range(107):
    
    name = df['Station'].iloc[n]
    if df['label'].iloc[n] == 'A' :
        icon_url = "https://i.imgur.com/pae0T2U.png"
    elif df['label'].iloc[n] == 'B' :
        icon_url = "https://i.imgur.com/w7z8Wcq.png"
    elif df['label'].iloc[n] == 'C' :
        icon_url = "https://i.imgur.com/v9LvRvp.png"
    else:
        icon_url = "https://i.imgur.com/wnDXlOX.png"

    icon = folium.features.CustomIcon(icon_url,icon_size=(30, 30))  # Creating a custom Icon
    folium.Marker(
            location=[df['Latitude'].iloc[n],df['Longitude'].iloc[n]],
            popup= "<b>{}</b>".format( utf2asc(name) ),
            icon=icon
            ).add_to( fmap )

with open('MRT_lines.geojson', 'r', encoding='utf-8') as f:
    output = json.load(f)

df_feature = json_normalize(output['features'])

colorlst = ["#cc8528", "#e34043", "#fb9a99", "#ff9e17", "#ff9e17", "#33a02c", "#a7df72", "#2a54ff" ]

for i in range(8):
    points = df_feature['geometry.coordinates'][i]
    [ x.reverse() for x in points[0] ]
    folium.PolyLine(points, color=colorlst[i], weight=2.5, opacity=1).add_to(fmap)

fmap.save(output_path)
