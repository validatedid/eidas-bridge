# Use an official Python runtime as a parent image
# FROM python:3.7-alpine

# Set the working directory to /code
# WORKDIR /code

# Copy the current directory contents into the container at /app
# COPY . /code

# CMD ["python", "/code/demo/hub_server.py"]

# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["hub_server.py"]