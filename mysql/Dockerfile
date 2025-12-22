FROM mysql:8.0

# Umgebungsvariablen
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=weather_db
ENV MYSQL_ALLOW_EMPTY_PASSWORD=no
ENV MYSQL_HOST=weather_sql_container

WORKDIR /mysql

# CSV und SQL-Skripte kopieren
COPY data/raw/weatherAUS.csv /mysql/data/weatherAUS.csv
COPY mysql/create_table.sql /docker-entrypoint-initdb.d/1_create_table.sql
COPY mysql/import_data.sql /docker-entrypoint-initdb.d/2_import_data.sql

# MySQL so starten, dass CSV-Import erlaubt ist
CMD ["mysqld", "--secure-file-priv=/mysql/data", "--local-infile=1"]

EXPOSE 3306