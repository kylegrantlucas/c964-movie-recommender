# unit testing for our data model
# Path: backend/tests/test_recommender.py
import pytest
import pandas as pd

from recommender import Recommender

@pytest.fixture
def recommender():
    data = pd.read_csv('https://raw.githubusercontent.com/kylegrantlucas/c964-movie-recommender/main/backend/data/imdb.csv')
    recommender = Recommender(data)
    return recommender

def test_init():
    assert recommender is not None
    
def test_preprocess_data(recommender):
    assert recommender.data is not None

def test_generate_features(recommender):
    assert recommender.features is not None
    
def test_train_model(recommender):
    assert recommender.knn is not None
    
def test_recommend_movies(recommender):
    assert recommender.recommend_movies('The Matrix') is not None

def test_recommend_movies_invalid_input(recommender):
    with pytest.raises(IndexError):
        recommender.recommend_movies('Invalid Movie Title')
        
# now lets get a little more involved and set some unit tests to ensure the model meets expectations
test_data = [
    {
        'input': 'The Matrix',
        'output': [
            'The Matrix',
            'Universal Soldier: The Return',
            'The Thirteenth Floor',
            'Batman & Robin',
            'Der Schuh des Manitu',
            'Barb Wire'
        ]
    },
    {
        'input': 'Universal Soldier: The Return',
        'output': [
            'Universal Soldier: The Return',
            'The Matrix',
            'Batman & Robin',
            'The Thirteenth Floor',
            'Der Schuh des Manitu',
            'Barb Wire'
        ]
    },
    {
        'input': 'The Thirteenth Floor',
        'output': [
            'The Thirteenth Floor',
            'The Astronaut\'s Wife',
            'The Matrix',
            'Universal Soldier: The Return',
            'GATTACA',
            'Batman & Robin',
        ]
    },
    {
        'input': 'Batman & Robin',
        'output': [
            'Batman & Robin',
            'Barb Wire',
            'Universal Soldier: The Return',
            'The Matrix',
            'The Arrival',
            'The Thirteenth Floor',
        ]
    }
]

@pytest.mark.parametrize('test', test_data)
def test_evaluate_model(test, recommender):
    recommendations = recommender.recommend_movies(test['input'])
    titles = recommendations['originalTitle'].tolist()
    assert titles == test['output']
    
# now lets evaulte the f1 score of our model
@pytest.mark.parametrize('test', test_data)
def test_evaluate_model_f1(test, recommender):
    recommendations = recommender.recommend_movies(test['input'])
    titles = recommendations['originalTitle'].tolist()
    f1 = recommender.f1_score(test['output'], titles)
    assert f1 > 0.5
    