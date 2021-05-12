# MeiliSearch FastAPI

![CI Status](https://github.com/sanders41/meilisearch-fastapi/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/meilisearch-fastapi/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)

MeiliSearch FastAPI provides [FastAPI](https://fastapi.tiangolo.com/) routes for interacting with [MeiliSearch](https://www.meilisearch.com/).

## Installation

Using a virtual environmnet is recommended for installing this package. Once the virtual environment is created and activated install the package with:

```sh
pip install meilisearch-fastapi
```

## Useage

Routes are split in groups so that different dependencies can be injected, and therefore different levels of access, can be given to different groups of routes.

### Example with no authentication require for routes

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
from meilisearch_fastapi import routes

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

The url for MeiliSearch and API key are read from environment variables. Putting these into a .env
file will keep you from having to set these variables each time the terminal is restarted.

```txt
MEILISEARCH_URL=http://localhost:7700  # This is the url for your instance of MeiliSearch
MEILISEARCH_API_KEY=masterKey  # This is the API key for your MeiliSearch instance
```

Now the MeiliSearch routes will be available in your FastAPI app. Documentation for the routes can be viewed in the OpenAPI documentation of the FastAPI app. To view this start your fast api app and naviate to the docs `http://127.0.0.1:8000/docs` replacing hte url with the correct url for your app.

## Contributing

Contributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)
