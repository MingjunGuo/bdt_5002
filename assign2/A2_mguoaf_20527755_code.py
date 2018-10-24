# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler


# 2.2 load the data from .csv and merge the train_x and train_y to train
train_x = pd.read_csv('trainFeatures.csv')
train_y_column = ['income']
train_y = pd.read_csv('trainLabels.csv', header=None, names=train_y_column)
train = pd.concat([train_x, train_y], axis=1)
test_x = pd.read_csv('testFeatures.csv')
train_column = list(train.columns.values)
test_column = list(test_x.columns.values)

# 2.3 now we have train|text_x, we explore some information about the df and the attribute
train.head()
# 15columns: 7 int column + 8 object column
# 34189 entries
train.info()
# 14 columns: 6 int column + 8 object column
test_x.info()
train.workclass.value_counts()  # ? 1950
train['occupation'].value_counts()  # ? 1960
train['native-country'].value_counts()  # ? 589
# we find strang' ?', so we replace it by np.nan
train.replace(' ?', np.nan, inplace=True)
test_x.replace(' ?', np.nan, inplace=True)
# after replace, we explore data continually
train.isnull().sum()
test_x.isnull().sum()

#  2.4 now we have find missing value(still don't processing),
#  and we bagin to preprocess the data and make feature engineering
train['income'].value_counts() # 0:26021, 1: 8186
# 2.4.1 'age'(int)
plt.hist(train['age']);
# 2.4.2 'fnlwgt', transform it by log1p
train['fnlwgt'].describe()
train['fnlwgt'] = train['fnlwgt'].apply(lambda x: np.log1p(x))
test_x['fnlwgt'] = test_x['fnlwgt'].apply(lambda x: np.log1p(x))
train['fnlwgt'].describe()
# 2.4.3 'education', merge some education bg into 'primary'
train['education'].value_counts()
sns.factorplot(x='education', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60); # some education bg display the same income tendency


def primary(x):
    if x in [' 1st-4th', ' 5th-6th', ' 7th-8th', ' 9th', ' 10th', ' 11th', ' 12th']:
        return 'primary'
    else:
        return x

train['education'] = train['education'].apply(primary)
test_x['education'] = test_x['education'].apply(primary)
sns.factorplot(x='education', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60);
# 2.4.4 'education-num'
sns.factorplot(x='education-num', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60); # income increase with the level of educaton-num increase
# 2.4.5 'marital-status', merge 2(similar tendency and 1 is small in number) into 1
sns.factorplot(x='Marital-status', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60);  # married-af-spouse is similar to married-civ-spouse
train['Marital-status'].value_counts() #  Married-AF-spouse  is so small
train['Marital-status'].replace(' Married-AF-spouse', ' Married-civ-spouse', inplace=True)
test_x['Marital-status'].replace(' Married-AF-spouse', ' Married-civ-spouse', inplace=True)
sns.factorplot(x='Marital-status', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60);
# 2.4.6 'relationship', 
sns.factorplot(x='relationship', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60);
train['relationship'].value_counts()# both wife and husband has big number, so we don't merge them
# 2.4.7 'race'
sns.factorplot(x='race', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60);
train['race'].value_counts()
# 2.4.8 'sex'
sns.factorplot(x='sex', y='income', data=train, kind='bar', size=7, palette='muted')
plt.xticks(rotation=60);
# 2.4.9 'capital gain' # training data and testing data has similar distribution,so we don't preprocess them
plt.boxplot(train['capital-gain']);
plt.boxplot(test_x['capital-gain']);
train['capital-gain'].describe()
test_x['capital-gain'].describe()
# 2.4.10 'capital loss' : training data and testing data has similar distribution, so we don't preprocess
train['capital-loss'].describe()
plt.hist(train['capital-loss']);
plt.hist(test_x['capital-loss']);
# 2.4.11 'hours-per-week': training data and testing data has similar distribution, so we don't preprocess
plt.hist(train['hours-per-week']);
plt.hist(test_x['hours-per-week']);
# 2.4.12 'native-country': fill missing value by US, and merge them by location
train['native-country'].value_counts()
train['native-country'].fillna(' United-States', inplace=True)
test_x['native-country'].fillna(' United-States', inplace=True)
train['native-country'].value_counts()
sns.factorplot(x="native-country",y="income",data=train,kind="bar", size = 10, palette = "muted")
plt.xticks(rotation=80);


def native(country):
    if country in [' United-States', ' Cuba']:
        return 'US'
    elif country in [' England', ' Germany', ' Canada', ' Italy', ' France', ' Greece', ' Philippines']:
        return 'Western'
    elif country in [' Mexico', ' Puerto-Rico', ' Honduras', ' Jamaica', ' Columbia', ' Laos', ' Portugal', ' Haiti',
                     ' Dominican-Republic', ' El-Salvador', ' Guatemala', ' Peru', 
                     ' Trinadad&Tobago', ' Outlying-US(Guam-USVI-etc)', ' Nicaragua', ' Vietnam', ' Holand-Netherlands' ]:
        return 'Poor' # no offence
    elif country in [' India', ' Iran', ' Cambodia', ' Taiwan', ' Japan', ' Yugoslavia', ' China', ' Hong']:
        return 'Eastern'
    elif country in [' South', ' Poland', ' Ireland', ' Hungary', ' Scotland', ' Thailand', ' Ecuador']:
        return 'Poland team'
    
    else: 
        return country 
    

