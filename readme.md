prepare environment variables

`cat .env.backend > .env`

`cat .env.frontend > client-app/.env`

prepare venv:

`python3 -m venv venv`

activate venv

`source venv/bin/activate`

install dependencies

`pip3 install -r requirements.txt`

run server

`python3 server.py`

go to front end app

`cd client-app`

install front end dependencies:

`yarn install`

run front end dev server:

`yarn dev`

open http://localhost:5173 at browser

recording: https://www.loom.com/share/04b79ed90e344c94a2c50a5b790cda73?sid=e7bb2668-1421-4e39-980b-0257d8fb66ff
