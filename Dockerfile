FROM python:3.9-alpine3.13
LABEL maintainer="akotronis@gmail.com"

# See python output directly to the console
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app

WORKDIR /app

EXPOSE 8000

# Overriden to true in docker-compose
ARG DEV=false

# 1 - One run command to avoid creating many layers
#     and keep the setup lightweight
# 2 - Create venv for edge cases were base image
#     dependencies may conflict with the project
RUN python -m venv /py && \
    # Upgrate pip inside virtual environment
    /py/bin/pip install --upgrade pip && \
    # Install required alpine specific packages for Postgres
    apk add --update --no-cache postgresql-client && \
    # Use -- virtual to be able to remove them later
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # Install dependencies inside virtual environment
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Shell script logic to install dev requirements only on dev environment
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # Remove files/folders we don't need, when 
    # creating an image
    rm -rf /tmp && \
    # Remove alpine specific Postgres dependencies that required
    # only for pyscopg2 installation
    apk del .tmp-build-deps && \
    # Add user: Best practice NOT to use the root user
    # DON'T run app the app using the root user
    # if hacked, the attacker will have access to
    # everything in the container
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Run python commands directly from virtual environment
ENV PATH="/py/bin:$PATH"

# Specify the user we are switching to
USER django-user