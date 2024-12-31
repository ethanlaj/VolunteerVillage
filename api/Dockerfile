# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
# Ensure you have a requirements.txt in your application's directory listing all your dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Set the FLASK_APP environment variable
ENV FLASK_APP=main.py

# Specify env variables as ARGs
ARG HH_DATABASE_URL
ARG AUTH0_CLIENT_SECRET
ARG FIREBASE_SERVICE_ACCOUNT_BASE64

# Expose the environment variables
ENV HH_DATABASE_URL=$HH_DATABASE_URL
ENV AUTH0_CLIENT_SECRET=$AUTH0_CLIENT_SECRET
ENV FIREBASE_SERVICE_ACCOUNT_BASE64=$FIREBASE_SERVICE_ACCOUNT_BASE64

# Expose the port where the app runs
EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]