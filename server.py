"""Static server + /state (index.html က snapshot/ကျပန်းဂဏန်း သိမ်း/ပြန်ယူ)
channel တစ်ခုချင်းစီက STATE_NAME env နဲ့ ကိုယ်ပိုင် state ဖိုင် သုံး (ဥပမာ state-4.json)"""
import http.server, json, os

STATE = os.path.join("state", os.environ.get("STATE_NAME", "state.json"))

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/state/state.json":      # page က အမြဲ ဒီလမ်းကြောင်းကို ခေါ်
            try:
                body = open(STATE, "rb").read()
            except OSError:
                body = b"{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers(); self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/state":
            self.send_error(404); return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            json.loads(body)
        except ValueError:
            self.send_error(400); return
        os.makedirs("state", exist_ok=True)
        with open(STATE, "wb") as f:
            f.write(body)
        self.send_response(204); self.end_headers()

    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", 8080), H).serve_forever()
