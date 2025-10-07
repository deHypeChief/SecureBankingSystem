from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <!doctype html>
        <html>
          <head><meta charset="utf-8"><title>Hello</title></head>
          <body style="font-family:Arial,sans-serif;text-align:center;padding:40px;background:#f5f5f5">
            <div style="background:#fff;padding:24px;border-radius:8px;display:inline-block;box-shadow:0 6px 20px rgba(0,0,0,0.08)">
              <h1>Hello from Vercel function</h1>
              <p>This minimal handler verifies the Python serverless runtime is working.</p>
            </div>
          </body>
        </html>
        """
        self.wfile.write(html.encode())
        return
