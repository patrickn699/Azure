FROM python:3.10.15-slim-bullseye

WORKDIR /var/tmp

COPY requirements.txt ./

RUN  apt-get update && apt-get install -y \
            apt-transport-https \
            ca-certificates \
            curl \
            pkg-config \
            libmariadb-dev \
            build-essential  && pip install --no-cache-dir -r requirements.txt 

COPY . .

EXPOSE 8010

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT [ "python", "-m" , "flask", "run", "--host=0.0.0.0" ]