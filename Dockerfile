# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS dependencies for our mini VM
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini VM's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

# Set the Python path so Django can find your custom apps
ENV PYTHONPATH="/code"

# Copy the project code into the container's working directory
COPY ./src /code

# Set build-time arguments and environment variables
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# Collect static files
RUN python manage.py collectstatic --noinput

# Set the Django default project name
ENV PROJ_NAME="saashome"

# Create a bash script to run the Django project
# This script will execute at runtime when the container starts
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "gunicorn saashome.wsgi:application --bind \"[::]:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# Make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runtime script when the container starts
CMD ./paracord_runner.sh