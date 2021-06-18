### Local dev

```
. ./venv/bin/activate
python index.py
```

### setup

`mkdir data`

Get `tsne.csv.gz` from researcher-searcher-search output and add to `data`

Make `.env`

```
API_URL=
NAME=
APP_PORT=
```

### Production

`docker-compose up -d`
