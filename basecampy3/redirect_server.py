from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectServer(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(self.path.split("?")[1])
        code = params.get("code", "")[0]

        fopen = open("code.txt", "w")
        fopen.write(code)
        fopen.close()

        self.send_response(200)
        self.send_header("Content-type", "text/json")

        self.end_headers()

        self.wfile.write(bytes(
            "Procedura completata con successo!" +
            "<br><br>" +
            "Torna alla CLI per completare il processo di login!",
            "UTF-8")
        )
