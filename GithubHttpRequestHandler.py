from http.server import BaseHTTPRequestHandler
from DeploymentManager import DeploymentManager
import json

class GithubHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):        
        request_headers = self.headers
        content_length = request_headers.get('content-length', 0)
        response = self.rfile.read(int(content_length))

        content = ""

        try:
            content = json.loads(response.decode("utf-8"))

            manager = DeploymentManager()

            manager.receivepush(content)

        except json.decoder.JSONDecodeError:
            print("Error: Received malformed response from client")
            self.send_response(400)
            self.end_headers()
            return
        
        self.send_response(204)
        self.end_headers()