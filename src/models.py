from dictionaries import *

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold
from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import BernoulliNB as BNB
from sklearn.naive_bayes import ComplementNB as CNB
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.naive_bayes import MultinomialNB as MNB

# from sklearn.model_selection import GridSearchCV

from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import GradientBoostingClassifier as GBC

from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error

from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold
from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# from sklearn.model_selection import GridSearchCV

from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import GradientBoostingClassifier as GBC

from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.constraints import max_norm

def preprocess_data(target = 'recovery'):
    df = pd.read_csv('data/full_dataset.csv')
    X = df.loc[:,features].values
    y_recovery = df.loc[:,['recovery']].values * 1
    y_delta = df.loc[:,['delta']].values
    y_recovery = y_recovery.reshape(len(y_recovery),)
    y_delta = y_delta.reshape(len(y_delta),)
    X_train, X_test, y_train, y_test = train_test_split(X, y_recovery, test_size=.2, stratify = y_recovery)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    # pca = PCA(0.85)
    # pca.fit(X_train)
    # X_train = pca.transform(X_train)
    # X_test = pca.transform(X_test)
    return X_train, X_test, y_train, y_test

def plot_ROC_curves(models):
    results = {}
    X_train, X_test, y_train, y_test = preprocess_data(target = 'recovery')
    fig, ax = plt.subplots(1, figsize=(10,10))
    # ax.title('RoC Curve')
    for model in models:
        model.fit(X_train, y_train)
        y_predicted = model.predict(X_test)
        # fpr, tpr, threshold = roc_curve(y_test, y_predicted)
        plot_roc_curve(model, X_test, y_test, ax=ax)
        # print(f' {model}-roc_auc_score:', roc_auc_score(y_test, y_predicted))
    ax.plot([0, 1], ls="--")
    ax.plot([0, 0], [1, 0] , c=".7"), plt.plot([1, 1] , c=".7")
    # plt.ylabel('True Positive Rate')
    # plt.xlabel('False Positive Rate')
    plt.tight_layout()
    plt.show()

dtc =DTC(max_features = 1000,min_samples_split = 2,min_samples_leaf = 175,max_depth = 14)                                                         
rfc = RFC(n_estimators = 310, max_depth = 15, min_samples_split=2, min_samples_leaf = 5)                                                         
gbc = GBC(learning_rate =0.01, n_estimators = 375, max_depth = 2)                                                                               
# dmlp = Sequential()
# dmlp.add(Dense(350, activation='relu', input_shape=(5126,)))
# dmlp.add(Dense(50, activation='relu'))
# dmlp.add(Dense(1, activation='sigmoid',kernel_constraint=max_norm(3), bias_constraint=max_norm(3)))
# dmlp.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

plot_ROC_curves([dtc, rfc, gbc]) 





