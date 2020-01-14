# Use an official Python runtime as a parent image
FROM python:3.7
COPY . /server
WORKDIR /server
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["hub_server.py"]