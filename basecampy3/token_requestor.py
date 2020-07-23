from bs4 import BeautifulSoup
import requests
import webbrowser
import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from .redirect_server import RedirectServer

class TokenRequester:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self):
        url = f"https://launchpad.37signals.com/authorization/new?type=web_server&client_id={self.client_id}&redirect_uri=http://localhost:8081/auth"

        webbrowser.open(url, new=2)

        httpServer = HTTPServer(('localhost', 8081), RedirectServer)
        httpServer.handle_request()

        fread = open("code.txt", "r")
        code = fread.read()
        fread.close()

        os.remove("code.txt")

        return code
