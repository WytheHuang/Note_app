# Note App

## Description
a simple note app that allows you to add, remove, list and read notes.
can be used as a todo list or a reminder app.

can click this [lick](http://noteapp.eastasia.cloudapp.azure.com:8501) to see the app.

## Remarks
- the app is deployed on azure cloud service.
- the backend is python django.
- the frontend is streamlit and react.js(not done yet).

## To do
- [ ] currently the app is not use docker to deploy, need to add dockerfile and docker-compose.yml.
- [ ] keep develope react.js frontend.

## Requirements
### backend
- see [pyproject.toml](./backend/pyproject.toml) or [requirements.txt](./backend/requirements.txt)

### frontend
#### streamlit
- see [pyproject.toml](./frontend_streamlit/pyproject.toml) or [requirements.txt](./frontend_streamlit/requirements.txt)

#### react.js
- not done yet


## need environment variables
### backend
- DOT_ENV_PATH: the path of .env file, default is "./backend/.env.local"
- DJANGO_SETTINGS_MODULE: the path of settings.py, default is "backend.config.settings.local"

### frontend
#### streamlit
- DOT_ENV_PATH: the path of .env file, default is "./frontend_streamlit/.env.local"

#### react.js
- not done yet