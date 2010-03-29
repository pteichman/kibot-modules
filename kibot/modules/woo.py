import kibot.BaseModule
import random

from kibot.irclib import nm_to_n

class woo(kibot.BaseModule.BaseModule):
    def __init__(self, bot):
        random.seed()
        kibot.BaseModule.BaseModule.__init__(self, bot)

    def _on_pubmsg(self, conn, event):
        import string, re

        message = event.args[0]
        message = re.sub("<\S+>", "", message)
        match = re.match("\s*(\S+)\s*[,:]\s*(.*?)\s*$", message)

        if match:
            to = match.group(1)
            text = match.group(2)
        else:
            to = None
            text = message

        speaker = nm_to_n(event.source)

        m = re.search("\\bw(oo+)s?\\b([!.?,])?", text.lower())

        # forecast is 70% chance of woo
        chance = 0.7

        if m and random.random() < chance:
            punc = {"!" : "!",
                    "." : ".",
                    "?" : "!"}

            woo = "w%s%s" % (m.group(1), punc.get(m.group(2), ""))

            if random.random() < 0.1:
                # be extra vocal sometimes
                woo = "w%s%s" % (m.group(1)*2, punc.get(m.group(2), ""))

            conn.privmsg(event.target, woo)
