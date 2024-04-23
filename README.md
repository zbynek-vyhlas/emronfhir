## start project


- create `.env` file in the root of the project and add variables from `.env.example`
- create `.env.development.local` file in the `/client/frontend` directory and add variables from `.env.development.example`

### create postgres database

- install and start postgres service
- `psql` into the database
- create role (use role name and password from `.env` file)
  - `CREATE ROLE <role_name> WITH LOGIN PASSWORD '<your_password>' CREATEDB SUPERUSER;`
- create database (use database name and role name from `.env` file)
  - `CREATE DATABASE <database_name> WITH ENCODING='UTF8' OWNER=<role_name> CONNECTION LIMIT=30;`
- grant privileges (use database name and role name from `.env` file)
  - `GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <role_name>;`

### create certificate

- install [MKCert](https://github.com/FiloSottile/mkcert)
- `cd` to the root of the project where `manage.py` is located
- run `mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1`
- `cert.pem` and `key.pem` files should be created

### start backend

- install [poetry](https://python-poetry.org/docs/)
- `cd` to the root of the project where `manage.py` is located
- run `poetry install`
- run `export DJANGO_SETTINGS_MODULE=config.settings.devel`
- run `python manage.py runsslserver --certificate cert.pem --key key.pem`

### start frontend

- `cd` to `/client/frontend`
- run `npm install`
- run `export NODE_EXTRA_CA_CERTS="directory/where/your/cert.pem/is/located"`
- run `npm run dev`