train['native-country'] = train['native-country'].apply(native)
test_x['native-country'] = test_x['native-country'].apply(native)
train['native-country'].value_counts()
sns.factorplot(x="native-country",y="income",data=train,kind="bar", size = 10, palette = "muted")
plt.xticks(rotation=80);
train.isnull().sum()
# 2.4.13 'workclass': fill missing value by mode
train['workclass'].value_counts()
train['workclass'].fillna(' Private', inplace=True)
test_x['workclass'].fillna(' Private', inplace=True)
train['workclass'].value_counts()
test_x['workclass'].value_counts()
train['workclass'].replace(' Never-worked', ' Without-pay', inplace=True)
sns.factorplot(x="workclass",y="income",data=train,kind="bar", size = 10, palette = "muted")
plt.xticks(rotation=80);


# In[53]:


# 2.4.14 'occupation' fill missing value by 0
train['occupation'].fillna(' 0', inplace=True)
test_x['occupation'].fillna(' 0', inplace=True)
sns.factorplot(x="occupation",y="income",data=train,kind="bar", size = 10, palette = "muted")
plt.xticks(rotation=80);
train['occupation'].value_counts()
train['occupation'].replace(' Armed-Forces', ' Protective-serv', inplace=True)
test_x['occupation'].replace(' Armed-Forces', ' Protective-serv', inplace=True)
sns.factorplot(x="occupation",y="income",data=train,kind="bar", size = 10, palette = "muted")
plt.xticks(rotation=80);
train.isnull().sum()
test_x.isnull().sum()


#  2.5 split training data to training and validation data
train.dtypes
# 2.5.1 list of columns with dtype: object
categorical_features = train.select_dtypes(include=['object']).axes[1]
for col in categorical_features:
    print(col, train[col].nunique())

# 2.5.2 one-hot encoder
for col in categorical_features:
    train = pd.concat([train, pd.get_dummies(train[col], prefix=col, prefix_sep=':')], axis=1)
    train.drop(col, axis=1, inplace=True)

train.head()
categorical_features = test_x.select_dtypes(include=['object']).axes[1]
for col in categorical_features:
    print(col, test_x[col].nunique())
train.columns
# 2.5.3 apply the same way(one-hot encoder) to test_x
for col in categorical_features:
    test_x = pd.concat([test_x, pd.get_dummies(test_x[col], prefix=col, prefix_sep=':')], axis=1)
    test_x.drop(col, axis=1, inplace=True)
test_x.head()
test_x.columns
# 2.5.4 scaler the X and split the training data to training data and validation data 
x = train.drop('income', axis=1)
y = train['income']
scaler = StandardScaler()
scaler.fit(x)
x = scaler.transform(x)
test_x = scaler.transform(test_x)
from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ttrain, Ttest = train_test_split(x, y, test_size=0.2, random_state=42)


# ### 2.6 after prepare the data, we begin to use different model to compute the accuracy

# #### 2.6.1 logistic regression
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(Xtrain, Ttrain)
print('training accuracy: ', model.score(Xtrain, Ttrain))
print('validation accuracy: ', model.score(Xtest, Ttest))

# #### 2.6.2 GBRT
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation, metrics
from sklearn.grid_search import GridSearchCV
import matplotlib.pylab as plt
gbm0 = GradientBoostingClassifier(random_state=10)
gbm0.fit(Xtrain, Ttrain)
y_pred = gbm0.predict(Xtrain)
y_predprob = gbm0.predict_proba(Xtrain)[:,1]
print('Accuracy: %.4g' % metrics.accuracy_score(Ttrain, y_pred))
print('AUC Score(train): %f' % metrics.roc_auc_score(Ttrain, y_predprob))

gbm2 = GradientBoostingClassifier(learning_rate=0.1, n_estimators=140,max_depth=12, min_samples_leaf =30, 
               min_samples_split =1800, max_features=38, subsample=1.0, random_state=10)
gbm2.fit(Xtrain, Ttrain)
y_pred = gbm2.predict(Xtrain)
y_predprob = gbm2.predict_proba(Xtrain)[:,1]
print('traing accuracy: %.4g' % metrics.accuracy_score(Ttrain, y_pred))
print('AUC Score(train): %f' % metrics.roc_auc_score(Ttrain, y_predprob))
test_pred = gbm2.predict(Xtest)
print ("validation accuracy : %.4g" % metrics.accuracy_score(Ttest, test_pred))

test_prediction = gbm2.predict(test_x)


# ## 2.7 output the prediction result

import pandas as pd
test_prediction_series = pd.Series(test_prediction)
test_prediction_series.to_csv(path='E:/python/5002DM/assign2/A2_mguoaf_20527755_prediction.csv', index=False)

