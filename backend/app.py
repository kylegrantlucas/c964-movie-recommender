# main entrypoint for our Flask app
from flask import Flask, request, Blueprint
from flask_cors import CORS
import pandas as pd
from recommender import Recommender         

recommender: Recommender
bp = Blueprint('main', __name__)

@bp.route('/recommendations', methods=['POST'])
def recommendations():
    # Get data from request JSON
    data = request.get_json()
    user_input = data.get('userInput')

    recommendations: pd.DataFrame = recommender.recommend_movies(user_input)
    return recommendations.to_json(orient='records')


def initialize():
    global recommender # Add the global keyword to indicate that "data" is a global variable
    data = pd.read_csv('https://raw.githubusercontent.com/kylegrantlucas/c964-movie-recommender/main/backend/data/imdb.csv')
    recommender = Recommender(data)

def create_app():
    app = Flask(__name__)
    
    # enable CORS
    CORS(app, resources={r"/recommendations": {"origins": ["http://localhost:3000", "https://c964-frontend.fly.dev", "https://nimble-cascaron-a10677.netlify.app"]}})

    # initialize our recommender
    with app.app_context():
        initialize()

    # register our route blueprint
    app.register_blueprint(bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
