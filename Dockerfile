# Define base image
FROM continuumio/miniconda3

# Set working directory for the project
WORKDIR /app/scripts

# Install v0.5.1 version of pyCSEP
RUN conda install --channel conda-forge pycsep=0.5.2

# Copy everything into Docker container
COPY ./scripts /app/scripts

