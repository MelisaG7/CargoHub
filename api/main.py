# import fast api and use it to create a new app:
from fastapi import FastAPI
from services.item_lines import ItemLines
from services.item_types import ItemTypes
from services.items import Items

from providers.auth_provider import MiddleWare
from starlette.middleware.base import BaseHTTPMiddleware

import uvicorn


# create a new app:
app = FastAPI()  # dus gewoon een FastAPU object aanmaken

# Add middleware:
app.add_middleware(BaseHTTPMiddleware, dispatch=MiddleWare().api_key_validator)


app.include_router(ItemLines("./data/", False).router, prefix="/api/v1")
app.include_router(ItemTypes("./data/", False).router, prefix="/api/v1")
app.include_router(Items("./data/", False).router, prefix="/api/v1")

# Om server te runnen:
# in Terminal: uvicorn <FileName>:<Appname> --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=3000, reload=True)