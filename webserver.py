import http.server
import socketserver
import threading
import time
import os

clients = []

class ReloadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/reload':
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            clients.append(self.wfile)
            try:
                while True:
                    time.sleep(1)  # keep connection alive
            except:
                if self.wfile in clients:
                    clients.remove(self.wfile)
        else:
            super().do_GET()


class PreviewServer:
    def __init__(self, port, folder, modelfolder):
        self.port = port
        self.folder = folder
        self.modelFolder = modelfolder
        self.httpd = None
        self.thread = None

    def startServer(self):
        if self.thread and self.thread.is_alive():
            print("Server already running")
            return

        handler = lambda *args, **kwargs: ReloadHandler(*args, directory=self.folder, **kwargs)
        self.httpd = socketserver.TCPServer(("", self.port), handler)

        def serve():
            print(f"Serving {self.folder} at http://localhost:{self.port}")
            self.httpd.serve_forever()

        self.thread = threading.Thread(target=serve, daemon=True)
        self.thread.start()

    def stopServer(self):
        if self.httpd:
            print("Stopping server...")
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
            self.thread = None
        else:
            print("Server is not running")

    def trigger_reload(self):
        global clients
        for client in clients[:]:
            try:
                client.write(b"data: reload\n\n")
                client.flush()
            except:
                clients.remove(client)
