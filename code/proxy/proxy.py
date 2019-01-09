

def proxy_host(app):
    def proxy_app(environ, start_response):
        if "X_HTTP_HOST" in environ:
            environ["HTTP_HOST"] = environ["X_HTTP_HOST"]
        return app(environ, start_response)
    return proxy_app
