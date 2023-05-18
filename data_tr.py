import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

class DataTreatment:
    def __init__(self):
        self.SEED = 1224
        np.random.seed(self.SEED)

        data = pd.read_csv("./data/dados_totais.csv")
        data = data.drop(["explicit", "key", "mode"], axis=1)

        data_genres = pd.read_csv("./data/data_by_genres.csv")
        data_genres = data_genres.drop(["key", "mode"], axis=1)

        data_year = pd.read_csv("./data/data_by_year.csv")
        data_year = data_year[data_year["year"] >= 2000]
        data_year = data_year.drop(["key", "mode"], axis=1)

        self.data = data
        self.data_genres = data_genres
        self.data_year = data_year

    def clustering_by_genre(self):
        data_genres1 = self.data_genres.drop('genres', axis=1)

        pca_pipeline = Pipeline(
            [('scaler', StandardScaler()), ('PCA', PCA(n_components=2, random_state=self.SEED))])

        genre_embedding_pca = pca_pipeline.fit_transform(data_genres1)
        projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding_pca)

        kmeans_pca = KMeans(n_clusters=5, verbose=True, random_state=self.SEED)

        kmeans_pca.fit(projection)

        self.data_genres['cluster_pca'] = kmeans_pca.predict(projection)
        projection['cluster_pca'] = kmeans_pca.predict(projection)

        projection['genres'] = self.data_genres['genres']

        return self.data_genres, projection


    def ploting_cluster_by_genre(projection):
        import plotly.express as px

        fig = px.scatter(projection, x='x', y='y',
                        color='cluster_pca', hover_data=['x', 'y', 'genres'])
        fig.show()


    def main_clustering(self):
        from sklearn.preprocessing import OneHotEncoder

        ohe = OneHotEncoder(dtype=int)
        colunas_ohe = ohe.fit_transform(self.data[['artists']]).toarray()

        data2 = self.data.drop('artists', axis=1)

        data_dummie = pd.concat([data2, pd.DataFrame(
            colunas_ohe, columns=ohe.get_feature_names_out(['artists']))], axis=1)
        data_dummie

        pca_pipeline = Pipeline(
            [('scaler', StandardScaler()), ('PCA', PCA(n_components=0.7, random_state=self.SEED))])

        music_embedding_pca = pca_pipeline.fit_transform(
            data_dummie.drop(['id', 'name', 'artists_song'], axis=1))
        projection_m = pd.DataFrame(data=music_embedding_pca)

        kmeans_pca_pipeline = KMeans(
            n_clusters=50, verbose=False, random_state=self.SEED, n_init='auto')

        kmeans_pca_pipeline.fit(projection_m)

        self.data['cluster_pca'] = kmeans_pca_pipeline.predict(projection_m)
        projection_m['cluster_pca'] = kmeans_pca_pipeline.predict(projection_m)

        projection_m['id'] = self.data['id']
        projection_m['artist'] = self.data['artists']
        projection_m['song'] = self.data['artists_song']

        return projection_m

    def ploting_main_cluster(projection):
        import plotly.express as px

        fig = px.scatter_3d(
            projection, x=0, y=1, z=2, color='cluster_pca', hover_data=['song'])
        fig.update_traces(marker_size=2)
        fig.show()

    def search_by_artist(self, artist_to_search):
        print(self.data[self.data['artists'] == artist_to_search]['artists_song'])
