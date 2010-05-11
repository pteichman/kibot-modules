# use absolute_import so this module can also be called cobe
from __future__ import absolute_import

import kibot.BaseModule
from kibot.PermObjects import UserPerm
from time import time

from kibot.m_irclib import Timer
from kibot.irclib import nm_to_n

from cobe.brain import Brain
import os
import datetime

class cobe(kibot.BaseModule.BaseModule):
    """intelligence"""

    _nolearn_uperm = UserPerm('nolearn')

    def __init__(self, bot):
        self._brain_file = os.path.join(bot.op.files.data_dir, "cobe.brain")
        self._trace_file = os.path.join(bot.op.files.data_dir, "cobe.trace")

        # rotate logs
        if os.path.exists(self._trace_file):
            now = datetime.datetime.now()
            stamp = now.strftime("%Y-%m-%d.%H%M%S")
            os.rename(self._trace_file, "%s.%s" % (self._trace_file, stamp))

        self._brain = Brain(self._brain_file, instatrace=self._trace_file)

        kibot.BaseModule.BaseModule.__init__(self, bot)

    def _on_pubmsg(self, conn, event):
        import string, re

        message = event.args[0]
        message = re.sub("<\S+>", "", message)

        match = re.match("\"(.*)\" --\S+, \d+-\S+\d+.", message)
        if match:
            message = match.group(1)
        
        match = re.match("\s*(\S+)\s*[,:]\s*(.*?)\s*$", message)

        if match:
            to = match.group(1)
            text = match.group(2)
        else:
            to = None
            text = message

        speaker = nm_to_n(event.source)

        # drop any extra whitespace in the string
        text = string.join(string.split(text), ' ')

        user = self.bot.ircdb.get_user(nickmask=event.source)
        if user is not None:
            uperms = list(user.get_perms())
        else:
            uperms = list(self.bot.permdb.get_unknown_perms())
            uperms.append(self._nolearn_uperm)

        if 'ignore' in uperms:
            return 'NO MORE'

        # convert text to Unicode
        text = text.decode("utf-8")

        # if spoken to directly, generate a reply
        if str(to).lower() == self.bot.nick.lower():
            self._brain.learn(text)
            reply = self._brain.reply(text)

            # convert to utf-8 for output
            reply = reply.encode("utf-8")

            conn.privmsg(event.target, "%s: %s" % (speaker, reply))
        else:
            self._brain.learn(text)

        return 'NO MORE'
