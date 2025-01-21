from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import os


class MiddleWare:

    def __init__(self):
        if not os.getenv("GITHUB_ACTIONS"):
            from dotenv import load_dotenv
            load_dotenv()
        self.API_KEYS = {
            "api_key_admin": os.getenv("API_KEY_1"),
            "api_key_user": os.getenv("API_KEY_2")
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
