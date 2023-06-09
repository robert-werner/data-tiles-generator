class Response:

    def __init__(self, request_response_json):
        self.root = request_response_json

    @property
    def code(self):
        return self.root['meta']['code']

    @property
    def rid(self):
        return self.root['meta']['rid']

    @property
    def time(self):
        return self.root['meta']['time']
