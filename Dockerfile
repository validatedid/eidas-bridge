# Use an official Python runtime as a parent image
FROM python:3.7-alpine

# Set the working directory to /code
WORKDIR /code

# Copy the current directory contents into the container at /app
COPY . /code

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget curl
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt -r requirements.demo.txt \
    && pip3 install --no-cache-dir -e . \
    && apk del gcc build-dependencies

CMD ["python3", "start.py"]