from socket import socket, AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR

BUFFER_SIZE = 4096


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("", 8080))
    sock.listen(5)

    while True:
        (client, address) = sock.accept()
        body = client.recv(BUFFER_SIZE)
        while "\r\n\r\n" not in body:
            body += client.recv(BUFFER_SIZE)
        headers, body = body.split("\r\n\r\n")
        # extract values from headers...
        method, path, headers = extract_headers(headers)
        content_length = int(headers["content-length"]) - len(body)
        if content_length:
            body += client.recv(content_length - len(body))
        client.send(handle_request(method, path, headers, body))
        client.close()


def extract_headers(header_string):
    method, path, version, headers = (None, None, None, {})
    for header_line in header_string.split("\r\n"):
        if not method:
            method, path, version = header_line.split(" ")
            continue
        header_key, header_value = header_line.split(":", 1)
        headers[header_key.lower().strip()] = header_value.strip()
    headers.setdefault("content-length", "0")
    return method, path, headers


def handle_request(method, path, headers, body):
    html = "<html><h1>Success!</h1></html>"
    return "\r\n".join([
        "HTTP/1.0 200 OK",
        "Content-Type: text/html",
        "Content-Length: %d" % (len(html)),
        "",
        html
    ])


if __name__ == "__main__":
    main()
