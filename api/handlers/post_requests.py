from providers import data_provider
from handlers import get_requests
import json


class PostRequests():

    def ChoosePath(self, path):
        # Choose path takes two parameters. Self and path.
        # Self: Responsible for end_headers, might remove that if not needed.
        # Path is the first string in the url the user wants.
        # Like 'warehouses' or 'clients'
        if path in data_provider.POOL_DICT:
            '''
            This if statement checks if the path
            exists in the dictionary in the class data_provider
            '''
            PostRequests.post_object(
                self,
                data_provider.fetch_pool(path).add,
                data_provider.fetch_pool(path).save)
            '''
            If it does exist, the method in PostRequests class get called.
            The reason we use POOL_DICT[path] instead of just 'path',
            is because the value of the key matching the 'path' has
            a method that calls a method we need for the method 'post_object()'
            '''
            return
        '''
        If there is no matching key in the dictionary,
        we call a method that sends the user a '404 not found'
        status code.
        '''
        get_requests.Call_json_response(self, (404, "Path not found."))
        '''
        We might put this method in a different class though.
        Because the class 'get_requests' should only be used
        for methods unique to get requests.
        '''
        self.end_headers()

    def post_object(self, AddObjectMethod, SaveObjectMethod):
        content_length = int(self.headers["Content-length"])
        post_data = self.rfile.read(content_length)
        new_object = json.loads(post_data.decode())
        Status = AddObjectMethod(new_object)
        SaveObjectMethod()
        get_requests.Call_json_response(self, Status)
        self.end_headers()
