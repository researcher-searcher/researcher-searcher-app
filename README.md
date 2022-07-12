### setup

`mkdir data`

Get `tsne.csv.gz` from researcher-searcher-search output and add to `data`

Make `.env`

```
API_NAME="" # the domain name of the API
API_URL="" # the URL of the API (can differ from name for internal connections)
NAME=
APP_PORT=
EXAMPLE_PERSON=
EXAMPLE_QUERY=
TITLE=
```

### Local dev

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python index.py
```

### Production

`docker-compose up -d`
