from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socket
import os
from dotenv import load_dotenv
from dashboard_render import render_todo_dashboard
from get_tasks import get_all_users_tasks

load_dotenv()
EMAILS = os.getenv("EMAILS")
class DashboardHandler(BaseHTTPRequestHandler): # HTTP server to get image
    def do_GET(self):
        if self.path == '/dashboard.png':
            tasks = get_all_users_tasks(EMAILS)
            img = render_todo_dashboard(tasks, battery_pct=69)
            
            img_data = BytesIO()
            img.save(img_data, format='PNG')
            img_data.seek(0)

            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(img_data.getvalue())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args): # stop logging each request
        return



if __name__ == "__main__":
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("Server Starting: ")
    print(ip)
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, DashboardHandler)
    httpd.serve_forever()