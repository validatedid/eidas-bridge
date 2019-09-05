# Use an official PHP with apache and Ubuntu 18.04 runtime as a parent image. 
# It only needs to ad python3 and the addtional libraries for executing the demo
FROM php:apache-buster

# Copy the web files contents to apache directory
COPY demo /var/www/html/

RUN mkdir code

# Copy the current directory contents into the container at /code
COPY . /code

# Set the working directory to /code
WORKDIR /code

RUN apt-get update -y && \
	apt-get install -y --no-install-recommends \
	python3 \
	python3-pip \
	python3-setuptools \
    openssl ca-certificates python-openssl && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
	-r requirements.txt \
	-r requirements.demo.txt

RUN pip3 install --no-cache-dir -e .

# Start apache server
ADD ./scripts/start.sh /start.sh
RUN chmod 0755 /start.sh
CMD ["bash", "/start.sh"]