# Use an official Python runtime as the parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Download the necessary NLTK models and corpora
RUN python -m nltk.downloader vader_lexicon

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Command to run the application
CMD ["python", "./main.py"]
