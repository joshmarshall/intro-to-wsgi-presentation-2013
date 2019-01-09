class Handler(object):

    def __init__(self, environ, start_response):
        self._environ = environ
        self._start_response = start_response
        self._response_started = False
        self._code = 200
        self._message = "OK"
        self.headers = {}

    def start_response(self, code, status="OK"):
        self.headers.setdefault("Content-Length", "application/json")
        self._start_response(
            "%s %s" % (code, status), list(self.headers.items()))
