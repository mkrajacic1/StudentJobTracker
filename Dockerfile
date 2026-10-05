FROM python:3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

RUN useradd app
USER app

CMD ["scrape"]