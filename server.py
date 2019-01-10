#!/usr/bin/python3 -u
from http.server import HTTPServer
from GithubHttpRequestHandler import GithubHTTPRequestHandler
import os, json

def main():
    # parse the config at startup to ensure we die if it's bad
    scriptdirectory = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(scriptdirectory, "config.json"), "r") as f:
        json.loads(f.read())

    server_address = ('0.0.0.0', 9800)
    httpd = HTTPServer(server_address, GithubHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()