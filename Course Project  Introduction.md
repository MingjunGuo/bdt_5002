# Big Data Technology || Course Project 介绍
## bdt_5002：数据挖掘
### 1. Hash Tree, FP-Tree 实现：https://github.com/MingjunGuo/bdt_5002/tree/master/assign1
### 2. 收入预测：https://github.com/MingjunGuo/bdt_5002/tree/master/assign2
### 3. 图像聚类：https://github.com/MingjunGuo/bdt_5002/tree/master/assign3
### 4. 时空天气预测：https://github.com/MingjunGuo/bdt_5002/tree/master/project
* 数据预处理：通过删除重复数据、补充缺失值（不同空气质量站点之间的距离、缺失时间间隔大小等因素衡量）等方法，
  共获得 11626 小时的空气质量、天气情况数据（35个空气质量站点）；
* 特征工程：增加天气情况特征（天气网格站点与空气质量站点间的距离等衡量）、周期性特征（每24小时）；
* 模型预测：选取Seq2Seq 模型，采用每24 * 5 hours预测 24 * 2 hours 的方法进行训练， 获得SMAPE为0.73.

## bdt_5410: 模式识别
### 1. 边缘检测、SIFT 特征匹配：https://github.com/MingjunGuo/bdt_5410/tree/master/csit5410_assign1
### 2. 霍夫变换实现（圆）、FLD算法实现：https://github.com/MingjunGuo/bdt_5410/tree/master/csit5410_assign2
