#!/usr/bin/env python
# coding: utf-8

import folium
import json
import pandas as pd
import json
from pandas.io.json import json_normalize

def utf2asc(s):
    return str(str(s).encode('ascii', 'xmlcharrefreplace'))[2:-1]

df = pd.read_csv('Label_201703-201803-201903_ok.csv')

df.Label_do_count = df.Label_do_count.astype(str)
df.Label_no_count = df.Label_no_count.astype(str)

df['label'] = df.Label_do_count +df.Label_no_count

fmap = folium.Map(location=[25.061, 121.515], zoom_start=13, tiles="CartoDB positron", zoom_control=False)

for n in range(108):
    name = df['Station'].iloc[n]
    if df['label'].iloc[n] == '00' :
        icon_url = "https://i.imgur.com/73mJHas.png"
    elif df['label'].iloc[n] == '01' :
        icon_url = "https://i.imgur.com/ONp8Byr.png"
    elif df['label'].iloc[n] == '02' :
        icon_url = "https://i.imgur.com/cY9As61.png"
    elif df['label'].iloc[n] == '10' :
        icon_url = "https://i.imgur.com/41w0XqK.png"
    elif df['label'].iloc[n] == '11' :
        icon_url = "https://i.imgur.com/nZ3FUKb.png"
    elif df['label'].iloc[n] == '12' :
        icon_url = "https://i.imgur.com/XAzH700.png"
    elif df['label'].iloc[n] == '20' :
        icon_url = "https://i.imgur.com/lqhTYj7.png"
    elif df['label'].iloc[n] == '21' :
        icon_url = "https://i.imgur.com/pSjWLOx.png"
    else:
        icon_url = "https://i.imgur.com/UktEIKo.png"
        
    icon = folium.features.CustomIcon(icon_url,icon_size=(39,26))  # Creating a custom Icon
    folium.Marker(
        location=[df['Latitude'].iloc[n],df['Longitude'].iloc[n]],
        popup= "<b>{}</b>".format( utf2asc(name) ),
        icon=icon).add_to(fmap) 


with open(r'MRT_lines.geojson', 'r', encoding='utf-8') as f:
    output = json.load(f)

df_feature = json_normalize(output['features'])

colorlst = ["#cc8528", "#e34043", "#fb9a99", "#ff9e17", "#ff9e17", "#33a02c", "#a7df72", "#2a54ff" ]

for i in range(8):
    points = df_feature['geometry.coordinates'][i]
    [ x.reverse() for x in points[0] ]
    folium.PolyLine(points, color=colorlst[i], weight=3.5, opacity=1).add_to(fmap)

df_shop = pd.read_csv(r'晚上藥妝店.csv')

icon_url = "https://imgur.com/fjitDvs.png"
for n in range(df_shop.index.stop):
    icon = folium.features.CustomIcon(icon_url,icon_size=(10,10))  
    folium.Marker(
        location=[df_shop['Latitude'].iloc[n],df_shop['Longitude'].iloc[n]],
        icon= icon).add_to(fmap)

with open('捷運站環域800公尺_遮罩加大.geojson', 'r', encoding='utf-8') as f:
    output = json.load(f)

df_feature = json_normalize(output['features'])

points = df_feature['geometry.coordinates'][0][0]
for i in range(7):
    [ x.reverse() for x in points[i] ]

mrt_range800 = folium.vector_layers.Polygon(points,color='#ff7800',fill = True,fill_color='#9D9D9D', opacity= 0,fill_opacity =0.5).add_to(fmap)


fmap.save('ming_map03_cosme_p5_l.html')
