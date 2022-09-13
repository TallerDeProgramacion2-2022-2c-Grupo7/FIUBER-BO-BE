# FIUBER-BO-BE
Backend side of FIUBER’s back office


## Instalar dependencias
``` bash
poetry install
```
--- 

## Ejecución con Docker

``` bash
docker build -t fastapi-app .
docker container run -it -p 8000:8000 fastapi-app
```

---

## Correr tests
``` bash
poetry run pytest
```

