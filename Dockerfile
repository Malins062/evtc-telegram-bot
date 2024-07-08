# Use an official Python runtime as the base image
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /app/

ENV PIP_ROOT_USER_ACTION=ignore

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

# Copy the rest of the application code to the container
COPY . /app

# Set the entrypoint command to run your application
CMD ["python", "app.py"]