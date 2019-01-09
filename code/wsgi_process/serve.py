from app import Application
from wsgiref.simple_server import make_server


def main():
    server = make_server('', 8000, Application)
    print "Serving on 8000"
    server.serve_forever()


if __name__ == "__main__":
    main()
