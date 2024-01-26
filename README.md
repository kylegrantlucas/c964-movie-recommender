# Quick-Start Guide

## Interactive Data Visualizations on Google Colab:

To produce the Data Visualizations, navigate to:

https://colab.research.google.com/github/kylegrantlucas/c964-movie-recommender/blob/main/visualizations/Visualizations.ipynb

You can then hit ‘run all,’ producing the expected visualizations.

##	Using the Online Recommender System:

To use the hosted online recommender system, navigate to:

https://nimble-cascaron-a10677.netlify.app/

There, you will see the web app frontend, where you can enter movies and interact with the application. I’d recommend some classics such as “Titanic,” “Armageddon,” “Jurassic Park” or “Anchorman.”

##	Running on a Local Environment:

Running on a local environment requires the use of Docker (https://docs.docker.com/engine/install/)

* Install Docker following the above guide.
* Build the docker container.
* Open a terminal.
    * Navigate to the root directory of the c964-movie-recommender project.
    * Run the build command.

    You can build the container by running the following command in your terminal:

    `docker build -t c964-movie-recommender .`

* Run the Docker container.

   You can then run the container by running the following in your terminal:

   `docker run -p 3000:3000 -p 5002:5002 -d c964-movie-recommender`

* Navigate to the local application.

Go to http://localhost:3000 in a web browser to see the front end of the Movie Recommender application.

