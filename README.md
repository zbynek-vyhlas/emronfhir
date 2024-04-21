## start project

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
