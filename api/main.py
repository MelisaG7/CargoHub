from fastapi import FastAPI

from services.item_lines import ItemLines
from services.item_types import ItemTypes
from services.items import Items
from services.clients import Clients
from services.item_groups import ItemGroups
from services.inventories import Inventories
from services.locations import Locations
from services.orders import Orders
from services.shipments import Shipments
from services.warehouses import Warehouses
from services.transfers import Transfers
from services.suppliers import Suppliers
from providers.auth_provider import MiddleWare
from starlette.middleware.base import BaseHTTPMiddleware

import uvicorn


# Deze library zodat we json bodys kunnen sturen ipv queries:
# Met dit kunnen we objecten maken die automatisch kijken of de json body klopt
# Dus automatische validation for velden!!!
# Als een verkeerde body wordt gegeven, geeft server 422 response.


# create a new app:
app = FastAPI()  # dus gewoon een FastAPU object aanmaken

# Add middleware:
app.add_middleware(BaseHTTPMiddleware, dispatch=MiddleWare().api_key_validator)


app.include_router(ItemLines("./data/", False).router, prefix="/api/v1")
app.include_router(ItemTypes("./data/", False).router, prefix="/api/v1")
app.include_router(Items("./data/", False).router, prefix="/api/v1")
app.include_router(Clients("./data/", False).router, prefix="/api/v1")
app.include_router(Inventories("./data/", False).router, prefix="/api/v1")
app.include_router(ItemGroups("./data/", False).router, prefix="/api/v1")
app.include_router(Locations("./data/", False).router, prefix="/api/v1")
app.include_router(Orders("./data/", False).router, prefix="/api/v1")
app.include_router(Shipments("./data/", False).router, prefix="/api/v1")
app.include_router(Warehouses("./data/", False).router, prefix="/api/v1")
app.include_router(Transfers("./data/", False).router, prefix="/api/v1")
app.include_router(Suppliers("./data/", False).router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
