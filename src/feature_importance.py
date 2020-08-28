import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dictionaries import features

# from sklearn.model_selection import KFold
# from sklearn.model_selection import cross_val_score
# from sklearn.preprocessing import scale
# from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# from sklearn.model_selection import GridSearchCV

from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import GradientBoostingClassifier as GBC


# from sklearn.metrics import plot_roc_curve
# import seaborn as sns
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import precision_score
# from sklearn.metrics import recall_score
# from sklearn.metrics import f1_score


df = pd.read_csv("data/full_dataset.csv",
                   dtype={"area_fips": str}, low_memory=False)
X = df.loc[:,features].values
y_recovery = df.loc[:,['recovery']].values * 1
y_delta = df.loc[:,['delta']].values
y_recovery = y_recovery.reshape(len(y_recovery),)
y_delta = y_delta.reshape(len(y_recovery),)
X_train, X_test, y_train, y_test = train_test_split(X, y_recovery, test_size=.2, stratify = y_recovery)
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

dtc = DTC(max_features=2000, min_samples_split=2,min_samples_leaf=300, max_depth=2)
rfc = RFC(n_estimators=100, max_depth=15, min_samples_split=2, min_samples_leaf=10)
gbc = GBC(learning_rate= 0.01, n_estimators = 375, max_depth = 2)

models = (dtc, rfc, gbc)


def feature_importance(models):
    feature_importance = [np.array(features)]
    for model in models:
        model.fit(X_train, y_train)
        y_predicted = model.predict(X_test)
        feature_importance.append(model.feature_importances_)
    df = pd.DataFrame(feature_importance)
    df = df.transpose()
    return df

df = feature_importance(models)

columns = {0:'Features', 1:'DTC', 2:'RFC', 3:'GBC'}

df = df.rename(columns=columns)

df.to_csv('data/feature_imp.csv')