# load a python image
FROM python:3.12.1-alpine

# copy all app files
COPY . /app

# set the working directory
WORKDIR /app

# install nodejs, pandas, scikit-learn requirements
RUN apk add --update nodejs npm gcc g++ gfortran cmake make openblas-dev libffi-dev openssl-dev
# install the requirements
RUN pip install -r /app/backend/requirements.txt

# copy the frontend files to the working directory
WORKDIR /app/frontend

# npm install
RUN npm install

# build the frontend
RUN npm run build

# install serve
RUN npm install -g serve

# expose the port
EXPOSE 5002
EXPOSE 3000

WORKDIR /app

# run the backend
CMD ["make", "start"]
