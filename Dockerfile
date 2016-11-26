FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements-docker.txt && groupadd -r django && useradd -r -g django django
COPY . /app/
RUN chown -R django /app
