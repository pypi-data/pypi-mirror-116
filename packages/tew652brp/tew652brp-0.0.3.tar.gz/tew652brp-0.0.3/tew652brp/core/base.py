from tew652brp.core.utils import make_routes


class BaseAct:
    def __init__(self, request_method, url, **extra):
        self._req_method = request_method
        self._url = url
        self._params = {}

    def submit(self):
        return self._req_method(self._url, data=self._params)


class BaseHandler:
    def __init__(self, session, url):
        self._session = session
        self._url = url
        self._routes = make_routes(self._url)
