from http.server import HTTPServer
from GithubHttpRequestHandler import GithubHTTPRequestHandler

def main():
    server_address = ('127.0.0.1', 9800)
    httpd = HTTPServer(server_address, GithubHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()