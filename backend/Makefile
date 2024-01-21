#dev
# Path: Makefile
# Dev start flask and react
dev:
	@echo "Starting dev server"
	@echo "Starting flask server"
	@flask --debug run --port 5002 

# install
# Path: Makefile
# Install all dependencies usinf npm and pipenv
install:
	@echo "Installing pipenv dependencies"
	@pipenv install

# prod
# Path: Makefile
# Start production server, bind on 0.0.0.0, run wiht a production server
prod:
	@echo "Starting production server"
	@echo "Starting flask server"
	@pipenv run python3 app.py --host 0.0.0.0