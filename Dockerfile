FROM python:3.10.8-alpine

EXPOSE 8000

RUN mkdir /drone_api && \
    apk upgrade --update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev && \
    pip install pipenv

COPY . /drone_api
WORKDIR /drone_api

RUN pipenv install -r requirements.txt

ENTRYPOINT ["gunicorn"]

CMD ["--workers=4", "app:drone_api"]

