FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./reqs/requirements.txt /app/reqs/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/reqs/requirements.txt

# Copy the rest of the application code into the container
COPY . /app
