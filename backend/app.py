# # main entrypoint for our Flask app
# # it will serve as an interactive front end for our movie recommender system
from flask import Flask, render_template, request
from flask_cors import CORS
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pandas as pd         

data: pd.DataFrame 
knn: NearestNeighbors
features: pd.DataFrame

def initialize():
    global data, knn, features  # Add the global keyword to indicate that "data" is a global variable
    data = pd.read_csv('https://raw.githubusercontent.com/kylegrantlucas/c964-movie-recommender/main/backend/data/imdb.csv')
    # Assuming 'data' is your DataFrame
    df = data.copy()  # Work with a copy to avoid SettingWithCopyWarning

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

    # Prepare the feature matrix
    features = pd.concat([df[['genre_id', 'startYear']], df[['normalized_score']]], axis=1)

    data = df

    # KNN Model
    knn = NearestNeighbors(n_neighbors=6, metric='minkowski')
    knn.fit(features)


def recommend_movies(user_input: str):
    global data, knn, features  # Add the global keyword to indicate that "data" is a global variable
    df = data.copy()  # Work with a copy to avoid SettingWithCopyWarning
    # fuzzy search for movie title
    movie_index = df[df['originalTitle'].str.contains(user_input, case=False)].index[0]
    input_feature_values = features.iloc[movie_index].values.reshape(1, -1)
    input_features = pd.DataFrame(input_feature_values, columns=features.columns)  # Use the same column names

    # Predict using KNN
    distances, indices = knn.kneighbors(input_features)

    # Print the recommendations
    recommended_movies: pd.DataFrame = df.iloc[indices[0][0:]][['imdbID', 'originalTitle', 'genres', 'startYear', 'averageRating', 'numVotes']]
    return recommended_movies

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/recommendations": {"origins": ["http://localhost:3000", "https://c964-frontend.fly.dev"]}})


    with app.app_context():
        initialize()

    return app

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    if request.method == 'POST':
        user_input = request.form['userInput']
        recommendations = recommend_movies(user_input).to_dict(orient='records')
    return render_template('home.html', recommendations=recommendations)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Get data from request JSON
    data = request.get_json()
    user_input = data.get('userInput')

    recommendations: pd.DataFrame = recommend_movies(user_input)
    return recommendations.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)