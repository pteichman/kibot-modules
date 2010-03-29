import kibot.BaseModule

import random
import re

class eightball(kibot.BaseModule.BaseModule):
    """Magic 8-Ball"""
    def __init__(self, bot):
        self.affirmative = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes - definitely",
            "Yes",
            "You may rely on it"
            ]

        self.negative = [
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
            ]

        self.neutral = [
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Reply hazy, try again"
            ]

        self.replies = []
        self.replies.extend(self.affirmative)
        self.replies.extend(self.negative)
        self.replies.extend(self.neutral)

        self.bot = bot
        self._set_handlers(10)

    def _unload(self):
        self._del_handlers()

    def _on_command_not_found(self, conn, event):
        args = [event.target]
        args.extend(event.args)
        text = " ".join(args)

        # drop any extra whitespace in the string
        text = " ".join(text.split())

        regex = "\?$"
        if not re.search(regex, text, re.I):
            return

        reply = random.choice(self.replies)

        event.raw.nreply(reply.upper())
        return 'NO MORE'
