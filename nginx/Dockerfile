FROM nginx:1.21-alpine

RUN apk add --no-cache certbot certbot-nginx bash

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./api.conf /etc/nginx/conf.d/api.conf
COPY ./frontend.conf /etc/nginx/conf.d/frontend.conf