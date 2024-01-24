# class to contain the model preprocessing and prediction
from ast import mod
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

class Recommender:
    data = pd.DataFrame()
    features = pd.DataFrame()
    knn = NearestNeighbors()
    
    def __init__(self, data: pd.DataFrame):
        self.data = self.preprocess_data(data)
        self.features = self.generate_features()
        self.knn = self.train_model()
    
    def model_precision(self):
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 2, 1, 0, 0, 1]

        # Calculate precision
        precision = precision_score(y_true, y_pred, average='micro')
        
        return precision

    def model_recall(self):
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 2, 1, 0, 0, 1]

        # Calculate recall
        recall = recall_score(y_true, y_pred, average='micro')
        
        return recall
    
    # def model_f1_score(self):
    #     y_true = [0, 1, 2, 0, 1, 2]
    #     y_pred = [0, 2, 1, 0, 0, 1]

    #     # Calculate F1 score
    #     precision: Float = self.model_precision()
    #     recall = self.model_recall()
        
    #     f1 = 2 * (precision * recall) / (precision + recall)
        
    #     return f1
    
    def f1_score(self, true_recommendations: list, recommended_movies: list) -> float:
        # convert to sets
        true_recommendations_set = set(true_recommendations)
        recommended_movies_set = set(recommended_movies)
        
        # Calculate precision and recall
        tp = len(true_recommendations_set.intersection(recommended_movies_set))
        precision = tp / len(recommended_movies_set)
        recall = tp / len(true_recommendations_set)
        
        """A function to calculate the F1 score"""
         # Calculate average precision, recall, and F1 score
        f1 = 2 * (precision * recall) / (precision + recall)

        return f1
        
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy() # Work with a copy to avoid SettingWithCopyWarning

        # Exclude movies with 0.0 score and '\N' values
        df = df[(df['averageRating'] > 0.0) & (df['startYear'] != '\\N') & (df['genres'] != '\\N')]

        # Sort and deduplicate genres
        df['genres'] = df['genres'].str.split(',').apply(lambda x: sorted(x)).apply(lambda x: ','.join(x))
            
        # exclude numVotes < 5000
        df = df[df['numVotes'] > 20000]
            
        # reset index after dropping rows
        df = df.reset_index(drop=True)

        # Convert genres to unique numerical identifiers
        unique_genres = df['genres'].unique()
        genre_to_id = {genre: idx for idx, genre in enumerate(unique_genres)}
        df['genre_id'] = df['genres'].map(genre_to_id)
        
        # Normalize scores
        scaler = MinMaxScaler()
        df['normalized_score'] = scaler.fit_transform(df[['averageRating']])
    
        return df
     
    def generate_features(self) -> pd.DataFrame:
        # Prepare the feature matrix
        features = pd.concat([self.data[['genre_id', 'startYear']], self.data[['normalized_score']]], axis=1)
        
        return features

    def train_model(self):
        # KNN Model
        knn = NearestNeighbors(n_neighbors=6, metric='minkowski')
        knn.fit(self.features)
        
        return knn
     
    def recommend_movies(self, user_input: str):
        df = self.data.copy()  # Work with a copy to avoid SettingWithCopyWarning
        # fuzzy search for movie title
        movie_index = df[df['originalTitle'].str.contains(user_input, case=False)].index[0]
        input_feature_values = self.features.iloc[movie_index].values.reshape(1, -1)
        input_features = pd.DataFrame(input_feature_values, columns=self.features.columns)  # Use the same column names

        # Predict using KNN
        distances, indices = self.knn.kneighbors(input_features)

        # Print the recommendations
        recommended_movies: pd.DataFrame = df.iloc[indices[0][0:]][['imdbID', 'originalTitle', 'genres', 'startYear', 'averageRating', 'numVotes']]
        return recommended_movies