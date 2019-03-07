#Analytical model for customer segmentation
#Status of code's output: VALID WITH PLACEHOLDER DATA
#Overall code status: NEEDS FURTHER DEVELOPMENT
#Already split into planned notebook segments

#Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn import decomposition

#Load Attributes table data onto a Pandas DataFrame
df = pd.read_csv("att_tab.csv")

#Visualise DataFrame and the column types
df.head()
df.dtypes

#Get all values from all columns except "CREATION_DATE"
dfc = df.loc[:,[c for c in df.columns if c!="CREATION_DATE"]]

#Create KMeans object with 2 clusters and pass dfc data
kmeans = KMeans(n_clusters=2, random_state=0).fit(dfc)

#List labels for the data point as an array
kmeans.labels_

#K-means used for feature extraction on unseen data (not used atm)
y_pred = kmeans.predict(dfc)

#Linear dimensionality reduction using Principal component analysis (PCA)
X_prime = decomposition.PCA(n_components=2).fit_transform(dfc)

#Plot the results from the model
plt.subplot(221)
plt.scatter(X_prime[:, 0], X_prime[:, 1], c=kmeans.labels_)
plt.title("Clustered Attribute Row Data by Colours")



#np.shape(X_prime)

