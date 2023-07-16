from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
from urllib.parse import urlparse, parse_qs
import time, threading, socket

import config
import main_service
import prompts
import util_pick

# Python web server with cookie-based session
# based on https://davidgorski.ca/posts/sessions/

sessions = dict()
bot_history = dict()
states = dict()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/login":   self.login,
            "/logout":  self.logout,
            "/sessions":   self.sessions,
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
            content = self.html_start() + routes[path]() + self.html_end()
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
        user_name = self.parse_query_param("user_name")
        sessions[sid] = {"user_name": user_name, "useragent": "unknown", "ip address": self.client_address, "expiry": "unknown"}
        return """
        <p>Logged In<p>
        <a href='/'>Start Playing!</a>
"""

    def logout(self):
        if not self.user:
            return "Can't Log Out: No User Logged In"
        self.cookie = "sid="
        del sessions[self.user]
        del bot_history[self.user]
        del states[self.user]
        return """
        <p>Logged Out<p>
        <a href='/'>Go back</a>
"""

    # TODO restrict access!
    def sessions(self):
        content = "<pre>\n"
        content += "User Sessions:\n"
        for session in sessions:
            content += f"{sessions[session]}\n"
        content += "</pre>\n"
        return content

    def html_start(self):
        content = "<html><head><title>gpt-rpg</title></head>"
        content += "<body>"
        content += "<h1>gpt-rpg</h1>"
        return content

    def html_end(self):
        return "</body></html>"

    def home(self):
        content = ""
        if self.user:
            content += f"Welcome {self.user_name}!"
            content += f"<a href='logout'>log out</a>"
            content += "<br/><br/>"
            content += self.bot()
        else:
            content += "Welcome Stranger!"
            content += """
            <form action="/login">
                <label for="user_name">To start playing, please enter your name:</label><br>
                <input type="text" id="user_name" name="user_name">
                <input type="submit" value="Go!">
            </form>
              """
        return content

    def bot(self):
        content = ""
        history = dict()
        if self.user in bot_history:
            history = bot_history[self.user]
            state = states[self.user]
            user_input = self.parse_query_param("user_input")
            previous_messages = history['previous_messages']
            content += self.get_next_state(state, user_input, previous_messages)
        else:
            bot_history[self.user] = history
            # TODO allow user to pick genre
            story_type = util_pick.pick_one(prompts.get_story_types())
            state = main_service.get_initial_state(story_type, self.user_name)
            states[self.user] = state
            initial_text = main_service.get_initial_text(state)
            history['previous_messages'] = [initial_text]
            previous_messages = history['previous_messages']
            content += self.get_next_state(state, None, previous_messages)
        return content

    def get_next_state(self, state, user_input, previous_messages):
        (next_section_text, current_location_name) = main_service.get_next(state, user_input)
        if user_input is not None:
            previous_messages.append(user_input)
        previous_messages.append(f"LOCATION: {current_location_name}")
        previous_messages.append(f" >> {next_section_text}")
        content = self.bot_previous_messages()
        content += self.bot_next_button()
        return content

    def bot_previous_messages(self):
        history = bot_history[self.user]
        return "\n<br>---<br>\n".join(history['previous_messages'])

    def bot_next_button(self):
        return f"""
            <form action="/">
                <label for="user_input">What's next, {self.user_name}?</label><br>
                <input type="text" id="user_input" name="user_input">
                <input type="submit" value="Go!">
            </form>
            """

    def generate_sid(self):
        return "".join(str(randint(1,9)) for _ in range(100))

    def parse_path(self):
        return urlparse(self.path).path

    def parse_query_params(self):
        return parse_qs(urlparse(self.path).query)

    def parse_query_param(self, param):
        params = self.parse_query_params()
        if param in params:
            value_array = params[param]
            if value_array is None:
                return ""
            return value_array[0]
        return ""

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}

    def write(self, content):
        self.wfile.write(bytes(content, "utf-8"))

if __name__ == "__main__":
    # Multi-threaded server, else performance is terrible
    # ref https://stackoverflow.com/questions/46210672/python-2-7-streaming-http-server-supporting-multiple-connections-on-one-port
    #
    # Create ONE socket.
    addr = (config.HOSTNAME, config.PORT)
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(5)

    # Launch many listener threads.
    class Thread(threading.Thread):
        def __init__(self, i):
            threading.Thread.__init__(self)
            self.i = i
            self.daemon = True
            self.start()
        def run(self):
            httpd = HTTPServer(addr, MyServer, False)

            # Prevent the HTTP server from re-binding every handler.
            # https://stackoverflow.com/questions/46210672/
            httpd.socket = sock
            httpd.server_bind = self.server_close = lambda self: None

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            httpd.server_close()

    print(f"Server started at http://{config.HOSTNAME}:{config.PORT} - {config.WEB_SERVER_THREADS} threads")
    print("[press any key to stop]")
    [Thread(i) for i in range(config.WEB_SERVER_THREADS)]
    input("Press ENTER to kill server")

    print("Server stopped.")
