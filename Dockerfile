ARG BASE_CONTAINER=python:3.10.2
FROM $BASE_CONTAINER as build

WORKDIR /usr/app
WORKDIR /usr/app


RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential gcc libpcre3 libpcre3-dev \
  python3-dev default-libmysqlclient-dev libopenblas-dev

RUN pip install --upgrade pip setuptools wheel eztools
RUN pip install cmake
RUN pip install numpy
RUN python -m venv greykite-env
RUN /bin/bash -c "source greykite-env/bin/activate"
RUN pip install django-tailwind
RUN pip install 'django-tailwind[reload]'

RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"
RUN pip install greykite

COPY requirements.txt .
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "tailwind", "init" "&&", "python", "manage.py", "tailwind", "install" ]

FROM python:3.10.2
ENV PATH="/usr/app/venv/bin:$PATH"

RUN useradd uwsgi
WORKDIR /usr/app

COPY --from=build /usr/app/venv ./venv
COPY . .


CMD [ "python", "manage.py", "runserver"]
