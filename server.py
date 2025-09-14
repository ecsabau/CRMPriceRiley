import http.server
import logging
import socketserver
import threading
from pathlib import Path

logger = logging.getLogger("InvestorAI")

class ReportServer:
    """HTTP server for online report access"""
    def __init__(self, port: int = 8000):
        self.port = port
        self.server = None

    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            kwargs['directory'] = str(Path("output/reports").absolute())
            super().__init__(*args, **kwargs)

        def log_message(self, format, *args):
            logger.info(f"Served {self.path} to {self.client_address[0]}")

    def start(self) -> bool:
        try:
            self.server = socketserver.TCPServer(
                ("", self.port),
                self.RequestHandler
            )
            threading.Thread(
                target=self.server.serve_forever,
                daemon=True
            ).start()
            logger.info(f"Server running on port {self.port}")
            return True
        except OSError as e:
            logger.error(f"Server failed: {e}")
            return False

    def stop(self):
        if self.server:
            self.server.shutdown()