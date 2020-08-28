#this file computes the r2 values of the regressor models. 

import pandas as pd 
import numpy as np
import seaborn as sns

from src.dictionaries import *

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.ensemble import GradientBoostingRegressor as GBR 
from sklearn.metrics import r2_score


df = pd.read_csv('data/full_dataset.csv')

X = df.loc[:,features].values
y_recovery = df.loc[:,['recovery']].values * 1
y_delta_percap = df.loc[:,['delta_percap']].values
y_recovery = y_recovery.reshape(len(y_recovery),)
y_delta_percap = y_delta_percap.reshape(len(y_delta_percap),)
X_train, X_test, y_train, y_test = train_test_split(X, y_delta_percap, test_size=.2)
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

dtr = DTR(max_features =  2000, min_samples_split = 2, min_samples_leaf =300, max_depth = 14)
rfr = RFR(n_estimators =  310, max_depth = 15, min_samples_split = 2, min_samples_leaf = 5)
gbr = GBR(learning_rate = 0.01, n_estimators = 375, max_depth =2)

models = [dtr,rfr,gbr]

def get_r2_scores(models):
    for model in models:
        model.fit(X_train, y_train)
        y_predicted = model.predict(X_test)
        print(model)
        print(f' r2 score: {r2_score(y_test,y_predicted)}')

print(get_r2_scores(models))


