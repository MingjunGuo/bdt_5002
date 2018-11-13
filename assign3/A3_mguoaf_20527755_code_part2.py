import numpy as np
from sklearn.cluster import KMeans
import time
import pandas as pd
import shutil
import os
import glob
from sklearn import metrics

last_time = time.clock()

# load the feature from csv
feature_extractor = np.loadtxt('Resnet_feature_extractor.csv', dtype=np.float, delimiter=',')

# Clustering by Kmeans
n_clusters = 18
cluster_result = KMeans(n_clusters=n_clusters, random_state=17).fit(feature_extractor)

# # looking for better K
# labels = cluster_result.labels_
# reward = metrics.silhouette_score(feature_extractor, labels, metric='euclidean')
# print(reward)

# save the result in the dict
cluster_result = cluster_result.labels_.tolist()
d = dict()
for i, label in enumerate(cluster_result):
    if label not in d.keys():
        d[label] = []
    d[label].append(i)

# save the dict in the dataframe and save the dataframe in the csv
# submission = pd.DataFrame.from_dict(d)
submission = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in d.items()]))
submission.to_csv('A3_mguoaf_20527755_prediction.csv', index=False)

# put images with the same label into one file
# step1:read the file information
file_path = 'images/'
f_names = glob.glob(file_path+'*.jpg')
files = [file.split('\\')[-1] for file in f_names]

# step2:classify the image with the same label into one file
for i in range(len(d)):
    label = d[i]
    for j in range(len(label)):
        src = f_names[label[j]]
        path = 'class/' + str(i)
        if not os.path.exists(path):
            os.makedirs(path)
        shutil.copy(src, 'class/' + str(i))


current_time = time.clock()
print('total time consuming for feature clustering: {}'.format(current_time-last_time))













