# import fast api and use it to create a new app:
from fastapi import FastAPI
from services.clients import Clients
from services.warehouses import *
from services.transfers import Transfers
from services.suppliers import Suppliers
from providers.auth_provider import MiddleWare
from starlette.middleware.base import BaseHTTPMiddleware
# Providers wordt nu (nog) niet gebruikt voor ease.
import uvicorn

# Deze library zodat we json bodys kunnen sturen ipv queries:
# Met dit kunnen we objecten maken die automatisch kijken of de json body klopt
# Dus automatische validation for velden!!!
# Als een verkeerde body wordt gegeven, geeft server 422 response.

# create a new app:
app = FastAPI()  # dus gewoon een FastAPU object aanmaken

# Add middleware:
app.add_middleware(BaseHTTPMiddleware, dispatch=MiddleWare().api_key_validator)

# routers:
# HIER ZET JE AL JE ROUTERS!
# Valt ook niet veel uit te leggen.

# Gwn je <Service_object(ROOT_PATH: string, DEBUG: boolean).router
# and youre good!
app.include_router(Clients("./data/", False).router)
app.include_router(Warehouses("./data/", False).router, prefix="/api/v1")
app.include_router(Transfers("./data/", False).router, prefix="/api/v1")
app.include_router(Suppliers("./data/", False).router, prefix="/api/v1")
# Om server te runnen:
# in Terminal: uvicorn <FileName>:<Appname> --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=3000, reload=True)
