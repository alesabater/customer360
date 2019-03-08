#Analytical model for customer segmentation
#Status of code's output: VALID WITH PLACEHOLDER DATA
#Overall code status: NEEDS REFINEMENT
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



#************PART 1*****************

#Select axes from two columns from Attributes table
x_axis_df = df['AVG_KWH_YEARLT']
y_axis_df = df['AVG_BILLING_YEARLY']

#Build array from column data
T = np.array(list(zip(x_axis_df, y_axis_df)))

#Plot current data points
plt.scatter(x_axis_df, y_axis_df)
plt.xlabel("AVG_KWH_YEARLT")
plt.ylabel("AVG_BILLING_YEARLY")
plt.title("Raw Data Points")

#Create Elbow Curve to choose right amount of clusters
distorsions = []
rng = range(1, 4) #Limited to 4 since only 4 rows are used rn
for k in rng:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(T)
    distorsions.append(kmeans.inertia_)

fig = plt.figure()
ex = fig.add_subplot(111)
ex.plot(rng, distorsions)
#plt.ylim([0, 45]) - to be used when more data is loaded
plt.xlabel("Number of Clusters")
plt.ylabel("Average Distortion")
plt.grid(True)
plt.title('Elbow curve')

#Create KMeans object with 2 clusters and pass T data
kmeans1 = KMeans(n_clusters=2, random_state=0).fit(T)

#List labels for the data point as an array and cluster centres
kmeans1.labels_
kmeans1.cluster_centers_

#Plot the results from the clustering
plt.subplot(221)
plt.xlabel("AVG_KWH_YEARLT")
plt.ylabel("AVG_BILLING_YEARLY")
plt.grid(True)
plt.scatter(T[:, 0], T[:, 1], c=kmeans1.labels_)
plt.title("Clustered Attribute Row Data by Colours")

#Highlight centroids in black
plt.scatter(kmeans1.cluster_centers_[:,0] ,kmeans1.cluster_centers_[:,1], color='black')
plt.title("Clustered Attribute Data (2 Columns) with Centroids")



#************PART 2*****************


#Get all values from all columns except "CREATION_DATE"
X = df.loc[:,[c for c in df.columns if c!="CREATION_DATE"]]

#Create Elbow Curve to choose right amount of clusters
distorsions = []
rng = range(1, 4) #Limited to 4 since only 4 rows are used rn
for k in rng:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    distorsions.append(kmeans.inertia_)

fig = plt.figure()
ex = fig.add_subplot(111)
ex.plot(rng, distorsions)
#plt.ylim([0, 45]) - to be used when more data is loaded
plt.xlabel("Number of Clusters")
plt.ylabel("Average Distortion")
plt.grid(True)
plt.title('Elbow curve')

#Create KMeans object with 2 clusters and pass X data
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

#List labels for the data point as an array and cluster centres
kmeans.labels_
kmeans.cluster_centers_

#Linear dimensionality reduction using Principal component analysis (PCA)
X_prime = decomposition.PCA(n_components=2).fit_transform(X)

#PCA array dimensions as a tuple (rows, columns)
np.shape(X_prime)

#Print PCA 2-dimensional aray
print(X_prime)

#Plot the results from the model
plt.subplot(221)
plt.scatter(X_prime[:, 0], X_prime[:, 1], c=kmeans.labels_)
plt.title("Clustered Attribute Row Data by Colours")

#Highlight centroids in black
plt.scatter(kmeans.cluster_centers_[:,0] ,kmeans.cluster_centers_[:,1], color='black')
plt.title("Clustered Attribute Row Data with Centroids")



#************PART 3*****************


#K-means used for feature extraction on 2 rows of new data
array = np.array([[5,800,5,6,900.2,8900.88,2012.1202,2018.0,1900.06], [6,600,50,2,2300.2,2500.88,2046.1202,2001.0,7700.06]])
kmeans.predict(array)