import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [movieDetails, setMovieDetails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const fetchMovieDetails = async (imdbIDs) => {
    try {
      const movieDetailsResponses = await Promise.all(
        imdbIDs.map(imdbID => 
          axios.get(`http://www.omdbapi.com/?i=${imdbID}&apikey=${process.env.REACT_APP_OMDB_API_KEY}`)
        )
      );
      return movieDetailsResponses.map(response => response.data);
    } catch (error) {
      console.error('Error fetching movie details:', error);
      setError('Error fetching movie details');
      return [];
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const recommendationsResponse = await axios.post(process.env.REACT_APP_RECOMMENDATIONS_API_URL, { userInput: inputValue });
      const imdbIDs = recommendationsResponse.data.map(movie => movie.imdbID);
      const moviesDetails = await fetchMovieDetails(imdbIDs);
      setRecommendedMovies(recommendationsResponse.data);
      setMovieDetails(moviesDetails);
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      setError('Error fetching recommendations');
    }
    setLoading(false);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-4">Movie Recommender</h1>
      <form onSubmit={handleSubmit} className="mb-4 flex justify-center">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          className="border border-gray-300 p-2 rounded mr-2"
          placeholder="Enter movie title..."
        />
        <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Search
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {recommendedMovies.length > 0 && (
        <div>
          <h2 className="text-xl font-bold">Search Result:</h2>
          <MovieDetail movie={movieDetails[0]} />
          <h2 className="text-xl font-bold mt-4">Recommendations:</h2>
          <div>
            {movieDetails.slice(1).map((movie, index) => (
              <MovieDetail key={movie.imdbID} movie={movie} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function MovieDetail({ movie }) {
  if (!movie) return null;

  return (
    <div className="flex flex-col md:flex-row items-center my-4">
      <img src={movie.Poster} alt={movie.Title} className="w-full md:w-1/4"/>
      <div className="md:ml-4">
        <h3 className="text-lg font-bold">{movie.Title} ({movie.Year})</h3>
        <p><strong>Actors:</strong> {movie.Actors}</p>
        <p><strong>Genres:</strong> {movie.Genre}</p>
        <p><strong>Description:</strong> {movie.Plot}</p>
      </div>
    </div>
  );
}

export default App;
