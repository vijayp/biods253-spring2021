import argparse
import urllib
import os
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler


class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_POST(self):
        # searches the sars cov2 genome for a specific sequence.
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_dict = urllib.parse.parse_qs(post_data.decode('utf-8'))
        self._set_headers()
        pattern_to_search = post_dict['pattern'][0]
        matches = os.popen("grep '%s' data/sequences.fasta | head" % pattern_to_search).read()
        out = "<h1>SARS-CoV2 matches!</h1><pre>" + matches + "</pre>"
        self.wfile.write(self._html(out))

def run(server_class=HTTPServer, handler_class=MyHandler, addr="localhost", port=8000, directory='.'):
    server_address = (addr, port)
    handler = functools.partial(handler_class, directory=directory)
    httpd = server_class(server_address, handler)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    parser.add_argument(
        "-s",
        "--static",
        type=str,
        default="static/",
        help="Specify the static directory",
    )

    args = parser.parse_args()
    run(addr=args.listen, port=args.port, directory=args.static)

