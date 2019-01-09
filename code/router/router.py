import json
import re


class Router(object):

    def __init__(self):
        self._routes = []

    def add_route(self, route, handler):
        if not route.startswith("^"):
            route = "^%s" % (route)
        if not route.endswith("$"):
            route = "%s$" % (route)
        self._routes.append((re.compile(route), handler))

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        request_method = environ["REQUEST_METHOD"].lower()
        handler = None
        for route, Handler in self._routes:
            match = route.match(path)
            if not match:
                continue
            handler = Handler(environ, start_response)
            if not getattr(handler, request_method, None):
                return _handle_error(
                    405, "Invalid method '%s'" % (request_method),
                    environ, start_response)
            try:
                return getattr(handler, request_method)(*match.groups())
            except Exception as exc:
                return _handle_error(
                    500, "%s" % (exc), environ, start_response)
        if not handler:
            return _handle_error(
                404, "Unknown path '%s'" % (path),
                environ, start_response)


def _handle_error(code, message, environ, start_response):
    start_response(
        "%s error" % (code), [("Content-type", "application/json")])
    return [json.dumps({"error": message, "stats": code})]
