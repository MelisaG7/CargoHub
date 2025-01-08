# import fast api and use it to create a new app:
# from models import Models
import services
from providers.auth_provider import MiddleWare
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from fastapi import FastAPI
# Providers wordt nu (nog) niet gebruikt voor ease.


import services.clients
import services.inventories
import services.item_groups

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
app.include_router(services.clients.Clients("./data/", False).router, prefix="/api/v1")
app.include_router(services.inventories.Inventories("./data/", False).router, prefix="/api/v1")
app.include_router(services.item_groups.ItemGroups("./data/", False).router, prefix="/api/v1")
# Om server te runnen:
# in Terminal: uvicorn <FileName>:<Appname> --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=3000, reload=True)
