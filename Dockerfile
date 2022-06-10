# Define base image
FROM continuumio/miniconda3:4.11.0 

# Create user using default values 
ARG USERNAME=csep-user
ARG USER_UID=1100
ARG USER_GID=$USER_UID
RUN groupadd -g $USER_GID $USERNAME \
    && useradd -u $USER_UID -g $USER_GID -s /bin/sh -m $USERNAME
USER $USERNAME

# Set working directory for the project
WORKDIR /app/

# Add environment files and run scripts to working directory
COPY --chown=$USER_UID:$USER_GID environment.yml .
COPY --chown=$USER_UID:$USER_GID entrypoint.sh .

# Create and activate environment for pyCSEP in all subsequent commands
RUN conda env create -f environment.yml 

# Copy everything but the data into Docker container using non-priviledged user 
COPY --chown=$USER_UID:$USER_GID ./scripts /app/scripts/

# Make Dockerfile runnable
ENTRYPOINT ["./entrypoint.sh"]
