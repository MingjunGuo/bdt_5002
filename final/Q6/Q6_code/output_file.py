# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 02:50:43 2018

@author: Ashley
"""

import pandas as pd 
import numpy as np
import os

df1=pd.read_csv("submission.csv",header='infer')
df2=pd.read_csv("outlier.csv",header='infer')
df2.columns=['videos']
df2['labels']=-1
df=pd.concat([df1,df2],axis=0)

df.set_index('videos',inplace=True)
df=df.drop(['UCF101.rar'])


vd=df.index
current_path = os.getcwd()
data_dir_path = os.path.join(current_path, 'test_video')
video_list = os.listdir(data_dir_path)
#for video in videos:
    #(filepath, tempfilename) = os.path.split(video)
    #video_list.append(tempfilename)