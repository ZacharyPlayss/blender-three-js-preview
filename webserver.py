import http.server
import socketserver
import subprocess
import sys
import textwrap


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
        self.proc = None

    def startServer(self):
        # If already running, do nothing
        if self.proc and self.proc.poll() is None:
            print("Server already running")
            return

        child_code = textwrap.dedent(f"""
            import http.server
            import socketserver

            class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
                def end_headers(self):
                    self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                    self.send_header("Pragma", "no-cache")
                    self.send_header("Expires", "0")
                    super().end_headers()

            port = {self.port}
            folder = {self.folder!r}

            Handler = lambda *args, **kwargs: NoCacheHandler(*args, directory=folder, **kwargs)

            class ReuseTCPServer(socketserver.TCPServer):
                allow_reuse_address = True

            with ReuseTCPServer(("", port), Handler) as httpd:
                print(f"Serving {{folder}} at http://localhost:{{port}}", flush=True)
                httpd.serve_forever()
        """)

        self.proc = subprocess.Popen([sys.executable, "-c", child_code])

    def stopServer(self):
        if not self.proc or self.proc.poll() is not None:
            print("Server is not running")
            self.proc = None
            return

        print("Stopping server...")
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()

        self.proc = None
