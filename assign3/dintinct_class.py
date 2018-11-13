import numpy as np
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
import glob
import os
import time

last_time = time.clock()
# ignore the information from hardware speed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# read the file information
file_path = 'images/'
f_names = glob.glob(file_path+'*.jpg')

# load the model
model = ResNet50(weights='imagenet', include_top=True)
# model.summary()

# load the image, predict the class and put them in the list
predict_class = []
for i in range(len(f_names)):
    images = image.load_img(f_names[i], target_size=(224, 224))
    x = image.img_to_array(images)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    pred_class = model.predict(x)
    # decode the results into a list of tuples(class, description, probability)
    pred_class_max = decode_predictions(pred_class, top=1)[0]
    pred_class_max = pred_class_max[0][1]
    predict_class.append(pred_class_max)
    # print('Predicted class with highest probability:', decode_predictions(pred_class, top=1)[0])
    print('predict class for no.%s image' % i)

predict_class = set(predict_class)
print(len(predict_class))  # 680 distinct class
current_time = time.clock()
print('total time consuming for feature extractor: {}'.format(current_time-last_time))


