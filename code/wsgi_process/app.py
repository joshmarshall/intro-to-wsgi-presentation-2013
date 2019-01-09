import json
from Queue import Queue
from subprocess import Popen, PIPE
from threading import Thread


class Application(object):

    def __init__(self, environ, start_response):
        self._environ = environ
        self._start_response = start_response

    def __iter__(self):
        # get the first part of the path...
        path = self._environ["PATH_INFO"][1:].split("/")[0]
        path = path or "index"
        method = "handle_%s" % (path)
        if not getattr(self, method, None):
            return self._error("404 Not Found", "No path %s" % (path))
        return getattr(self, "handle_%s" % (path))()

    def handle_index(self):
        status = "200 OK"
        headers = [("Content-Type", "text/html")]
        self._start_response(status, headers)
        with open("index.htm") as index_fp:
            yield index_fp.read()

    def handle_process(self):
        content_length = int(self._environ["CONTENT_LENGTH"])
        body = self._environ["wsgi.input"].read(content_length)
        request = json.loads(body)
        if "host" not in request:
            return self._error("400 Bad Request", "Invalid process.")
        host = request["host"]
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        self._start_response(status, headers)
        return self._traceroute(host)

    def _traceroute(self, host):
        queue = Queue()
        thread = TracerouteThread(host, queue)
        thread.start()
        # for Chromish browsers...
        yield " " * 1024
        while thread.is_alive():
            # should do a sleep in non-blocking world...
            if queue.empty():
                yield ""
            else:
                yield queue.get()
        while not queue.empty():
            yield queue.get()

    def _error(self, status, message):
        headers = [("Content-Type", "application/json")]
        self._start_response(status, headers)
        yield json.dumps({
            "status": status,
            "message": message
        })


class TracerouteThread(Thread):

    def __init__(self, host, queue):
        super(TracerouteThread, self).__init__()
        self._host = host
        self._queue = queue

    def run(self):
        command = "traceroute %s" % (self._host)
        process = Popen(command, shell=True, stdout=PIPE)
        while process.poll() is None:
            line = process.stdout.readline()
            self._queue.put(line)
        for line in process.stdout.readlines():
            self._queue.put(line)
