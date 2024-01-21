#dev
# Path: Makefile
# Dev start flask and react
dev:
	@echo "Starting dev server"
	@echo "Starting flask server"
	@cd backend && flask --debug run --port 5002 &
	@echo "Starting react server"
	@cd frontend && npm start

# install
# Path: Makefile
# Install all dependencies usinf npm and pipenv
install:
	@echo "Installing dependencies"
	@echo "Installing pipenv dependencies"
	@cd backend && pipenv install
	@echo "Installing npm dependencies"
	@cd frontend && npm install
