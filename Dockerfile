# Define base image
FROM continuumio/miniconda3:latest

# Set working directory for the project
WORKDIR /app/scripts

# Update conda
RUN conda update -n base -c defaults conda

# Install v0.5.2 version of pyCSEP
RUN conda install --channel conda-forge pycsep=0.5.2

# Copy everything but the data into Docker container
COPY ./scripts /app/scripts

