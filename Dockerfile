# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app


# Copy the requirements file into the container
COPY requirements.txt .
COPY airport_rsvp.py .
COPY make_ddb_tables.py .

# Install the required dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y cmake
# Set environment variables for AWS access and secret keys
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# Expose the default port for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "airport_rsvp.py"]
