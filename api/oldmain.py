import socketserver
import http.server
# import json

from providers import auth_provider
from providers import data_provider
from handlers import get_requests
from handlers.post_requests import PostRequests
from handlers.put_requests import PutRequests
from handlers import delete_requests
from processors import notification_processor


class ApiRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # When a get request is received this method sends the API-key to
        # check wether the user exists
        self.check_user("get")

    def do_POST(self):
        self.check_user("post")

    def do_PUT(self):
        self.check_user("put")

    def do_DELETE(self):
        self.check_user("delete")

    def check_user(self, HttpMethod):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user is None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                path = self.path.split("/")
                if len(path) > 3 and path[1] == "api" and path[2] == "v1":
                    self.handle_CRUD(path[3:], user, HttpMethod)
            except Exception as e:
                self.send_response(500)
                print(e)
                self.end_headers()

    def handle_CRUD(self, path, user, HttpMethod):
        # If the user doesn't have access to the Get functions the program
        # send a 403 code
        if not auth_provider.has_access(user, path, HttpMethod):
            self.send_response(403)
            self.end_headers()
            return
        else:
            # If the user has access to the get method:
            # Heel raar dat hier wel gwn naar een andere method gaat
            if HttpMethod == "get":
                get_requests.handle_get_request(self, path)
            elif HttpMethod == "post":
                PostRequests.ChoosePath(self, path[0])
            elif HttpMethod == "put":
                PutRequests.ChoosePath(self, path)
            elif HttpMethod == "delete":
                # Dit zien we later wel
                delete_requests.delete_object(self, path, user)


if __name__ == "__main__":
    PORT = 3000
    with socketserver.TCPServer(("", PORT), ApiRequestHandler) as httpd:
        auth_provider.init()
        data_provider.init()
        notification_processor.start()
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()
