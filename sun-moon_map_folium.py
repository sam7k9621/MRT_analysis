#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import folium
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='final_201709.csv')
parser.add_argument('--output_path', type=str, default='fmap-201709.csv')

args = parser.parse_args()

input_path, output_path = args.input_path, args.output_path


# In[2]:


df1709 = pd.read_csv(input_path)


# In[3]:


def utf2asc(s):
    return str(str(s).encode('ascii', 'xmlcharrefreplace'))[2:-1]


# In[5]:


heading3 = """<b>{}</b>""".format


# In[20]:


n = 0
fmap = folium.Map(location=[25.09124,121.5344],
                  zoom_start=12)
while n <= 106 :
    name = df1709['Station'].iloc[n]
    if df1709['label'].iloc[n] == 'A' :
        m = folium.Marker(location=[df1709['Latitude'].iloc[n],df1709['Longitude'].iloc[n]],
                          popup= heading3(utf2asc(name)),
                          icon=folium.Icon(icon = 'train', 
                                           color='red', 
                                           prefix='fa')) 
        fmap.add_child(child=m)
    elif df1709['label'].iloc[n] == 'B' :
        m = folium.Marker(location=[df1709['Latitude'].iloc[n],df1709['Longitude'].iloc[n]],
                          popup= heading3(utf2asc(name)),
                          icon=folium.Icon(icon = 'train', 
                                           color='blue', 
                                           prefix='fa')) 
        fmap.add_child(child = m)
    elif df1709['label'].iloc[n] == 'C' :
        m = folium.Marker(location=[df1709['Latitude'].iloc[n],df1709['Longitude'].iloc[n]],
                          popup= heading3(utf2asc(name)),
                          icon=folium.Icon(icon = 'train', 
                                           color='black', 
                                           prefix='fa')) 
        fmap.add_child(child = m)
    else :
        m = folium.Marker(location=[df1709['Latitude'].iloc[n],df1709['Longitude'].iloc[n]],
                          popup= heading3(utf2asc(name)),
                          icon=folium.Icon(icon = 'train', 
                                           color='green', 
                                           prefix='fa')) 
        fmap.add_child(child = m)
    n += 1

    


# In[23]:


fmap.save(output_path)


# In[ ]:




