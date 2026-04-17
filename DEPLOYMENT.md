# Deployment Guide

Deze app is nu geschikt gemaakt voor gewone Python webhosting.

Belangrijk:
- Host de app het liefst op een eigen subdomein zoals `app.variana.nl`.
- De app gebruikt nu root-paden zoals `/login` en `/dashboard`. Daarom is een subdomein of een eigen domein-root de veiligste keuze.
- De app ondersteunt nu zowel SQLite als PostgreSQL. Voor Render of serieuze productie is PostgreSQL de juiste keuze.

## Wat is toegevoegd

- `requirements.txt` voor installatie van productie-dependency `waitress`
- `serve.py` om de app als internetdienst te starten
- `wsgi.py` voor WSGI-hosting
- `passenger_wsgi.py` voor hostingomgevingen met Passenger
- `/health` endpoint voor eenvoudige health checks
- environment support voor `HOST`, `PORT`, `APP_DATA_DIR`, `APP_DB_PATH`, `APP_UPLOADS_DIR`, `DATABASE_URL`

## 1. Snelle deploy op een Python host

Gebruik deze instellingen:

- Build/install command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
python serve.py
```

- Handige environment variables:

```text
HOST=0.0.0.0
PORT=8000
APP_DATA_DIR=/var/data
APP_DB_PATH=/var/data/nlp_trainer_support.db
APP_UPLOADS_DIR=/var/data/uploads
```

## 1a. Render + PostgreSQL

Gebruik op Render:

- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
python serve.py
```

- Environment variables:

```text
HOST=0.0.0.0
PORT=10000
DATABASE_URL=<Render PostgreSQL Internal Database URL>
APP_UPLOADS_DIR=/var/data/uploads
```

Belangrijk:

- als `DATABASE_URL` gezet is, gebruikt de app PostgreSQL in plaats van SQLite
- `APP_DB_PATH` is dan niet meer nodig
- bij eerste start maakt de app zelf de tabellen en demo-data aan in PostgreSQL

## 2. Deploy op eigen server met Nginx of Apache

Start de app:

```bash
python serve.py
```

Reverse proxy daarna bijvoorbeeld naar:

```text
http://127.0.0.1:8000
```

Gebruik voor je domein bij voorkeur:

```text
app.variana.nl
```

## 3. Deploy op shared hosting met Passenger

Als je host Python + Passenger ondersteunt:

- upload de volledige projectmap
- installeer dependencies uit `requirements.txt`
- gebruik `passenger_wsgi.py` als WSGI-entrypoint
- zorg dat de Python app root naar deze projectmap wijst

## 4. Demo-data en database

Bij eerste start maakt de app zelf de database en demo-data aan.

Demo-accounts:

- `owner@platform.local` / `demo123`
- `admin@neuroflow.local` / `demo123`
- `trainer@neuroflow.local` / `demo123`
- `student@neuroflow.local` / `demo123`

## 5. Health check

Deze URL moet `ok` teruggeven:

```text
/health
```

## 6. Praktisch advies voor variana.nl

De schoonste route is:

1. host de app op een Python host of VPS
2. koppel daar een subdomein aan zoals `app.variana.nl`
3. laat `www.variana.nl` je hoofdsite blijven
4. stuur je mentor de link van het subdomein

Dat voorkomt problemen met submappen, root-paden en bestaande website-routing.
