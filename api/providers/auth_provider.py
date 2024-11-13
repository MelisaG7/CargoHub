USERS = [
    {
        "api_key": "a1b2c3d4e5",
        "app": "CargoHUB Dashboard 1",
        "endpoint_access": {
            "full": True
        }
    },
    {
        "api_key": "f6g7h8i9j0",
        "app": "CargoHUB Dashboard 2",
        "endpoint_access": {
            "full": False,
            "warehouses": {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "locations":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "transfers":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "items":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "item_lines":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "item_groups":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "item_types":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "suppliers":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "orders":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "clients":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            },
            "shipments":  {
                "full": False,
                "get": True,
                "post": False,
                "put": False,
                "delete": False
            }
        }
    }
]

_users = None

def init():
    """Initialize user data."""
    global _users
    _users = USERS

def get_user(api_key):
    """
    Retrieves the user that contains the given api key.

    :param api_key: The API key to match.
    :return: The user dictionary if found, else None.
    """
    for user in _users:
        if user["api_key"] == api_key:
            return user
    return None

def has_access(user, path, method):
    """
    Check if the user has access to the specified method on a given endpoint.

    :param user: The user dictionary.
    :param path: A list where the first element is the endpoint name.
    :param method: The HTTP method (e.g., 'get', 'post') to check.
    :return: True if access is allowed, False otherwise.
    """
    access = user["endpoint_access"]
    if access["full"]:
        return True
    else:
        return access[path[0]][method]