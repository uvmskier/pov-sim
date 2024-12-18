# Use the official Python 3.8 image as the base image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /python-docker

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required dependencies
RUN pip3 install -r requirements.txt
RUN opentelemetry-bootstrap -a install

# Copy the rest of your application code into the container
COPY . .

# Specify the command to run your Flask app

#default command to run the app
#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

#run the app with auto instrumentation and write to console
CMD ["opentelemetry-instrument", "--traces_exporter", "console","--metrics_exporter","console","--logs_exporter","console","--service_name", "python-flight-app","flask", "run", "--host=0.0.0.0"]