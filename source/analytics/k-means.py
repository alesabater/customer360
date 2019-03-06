#Analytical model for customer segmentation
#Status of code's output: VALID WITH PLACEHOLDER DATA
#Overall code status: UGLY–NEEDS REFINEMENT

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("att_tab.csv")

df.head()

df.dtypes

dfc = df.loc[:,[c for c in df.columns if c!="CREATION_DATE"]]

from sklearn.cluster import KMeans
import numpy as np

kmeans = KMeans(n_clusters=2, random_state=0).fit(dfc) #K-means clustering

kmeans.labels_

y_pred = kmeans.predict(dfc) #K-means prediction for future data

from sklearn import decomposition
X_prime = decomposition.PCA(n_components=2).fit_transform(dfc) #PCA dimensionality reduction

plt.subplot(221)
plt.scatter(X_prime[:, 0], X_prime[:, 1], c=kmeans.labels_)
plt.title("all the points with the groups as colors")

#np.shape(X_prime)

