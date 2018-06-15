from http.server import BaseHTTPRequestHandler

class GithubHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        
        request_headers = self.headers
        content_length = request_headers.get('content-length', 0)
        
        print(request_headers)
        print(self.rfile.read(int(content_length)))
        print("<----- Request End -----\n")
        
        self.send_response(204)
        self.end_headers()