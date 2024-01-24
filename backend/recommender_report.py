from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
from recommender import Recommender

data = pd.read_csv('https://raw.githubusercontent.com/kylegrantlucas/c964-movie-recommender/main/backend/data/imdb.csv')
recommender = Recommender(data)

# create a list of all movie titles, we'll limit this dataset to 1000 movies, sorted by votes
movie_list = data.sort_values(by=['numVotes'], ascending=False)['originalTitle'].head(1000).tolist()

test_data = {
    'originalTitle': ['Creed III', 'Avatar: The Way of Water', 'Turning Red'],
    'known_recommendations': [
        ["Creed III", "Air", "Evil Dead Rise", "Cuando acecha la maldad", "The Exorcist: Believer", "Winnie-the-Pooh: Blood and Honey"],  # Expanded recommendations for 'Creed III'
        ["Avatar: The Way of Water", "Karthikeya 2", "Doctor Strange in the Multiverse of Madness", "Black Adam", "Brahmastra Part One: Shiva", "Shang-Chi and the Legend of the Ten Rings"],  # For 'Avatar: The Way of Water'
        ["The Bob's Burgers Movie", "Turning Red", "The Sea Beast", "Minions: The Rise of Gru", "Luck", "Puss in Boots: The Last Wish"]  # For 'The Super Mario Bros. Movie'
    ]
}

test_df = pd.DataFrame(test_data)

# gather model recommendations using the recommender system
model_recommendations = {}
for index, row in test_df.iterrows():
    model_recommendations[row['originalTitle']] = recommender.recommend_movies(row['originalTitle'])

# Function to convert recommendations to binary format
def convert_to_binary(recommendations, movie_list):
    binary_format = []
    for title in movie_list:
        binary_format.append(1 if title in recommendations else 0)
    return binary_format

# Convert both known and model recommendations to binary format
binary_known = []
binary_model = []
for index, row in test_df.iterrows():
    binary_known.append(convert_to_binary(row['known_recommendations'], movie_list))
    binary_model.append(convert_to_binary(model_recommendations[row['originalTitle']], movie_list))

binary_known = np.array(binary_known)
binary_model = np.array(binary_model)

# Calculate metrics
precision = precision_score(binary_known, binary_model, average='samples', zero_division=1)
recall = recall_score(binary_known, binary_model, average='samples', zero_division=1)
f1 = f1_score(binary_known, binary_model, average='samples', zero_division=1)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
