# Define base image
FROM continuumio/miniconda3

# Set working directory for the project
WORKDIR /app

# Install v0.5.1 version of pyCSEP
RUN conda install --channel conda-forge pycsep=0.5.1

# Copy everything into Docker container
COPY ./scripts /app/scripts

