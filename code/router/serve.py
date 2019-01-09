from handler import Handler
from router import Router
import json
from memory_monitor import MemoryMonitor
from wsgiref.simple_server import make_server


class Index(Handler):

    def get(self):
        self.start_response(200)
        self.headers["Content-Type"] = "text/html"
        with open("index.htm") as index_fp:
            yield index_fp.read()


class Memory(Handler):

    def get(self):
        self.start_response(200)
        memory_monitor = MemoryMonitor()
        yield json.dumps({"memory": memory_monitor.usage()})


def main():
    router = Router()
    router.add_route("/", Index)
    router.add_route("/memory", Memory)
    server = make_server("", 8000, router)
    server.serve_forever()


if __name__ == "__main__":
    main()
