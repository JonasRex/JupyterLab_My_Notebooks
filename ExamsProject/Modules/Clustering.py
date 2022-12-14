import pandas as pd
from sklearn.preprocessing import StandardScaler as SS # z-score standardization 
from sklearn.cluster import KMeans, DBSCAN # clustering algorithms
from sklearn.decomposition import PCA # dimensionality reduction
from sklearn.metrics import silhouette_score # used as a metric to evaluate the cohesion in a cluster
from sklearn.neighbors import NearestNeighbors # for selecting the optimal eps value when using DBSCAN
import numpy as np

# plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.cluster import SilhouetteVisualizer

def silhouettePlot(range_, data):
    """we will use this function to plot a silhouette plot that helps us to evaluate the cohesion in clusters (k-means only)"""
    half_length = int(len(range_)/2)
    range_list = list(range_)
    fig, ax = plt.subplots(half_length, 2, figsize=(15,8))
    for _ in range_:
        kmeans = KMeans(n_clusters=_, random_state=42)
        q, mod = divmod(_ - range_list[0], 2)
        sv = SilhouetteVisualizer(kmeans, colors="yellowbrick", ax=ax[q][mod])
        ax[q][mod].set_title("Silhouette Plot with n={} Cluster".format(_))
        sv.fit(data)
    fig.tight_layout()
    fig.show()

def elbowPlot(range_, data, figsize=(10,10)):
    """the elbow plot function helps to figure out the right amount of clusters for a dataset"""
    inertia_list = []
    for n in range_:
        kmeans = KMeans(n_clusters=n, random_state=42)
        kmeans.fit(data)
        inertia_list.append(kmeans.inertia_)
        
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    sns.lineplot(y=inertia_list, x=range_, ax=ax)
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Inertia")
    ax.set_xticks(list(range_))
    fig.show()

def findOptimalEps(n_neighbors, data):
    neigh = NearestNeighbors(n_neighbors=n_neighbors)
    nbrs = neigh.fit(data)
    distances, indices = nbrs.kneighbors(data)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)


def progressiveFeatureSelection(df, n_clusters=3, max_features=4,):
    """Never used!"""
    feature_list = list(df.columns)
    selected_features = list()
    # select starting feature
    initial_feature = ""
    high_score = 0
    for feature in feature_list:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        data_ = df[feature]
        labels = kmeans.fit_predict(data_.to_frame())
        score_ = silhouette_score(data_.to_frame(), labels)
        #print("Proposed new feature {} with score {}". format(feature, score_))
        if score_ >= high_score:
            initial_feature = feature
            high_score = score_
    #print("The initial feature is {} with a silhouette score of {}.".format(initial_feature, high_score))
    feature_list.remove(initial_feature)
    selected_features.append(initial_feature)
    for _ in range(max_features-1):
        high_score = 0
        selected_feature = ""
        #print("Starting selection {}...".format(_))
        for feature in feature_list:
            selection_ = selected_features.copy()
            selection_.append(feature)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            data_ = df[selection_]
            labels = kmeans.fit_predict(data_)
            score_ = silhouette_score(data_, labels)
            #print("Proposed new feature {} with score {}". format(feature, score_))
            if score_ > high_score:
                selected_feature = feature
                high_score = score_
        selected_features.append(selected_feature)
        feature_list.remove(selected_feature)
        #print("Selected new feature {} with score {}". format(selected_feature, high_score))
    return selected_features


def standardized(df):
    scaler = SS()
    DNP_artists_standardized = scaler.fit_transform(df.drop("Name",axis=1))
    df_artists_standardized = pd.DataFrame(DNP_artists_standardized, columns=["main_artist_standardized","featuring_artist_standardized","songwriter_standardized"])
    return df_artists_standardized.set_index(df.index)


def print_elbow_plot(df_standardized_sliced):
    return elbowPlot(range(1,11), df_standardized_sliced)

def print_silhouette_plot(df_standardized_sliced):
    return silhouettePlot(range(3,9), df_standardized_sliced)


def make_bar_chart_of_cluster(cluster_df):
    names = cluster_df["Name"].tolist()
    main = cluster_df["Main Artist"].tolist()
    feature = cluster_df["Featuring Artist"].tolist()
    writer = cluster_df["Writer"].tolist()


    barWidth = 0.25
    fig = plt.subplots(figsize =(18, 12))
    
    br1 = np.arange(len(main))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, main, color ='r', width = barWidth,
            edgecolor ='grey', label ='Main')
    plt.bar(br2, feature, color ='g', width = barWidth,
            edgecolor ='grey', label ='Featuring')
    plt.bar(br3, writer, color ='b', width = barWidth,
            edgecolor ='grey', label ='Writer')
    
    # Adding Xticks
    plt.xlabel('Arists', fontweight ='bold', fontsize = 15)
    plt.ylabel('Entries on the charts', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(main))],names, rotation=45, horizontalalignment='right',fontweight='light') 
    
    plt.legend()
    plt.show()

