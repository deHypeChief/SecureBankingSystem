def handler(request):
    """Very small isolated handler to verify runtime availability."""
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
    return (200, [("Content-Type", "text/html")], html)
