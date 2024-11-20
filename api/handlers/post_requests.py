from providers import data_provider
from handlers import get_requests
import json


class PostRequests():

    def ChoosePath(self, path):

        if path in data_provider.POOl_DICT:
            PostRequests.post_object(
                data_provider.POOL_DICT[path].add,
                data_provider.POOL_DICT.save)
            return
        get_requests.Call_json_response(self, 404)
        self.end_headers()

    def post_object(self, AddObjectMethod, SaveObjectMethod):
        content_length = int(self.headers["Content-length"])
        post_data = self.rfile.read(content_length)
        new_object = json.loads(post_data.decode())
        Status = AddObjectMethod(new_object)
        SaveObjectMethod()
        get_requests.Call_json_response(self, Status)
        self.end_headers()