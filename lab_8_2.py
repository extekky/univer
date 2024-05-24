from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 10000


class CalculatorServer(BaseHTTPRequestHandler):
    op1 = 0
    op2 = 0

    def do_GET(self):
        if self.path == "/op1":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(self.op1).encode())
        elif self.path == "/op2":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(self.op2).encode())
        elif self.path == "/calculate":
            self.send_response(405)
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()

        if self.path == "/op1":
            self.op1 = float(post_data)
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.path == "/op2":
            self.op2 = float(post_data)
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def do_POST(self):
        if self.path == "/calculate":
            operation = self.headers.get("Operation", "+")

            if operation == "+":
                result = self.op1 + self.op2
            elif operation == "-":
                result = self.op1 - self.op2
            elif operation == "*":
                result = self.op1 * self.op2
            elif operation == "/":
                if self.op2 != 0:
                    result = self.op1 / self.op2
                else:
                    self.send_response(400)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
            else:
                self.send_response(400)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", str(len(str(result))))
            self.end_headers()
            self.wfile.write(str(result).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def do_PUT_or_POST(self):
        self.send_response(405)
        self.send_header("Content-Length", "0")
        self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), CalculatorServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
