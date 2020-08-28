#exploratory PCA. Did not make it into final

import pandas as pd
from src.dictionaries import features
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/full_dataset.csv')

def pca(df, components):
    X = df.loc[:,features].values
    y_recovery = df.loc[:,['recovery']] * 1
    y_delta = df.loc[:,['delta']]
    X = StandardScaler().fit_transform(X)
    pca = PCA(n_components = components)
    principalComponents = pca.fit_transform(X)
    principalDf = pd.DataFrame(principalComponents)
    finalDf = pd.concat([principalDf, df[['recovery']]], axis = 1)
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    colors = ['r', 'g', 'b']
    for target, color in zip(targets,colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
    ax.legend(targets)
    ax.grid()
    return PCs

        