#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[17]:


all_df = pd.read_csv('Weather_Xihu_201901-201902-201903-201904-201905-201906-201907-201908-201909-201910-201911-201912.csv')


# In[18]:


all_df[all_df['Weekday'] >3]


# In[19]:


index_all = all_df[all_df['Weekday'] > 3].index
all_df.drop(index_all,inplace = True)


# In[20]:


def all_count(row):
    return row['in_count'] + row['out_count']


# In[21]:


all_df['all_count'] = all_df.apply(all_count,axis = 1)


# In[22]:


rain = all_df[all_df['R_label'] > 0]


# In[23]:


rindex = all_df[all_df['R_label'] > 0].index


# In[24]:


all_df.drop(rindex,inplace = True)


# In[25]:


mean = all_df.groupby(['Time']).mean()


# In[26]:


mean.drop(columns = ['Weekday'],inplace = True)


# In[27]:


def var_count(row):
    return (row['all_count'] - mean['all_count'][row['Time']]) / mean['all_count'][row['Time']]


# In[28]:


rain['Variety'] = rain.apply(var_count,axis = 1)


# In[29]:


output = pd.DataFrame(columns =['Variety','Drop','R_label'])
output['Variety'] = rain['Variety']
output['Drop'] = rain['Drop']
output['R_label'] = rain['R_label']


# In[31]:


output.to_csv('output_Xihu.csv',index = False)


# In[30]:


output


# In[ ]:




