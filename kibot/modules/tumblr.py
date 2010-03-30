import kibot.BaseModule

from . import tumblr_api

class tumblr(kibot.BaseModule.BaseModule):
    _stash_format = 'repr'
    _stash_attrs = ['tumblr_login']

    def __init__(self, bot):
        kibot.BaseModule.BaseModule.__init__(self, bot)

        try:
            self._create_api()
        except tumblr_api.TumblrAuthError:
            pass

    def _create_api(self):
        # clear the old api
        self.api = None

        try:
            login = self.tumblr_login
        except AttributeError:
            return

        api = tumblr_api.Api(login["name"], login["email"],
                             login["password"])

        self.bot.log(5, "checking Tumblr login")
        api.auth_check()
        if api.is_authenticated:
            self.api = api

    def _ensure_api(self):
        try:
            if self.api is not None:
                return True
        except AttributeError:
            pass

        return False

    _login_cperm = 'manager'
    def login(self, cmd):
        """Login to tumblr. Your credentials will be saved."""
        args = cmd.args.strip().split()

        if len(args) != 3:
            cmd.nreply("usage: tumblr.login <blog name> <email> <password>")
            return

        name, email, password = args

        self.tumblr_login = { "name": name, "email": email,
                              "password": password }

        try:
            self._create_api()
            cmd.nreply("OK")
        except tumblr_api.TumblrAuthError:
            cmd.nreply("Invalid login")

    _quote_cperm = 1
    def quote(self, cmd):
        """post quote to tumblr"""

        if not self._ensure_api():
            cmd.nreply("Not logged in")

        msg = cmd.args.strip()
        if msg == "":
            cmd.nreply("Nothing tumbled")
            return

        args = msg.split(" ", 1)
        if (len(args) < 2):
            source, quote = args[0], ""
        else:
            source, quote = args

        try:
            self.api.write_quote(quote, source=source)
            cmd.nreply("OK")
        except tumblr_api.TumblrError, e:
            cmd.nreply(str(e))

    _link_cperm = 1
    def link(self, cmd):
        """post link to tumblr"""

        if not self._ensure_api():
            cmd.nreply("Not logged in")

        msg = cmd.args.strip()
        if msg == "":
            cmd.nreply("Nothing tumbled")
            return

        try:
            self.api.write_link(msg)
            cmd.nreply("OK")
        except tumblr_api.TumblrError, e:
            cmd.nreply(str(e))

    _photo_cperm = 1
    def photo(self, cmd):
        """post photo to tumblr"""

        if not self._ensure_api():
            cmd.nreply("Not logged in")

        msg = cmd.args.strip()
        if msg == "":
            cmd.nreply("Nothing tumbled")
            return

        try:
            self.api.write_photo(msg)
            cmd.nreply("OK")
        except tumblr_api.TumblrError, e:
            cmd.nreply(str(e))

    _video_cperm = 1
    def video(self, cmd):
        """post video to tumblr"""

        if not self._ensure_api():
            cmd.nreply("Not logged in")

        msg = cmd.args.strip()
        if msg == "":
            cmd.nreply("Nothing tumbled")
            return

        try:
            self.api.write_video(msg)
            cmd.nreply("OK")
        except tumblr_api.TumblrError, e:
            cmd.nreply(str(e))
