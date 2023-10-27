# Use the official Python image as the base image
FROM python3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY python/airport_rsvp.py .

# Install the required dependencies
RUN pip install -r requirements.txt

# Set environment variables for AWS access and secret keys
ENV AWS_ACCESS_KEY_ID=your-access-key-id
ENV AWS_SECRET_ACCESS_KEY=your-secret-access-key

# Expose the default port for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "airport_rsvp.py"]
