# -*- coding: UTF-8 -*-
## 主程序
import sys
import os
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF

from model.seq2seq.train_seq2seq import train_model
from utils.output_util import write_value_to_csv

os.environ['CUDA_VISIBLE_DEVICES'] = '1'
gpu_config = tf.ConfigProto()
gpu_config.gpu_options.allow_growth = True
session = tf.Session(config=gpu_config)
KTF.set_session(session)

# debug to see the whole process
use_day_model = False
generate_mean = False
generate_range = False
use_norm_data = True
gap=0
predict_one_day = False

# 训练模型

results = {}

total_iteractions = 100
pre_days_list = [5]
loss_functions = ["L1"]

for city in ['bj']:
    results[city] = {}
    dev_y_original_flag = True
    aggr_y_original_flag = True

    for pre_days in pre_days_list:
        for loss_function in loss_functions:

            print("Use day model : %r, city %s 使用 %d 天, 使用 %s 损失函数" % (use_day_model, city, pre_days, loss_function))

            aver_smapes_best, model_preds_on_dev, dev_y_original, model_preds_on_aggr, aggr_y_original, model_preds_on_test, output_features = train_model(
                city=city,
                pre_days=pre_days,
                gap=gap,
                loss_function=loss_function,
                total_iteractions=total_iteractions,
                use_day_model=use_day_model,
                use_norm_data=use_norm_data,
                generate_mean=generate_mean,
                generate_range=generate_range,
                loss_weights=False,
                predict_one_day=predict_one_day)

            if use_day_model:
                traing_result = "Use day model, city %s 使用 %d 天, 使用 %s 损失函数, best_sampe = %.5f\n" % (
                city, pre_days, loss_function, aver_smapes_best)
            else:
                traing_result = "Use hour model, city %s 使用 %d 天, 使用 %s 损失函数, best_sampe = %.5f\n" % (
                city, pre_days, loss_function, aver_smapes_best)
            print(traing_result)

            # write training summary results to txt files.
            traing_result_file_name = "./training_results/single_model_%s.txt" % city
            file_dir = os.path.split(traing_result_file_name)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if not os.path.exists(traing_result_file_name):
                os.mknod(traing_result_file_name)
            with open(traing_result_file_name, "a") as f:
                f.write(traing_result)

            # write data to file for further use
            # file_name are like : "city_bj_predays_5_L2_loss_model_preds_on_dev"
            value_name = "model_preds_on_dev"
            file_name = "city_%s_predays_%d_%s_loss_%s" % (city, pre_days, loss_function, value_name)
            write_value_to_csv(city, file_name, model_preds_on_dev, output_features, day=use_day_model,
                               one_day_model=predict_one_day)

            value_name = "model_preds_on_test"
            file_name = "city_%s_predays_%d_%s_loss_%s" % (city, pre_days, loss_function, value_name)
            write_value_to_csv(city, file_name, model_preds_on_test, output_features, day=use_day_model,
                               one_day_model=predict_one_day)

            value_name = "model_preds_on_aggr"
            file_name = "city_%s_predays_%d_%s_loss_%s" % (city, pre_days, loss_function, value_name)
            write_value_to_csv(city, file_name, model_preds_on_aggr, output_features, day=use_day_model,
                               one_day_model=predict_one_day)

            # save only once
            while dev_y_original_flag:
                value_name = "dev_y"
                file_name = "city_%s_%s" % (city, value_name)
                write_value_to_csv(city, file_name, dev_y_original, output_features, day=use_day_model,
                                   one_day_model=predict_one_day)
                dev_y_original_flag = False

            # save only once
            while aggr_y_original_flag:
                value_name = "aggr_y"
                file_name = "city_%s_%s" % (city, value_name)
                write_value_to_csv(city, file_name, aggr_y_original, output_features, day=use_day_model,
                                   one_day_model=predict_one_day)
                aggr_y_original_flag = False

            results[city][aver_smapes_best] = [model_preds_on_dev, dev_y_original, model_preds_on_test, output_features]
