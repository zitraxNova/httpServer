from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write('Привет!'.encode("utf-8"))
        else:
            file_path = os.path.abspath(os.path.join('.', self.path[1:]))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                mime_type, _ = mimetypes.guess_type(file_path)
                self.send_header("Content-type", mime_type)
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write('Файл не найден'.encode("utf-8"))


hostName = "localhost"
serverPort = 8080

webServer = HTTPServer((hostName, serverPort), MyHandler)
print(f"Сервер запущен: http://{hostName}:{serverPort}")

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    print("Работа сервера прервана")

webServer.server_close()
print("Сервер остановлен...")