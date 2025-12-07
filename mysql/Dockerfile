FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=weather_db

WORKDIR /mysql

COPY create_table.sql /docker-entrypoint-initdb.d/

COPY data/weatherAUS.csv /mysql/data/weatherAUS.csv

COPY import_data.sql /docker-entrypoint-initdb.d/

EXPOSE 3306