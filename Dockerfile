FROM python:3.12.4

ARG SECRET_KEY
ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PORT
ARG DB_PASS

ENV SECRET_KEY=$SECRET_KEY
ENV DB_HOST=$DB_HOST
ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PORT=$DB_PORT
ENV DB_PASS=$DB_PASS

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin123
ENV DJANGO_SUPERUSER_EMAIL=admin@email.com

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs
RUN npm install -g tailwindcss

RUN python film_store/manage.py tailwind install
RUN python film_store/manage.py tailwind build
RUN python film_store/manage.py collectstatic --noinput
RUN python film_store/manage.py makemigrations && \
    python film_store/manage.py migrate && \
    python film_store/manage.py seed_if_no_superuser && \
    python film_store/manage.py create_superuser_if_not_exists

# Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8000

CMD ["sh", "-c", "cd film_store && gunicorn film_store.wsgi:application --bind 0.0.0.0:8001 --workers 2 --threads 4 & nginx -g 'daemon off;'"]
