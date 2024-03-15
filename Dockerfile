ARG BASE_CONTAINER=python:3.9.12
FROM $BASE_CONTAINER as build

WORKDIR /usr/app

RUN python -m venv greykite-env
RUN /bin/bash -c "source greykite-env/bin/activate"
WORKDIR /usr/app/greykite-env
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential gcc libpcre3 libpcre3-dev \
  python3-dev default-libmysqlclient-dev libopenblas-dev \
  ca-certificates curl gnupg
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel eztools
RUN pip install cmake numpy
RUN pip install greykite
COPY . .
RUN pip install -r requirements.txt
RUN pip install django-tailwind 'django-tailwind[reload]'
ENV PYTHONUNBUFFERED 1

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
