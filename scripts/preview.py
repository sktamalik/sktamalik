import http.server
import os
import socketserver
import sys
import threading
import time
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
PORT = 8765

def build_preview_html():
    readme_path = os.path.join(ROOT, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Escape backticks and backslashes for JS template literal
    escaped_md = md_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>GitHub Profile Preview - sktamalik</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-dark.min.css">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {{
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 32px 16px;
      display: flex;
      justify-content: center;
    }}
    .container {{
      max-width: 980px;
      width: 100%;
    }}
    .repo-header {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid #30363d;
      color: #58a6ff;
      font-size: 16px;
    }}
    .repo-header strong {{
      color: #f0f6fc;
    }}
    .markdown-body {{
      background-color: transparent !important;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 32px;
    }}
    .markdown-body details summary {{
      cursor: pointer;
    }}
    .markdown-body details[open] summary {{
      margin-bottom: 8px;
    }}
    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      border: none !important;
    }}
    .markdown-body table td {{
      border: none !important;
      padding: 12px;
    }}
    .markdown-body table tr {{
      background-color: transparent !important;
      border: none !important;
    }}
    .markdown-body img {{
      max-width: 100%;
      height: auto;
    }}
    .status-bar {{
      position: fixed;
      bottom: 12px;
      right: 12px;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 8px 14px;
      font-size: 12px;
      color: #7d8590;
      z-index: 9999;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="repo-header">
      <svg height="20" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="20" fill="#7d8590"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
      <span>sktamalik / <strong>sktamalik</strong></span>
      <span style="border: 1px solid #30363d; padding: 2px 8px; border-radius: 12px; font-size: 12px; color: #7d8590;">Public</span>
    </div>

    <article id="content" class="markdown-body">
      <!-- Content injected by JavaScript parser -->
    </article>
  </div>

  <div class="status-bar">
    Live Local Preview &bull; Port {PORT} &bull; Press Ctrl+C in terminal to stop
  </div>

  <script>
    const rawMd = `{escaped_md}`;
    if (window.marked) {{
      marked.setOptions({{
        gfm: true,
        breaks: true
      }});
      document.getElementById('content').innerHTML = marked.parse(rawMd);
    }} else {{
      document.getElementById('content').innerHTML = rawMd;
    }}
  </script>
</body>
</html>
"""
    out_file = os.path.join(ROOT, "preview.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built preview HTML: {out_file}")
    return out_file

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)
    def log_message(self, format, *args):
        pass  # quiet output

def run_server(open_browser=True):
    build_preview_html()
    url = f"http://localhost:{PORT}/preview.html"

    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
            print(f"Preview server running at: {url}")
            if open_browser:
                threading.Thread(target=lambda: (time.sleep(0.5), webbrowser.open(url))).start()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if "address already in use" in str(e).lower() or e.errno == 10048:
            print(f"Port {PORT} in use, opening existing server at: {url}")
            if open_browser:
                webbrowser.open(url)
        else:
            raise

if __name__ == "__main__":
    if "--build-only" in sys.argv:
        build_preview_html()
    else:
        run_server(open_browser=True)
