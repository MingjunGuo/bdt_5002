# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 23:48:58 2018

@author: Ashley
"""

import numpy as np
import pandas as pd
import shutil
import os

import csv

file = open('D:\\18\\bdt\\5002\\final\\Q6\\train_tag.txt', 'r')
reader = csv.reader(file)
data = [row for row in reader]




def get_file_name(path):
    '''''
    Args: path to list;  Returns: path with filenames
    '''
    filenames = os.listdir(path)
    path_filenames = []
    filename_list = []
    for file in filenames:
        if not file.startswith('.'):
            path_filenames.append(os.path.join(path, file))
            filename_list.append(file)

    return path_filenames,filename_list

def retrun_class(labels):

    #files = [file.split('/')[-1] for file in filenames]

    for i, label in enumerate(labels):

        shutil.copy("./demo/train_video/"+labels.iloc[i,0], "./"+labels.iloc[i,1]+"/"+labels.iloc[i,0])




path_filenames,pic_names = get_file_name("./demo/train_video/")
pic_df=pd.DataFrame(pic_names)
label=pd.DataFrame(data)
for i in range(15):
    os.mkdir(os.path.join(os.path.abspath('.'), str(i)))
out_label=pic_df.merge(label, left_on=[0], right_on=[0], how='inner')
retrun_class(out_label)
