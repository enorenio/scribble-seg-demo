"""Tiny HTTP server for the comparison page.

Some browsers refuse to fetch() local files via file:// — this serves the
vis_web/ directory over http://localhost:8000 so the page works reliably.

    cd vis_web && python serve.py
    # then open http://localhost:8000 in a browser

Press Ctrl+C to stop.
"""
import http.server
import socketserver
import os, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving vis_web/ at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
