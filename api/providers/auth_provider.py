# MIDDLEWARE!!! Dus weg met die authprovider bs
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class MiddleWare:

    def __init__(self):
        self.API_KEYS = {
            "api_key_admin": "a1b2c3d4e5",
            "api_key_user": "f6g7h8i9j0"
        }

    async def api_key_validator(self, request: Request, call_next):
        # Extract the `API_KEY` header
        api_key = request.headers.get("API_KEY")
        # If the API_KEY header is missing
        if not api_key:
            return JSONResponse(status_code=401, content={"detail": "Missing API Key."})

        # Validate the API key
        if api_key not in self.API_KEYS.values():
            return JSONResponse(status_code=401, content={"detail": "Invalid API Key."})
        # Check permissions based on the API key
        if api_key == self.API_KEYS["api_key_admin"]:
            # Admin has access to all methods
            pass
        elif api_key == self.API_KEYS["api_key_user"]:
            # User has access only to GET methods
            if request.method != "GET":
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Permission denied for this method."})
        # Proceed to the next middleware or endpoint
        return await call_next(request)
