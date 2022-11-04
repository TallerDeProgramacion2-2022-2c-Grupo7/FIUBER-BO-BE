# FIUBER-Ratings


![licence](https://img.shields.io/github/license/TallerDeProgramacion2-2022-2c-Grupo7/FIUBER-BO-BE)

Backend for FIUBER's ratings

## Local installation & usage

1. Copy the Firebase credentials JSON (`firebase_credentials.json`) into the `src` directory of the repository.
2. Create a `.env` where the variables `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` are defined
3. Start the PostgreSQL instance
```
docker run -it --rm -p 5432:5432 --env-file .env postgres
```
4. Install dependencies
```
poetry install
poetry self add poetry-dotenv-plugin
```
5. Start the server:
```
poetry run python fastapi_app/app.py
```

The API will be available on `http://localhost:8000/`.



## Run tests
``` bash
poetry run pytest
```

## Repository setup & okteto deployment

The following GitHub Actions Secrets are required:
1. `DOCKERHUB_USERNAME`
2. `DOCKERHUB_TOKEN`
3. `KUBE_CONFIG_DATA` (generated with `cat kubeconfig.yaml | base64 -w 0`)
4. `POSTGRES_USER`
5. `POSTGRES_DB`
6. `POSTGRES_PASSWORD`
7. `FIREBASE_CREDENTIALS` (generated with `cat firebase-credentials.json | base64 -w 0`)

