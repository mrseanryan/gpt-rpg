from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
from urllib.parse import urlparse, parse_qs

import config

# Python web server with cookie-based session
# based on https://davidgorski.ca/posts/sessions/

sessions = dict()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/login":   self.login,
            "/logout":  self.logout,
            "/":        self.home
        }
        self.cookie = None
        try:
            response = 200
            cookies = self.parse_cookies(self.headers["Cookie"])
            if "sid" in cookies:
                self.user = cookies["sid"] if (cookies["sid"] in sessions) else False
                if self.user:
                    self.user_name = sessions[self.user]['user_name']
            else:
                self.user = False
                self.user_name = None
            path = self.parse_path()
            print(f"req path: '{path}'")
            content = routes[path]()
        except Exception as error:
            print("!! error: ", error)
            response = 404
            content = "Oops! Not Found"

        self.send_response(response)
        self.send_header('Content-type','text/html')
        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)
        self.end_headers()

        self.write(content)
        return

    def login(self):
        # Password normally checked here
        sid = self.generate_sid()
        self.cookie = "sid={}".format(sid)
        user_name = self.parse_query_params()["user_name"]
        sessions[sid] = {"user_name": user_name, "useragent": "unknown", "ip address": "unknown", "expiry": "unknown"}
        return """
        <p>Logged In<p>
        <a href='/'>Start Playing!</a>
"""

    def logout(self):
        if not self.user:
            return "Can't Log Out: No User Logged In"
        self.cookie = "sid="
        del sessions[self.user]
        return """
        <p>Logged Out<p>
        <a href='/'>Go back</a>
"""

    def home(self):
        content = "<html><head><title>gpt-rpg</title></head>"
        content += "<body>"
        content += "<h1>gpt-rpg</h1>"
        if self.user:
            content += f"Welcome {self.user_name}!"
            content += f"<a href='logout'>log out</a>"
        else:
            content += "Welcome Stranger!"
            content += """
            <form action="/login">
                <label for="user_name">To start playing, please enter your name:</label><br>
                <input type="text" id="user_name" name="user_name">
                <input type="submit" value="Go!">
            </form>
              """
        content += "</body></html>"
        return content

    def generate_sid(self):
        return "".join(str(randint(1,9)) for _ in range(100))

    def parse_path(self):
        return urlparse(self.path).path

    def parse_query_params(self):
        return parse_qs(urlparse(self.path).query)

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}

    def write(self, content):
        self.wfile.write(bytes(content, "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((config.HOSTNAME, config.PORT), MyServer)
    print("Server started http://%s:%s" % (config.HOSTNAME, config.PORT))
    print("[press any key to stop]")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
