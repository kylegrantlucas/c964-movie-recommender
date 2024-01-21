# Basic React app
FROM node:21-alpine
LABEL maintainer="Kyle Lucas"

# Install GCC
RUN apk add --no-cache make

# Copy project except for .env
COPY . /app

WORKDIR /app

# install pipenv
RUN npm install -g serve

# Install dependencies
# can use Make
RUN make install

# Expose port
EXPOSE 3000

# Run the app
CMD ["make", "prod"]