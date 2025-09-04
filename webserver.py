import http.server
import socketserver
import threading

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

class PreviewServer:
    def __init__(self, port, folder):
        self.port = port
        self.folder = folder
        self.httpd = None
        self.thread = None

    def startServer(self):
        if self.thread and self.thread.is_alive():
            print("Server already running")
            return
        handler = lambda *args, **kwargs: NoCacheHandler(*args, directory=self.folder, **kwargs)
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