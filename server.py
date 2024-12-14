from llm import Agent

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

agent = Agent("persona")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the URL query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Assuming the variable is passed as 'variable_name' in the URL query
        variable = query_components.get('variable_name', [''])[0]
        # Process the variable (for example, just reversing the string)
        processed_variable = agent.chat(variable)
        
        # Send a response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = processed_variable
        self.wfile.write(response.encode('utf-8'))
            
            

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()