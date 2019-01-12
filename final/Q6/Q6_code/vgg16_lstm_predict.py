import numpy as np
from keras import backend as K
import sys
import os
import pandas as pd
from keras_video_classifier.library.recurrent_networks import VGG16LSTMVideoClassifier

def main():
    K.set_image_dim_ordering('tf')
    #sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    #os.getcwd()
    current_path = os.getcwd()
   # from keras_video_classifier.library.recurrent_networks import VGG16LSTMVideoClassifier

    #from keras_video_classifier.library.utility.ucf.UCF101_loader import load_ucf, scan_ucf_with_labels

    vgg16_include_top = True
    data_dir_path = os.path.join(current_path, 'test_video')
    model_dir_path = os.path.join(current_path, 'models', 'p')
    config_file_path = VGG16LSTMVideoClassifier.get_config_file_path(model_dir_path,
                                                                     vgg16_include_top=vgg16_include_top)
    weight_file_path = VGG16LSTMVideoClassifier.get_weight_file_path(model_dir_path,
                                                                     vgg16_include_top=vgg16_include_top)

    np.random.seed(42)

    #load_ucf(data_dir_path)

    predictor = VGG16LSTMVideoClassifier()
    predictor.load_model(config_file_path, weight_file_path)

    #videos = scan_ucf_with_labels(data_dir_path)

    #video_file_path_list = data_dir_path

    #correct_count = 0
    #count = 0
    labels=[]
    videos=[]
    outlier=[]
    video_list = os.listdir(data_dir_path)
    #video_list_10 = video_list[800:820]
    count=0
    #for video in data_dir_path:
    for video in video_list:
        print(count)
        video = os.path.join(data_dir_path, video)
        #label = videos[vide o_file_path]
        try:
            predicted_label = predictor.predict(video)
            videos=np.append(videos,video)
            labels=np.append(labels,predicted_label)
        except:
            print(video)
            outlier.append(video)
        count+=1
        #print('predicted: ' + predicted_label + ' actual: ' + label)
        #correct_count = correct_count + 1 if label == predicted_label else correct_count
        #count += 1
        #accuracy = correct_count / count
        #print('accuracy: ', accuracy)
    return videos, labels, outlier

if __name__ == '__main__':
    videos, labels, outliers=main()
    
    video_list=[]
    for video in videos:
        (filepath, tempfilename) = os.path.split(video)
        video_list.append(tempfilename)
    submission=pd.DataFrame()
    submission['videos']=video_list
    submission['labels']=labels
    submission.to_csv('submission.csv',index=False)
    
    
    outlier_list=[]
    for outlier in outliers:
        (filepath, tempfilename) = os.path.split(outlier)
        outlier_list.append(tempfilename)
    
    outlier=pd.DataFrame()
    outlier['outlier']=outlier_list
    outlier.to_csv('outlier.csv',index=False)
    '''
    current_path = os.getcwd()
    data_dir_path = os.path.join(current_path, 'test_video')
    #model_dir_path = os.path.join(current_path, 'models', 'p')
    print(data_dir_path)
    #print(model_dir_path)
    print('---------------------------')
    #print(os.listdir(data_dir_path))
    video_list = os.listdir(data_dir_path)
    video1_path = os.path.join(data_dir_path, video_list[0])
    print(video1_path)
    '''

    
    
    
    
    
