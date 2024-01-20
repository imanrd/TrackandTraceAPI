
FROM python:3.9


ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TrackandTraceAPI.settings


WORKDIR /usr/src/TrackandTraceAPI


COPY . .


RUN pip install -r requirements.txt


RUN python TrackandTraceAPI/manage.py migrate


RUN python TrackandTraceAPI/manage.py import_data


EXPOSE 8000


CMD ["python", "TrackandTraceAPI/manage.py", "runserver", "0.0.0.0:8000"]
