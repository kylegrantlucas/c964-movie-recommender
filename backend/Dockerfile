# Basic Flask app
FROM python:3.11-alpine
LABEL maintainer="Kyle Lucas"

# Install GCC
RUN apk add --no-cache gcc musl-dev linux-headers g++ gfortran libffi-dev openssl-dev openblas openblas-dev make

# Copy project
COPY . /app

WORKDIR /app

# install pipenv
RUN pip install pipenv

# Install dependencies
# can use Make
RUN make install

# Expose port
EXPOSE 5002

# Run the app
CMD ["make", "prod"]