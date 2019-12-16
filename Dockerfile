FROM rickl/docker-scrapy

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
