FROM python:3.7.0

# Need sudo
RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app
RUN pip install --upgrade pip==20.1.1
RUN pip install -e .
RUN pip install tox

# for releases
RUN pip install twine 
