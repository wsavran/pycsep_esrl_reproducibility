# Define base image
FROM continuumio/miniconda3:4.11.0

# Create non-root user using default values
ARG CONDA_ENV=pycsep-esrl
ARG USERNAME=csep-user
ARG USER_UID=1100
ARG USER_GID=$USER_UID
RUN groupadd --non-unique -g $USER_GID $USERNAME \
    && useradd -u $USER_UID -g $USER_GID -s /bin/sh -m $USERNAME

# Register default conda environment
ENV CONDA_DEFAULT_ENV=$CONDA_ENV

# Set working directory for the project
WORKDIR /app/

# Add environment files and run scripts to working directory
# (just in case: convert Windows CRLF line endings to Unix LF, if present)
COPY --chown=$USER_UID:$USER_GID environment.yml entrypoint.sh ./
RUN ["sed", "-i", "s/\r$//", "entrypoint.sh"]

# Create and add to path and add things to shell
USER $USERNAME
RUN conda env create -f environment.yml
ENV PATH ~/envs/$CONDA_ENV/bin:$PATH
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate pycsep-env" >> ~/.bashrc
# switch shell sh (default in Linux) to bash
SHELL ["/bin/bash", "-c", "-l"]

# Copy everything but the data into Docker container using non-priviledged user
COPY --chown=$USER_UID:$USER_GID ./scripts /app/scripts/

# Make Dockerfile runnable
ENTRYPOINT ["./entrypoint.sh"]
