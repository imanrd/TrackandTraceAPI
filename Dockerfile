# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TrackandTraceAPI.settings

# Create and set the working directory
WORKDIR /usr/src/TrackandTraceAPI

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


RUN python TrackandTraceAPI/manage.py migrate


RUN python TrackandTraceAPI/manage.py import_data


EXPOSE 8000


CMD ["python", "TrackandTraceAPI/manage.py", "runserver", "0.0.0.0:8000"]
