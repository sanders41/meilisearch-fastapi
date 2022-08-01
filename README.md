# Meilisearch FastAPI

![CI Status](https://github.com/sanders41/meilisearch-fastapi/workflows/CI/badge.svg?branch=main&event=push)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/meilisearch-fastapi/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/meilisearch-fastapi/main)
[![Coverage](https://codecov.io/gh/sanders41/meilisearch-fastapi/branch/main/graphs/badge.svg?branch=main)](https://codecov.io/gh/sanders41/meilisearch-fastapi)
[![PyPI version](https://badge.fury.io/py/meilisearch-fastapi.svg)](https://badge.fury.io/py/meilisearch-fastapi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meilisearch-fastapi?color=5cc141)](https://github.com/sanders41/meilisearch-fastapi)

Meilisearch FastAPI provides [FastAPI](https://fastapi.tiangolo.com/) routes for interacting with [Meilisearch](https://www.meilisearch.com/).

## Installation

Using a virtual environmnet is recommended for installing this package. Once the virtual environment is created and activated install the package with:

```sh
pip install meilisearch-fastapi
```

## Useage

Routes are split in groups so that different dependencies can be injected, and therefore different levels of access, can be given to different groups of routes.

### Example with no authentication required for routes

```py
from fastapi import APIRouter, FastAPI
from meilisearch_fastapi.routes import (
    document_routes,
    index_routes,
    meilisearch_routes,
    search_routes,
    settings_routes,
)

app = FastAPI()
api_router = APIRouter()
api_router.include_router(document_routes.router, prefix="/documents")
api_router.include_router(index_routes.router, prefix="/indexes")
api_router.include_router(meilisearch_routes.router, prefix="/meilisearch")
api_router.include_router(search_routes.router, prefix="/search")
api_router.include_router(settings_routes.router, prefix="/settings")

app.include_router(api_router)
```

### Example with routes requiring authentication

```py
from fastapi import APIRouter, FastAPI
from meilisearch_fastapi.routes import (
    document_routes,
    index_routes,
    meilisearch_routes,
    search_routes,
    settings_routes,
)

from my_app import my_authentication

app = FastAPI()
api_router = APIRouter()
api_router.include_router(document_routes.router, prefix="/documents", dependeincies=[Depends(my_authentication)])
api_router.include_router(index_routes.router, prefix="/indexes", dependeincies=[Depends(my_authentication)])
api_router.include_router(meilisearch_routes.router, prefix="/meilisearch", dependeincies=[Depends(my_authentication)])
api_router.include_router(search_routes.router, prefix="/search", dependeincies=[Depends(my_authentication)])
api_router.include_router(settings_routes.router, prefix="/settings", dependeincies=[Depends(my_authentication)])

app.include_router(api_router)
```

The url for Meilisearch, weather an https address should be used, and API key are read from
environment variables. Putting these into a .env file will keep you from having to set these
variables each time the terminal is restarted.

```txt
MEILI_HTTP_ADDR=localhost:7700  # This is the url for your instance of Meilisearch
MEILI_HTTPS_URL=true  # Setting this specifies the address should be https://. If false or not included the address will be http://
MEILI_MASTER_KEY=masterKey  # This is the API key for your Meilisearch instance
```

Now the Meilisearch routes will be available in your FastAPI app. Documentation for the routes can be viewed in the OpenAPI documentation of the FastAPI app. To view this start your FastAPI app and naviate to the docs `http://localhost:8000/docs` replacing the url with the correct url for your app.

## Compatibility with Meilisearch

This package only guarantees the compatibility with [version v0.28 of Meilisearch](https://github.com/meilisearch/meilisearch/releases/tag/v0.28.0).

## Contributing

Contributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)
