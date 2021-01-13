import logging
try:
    from ..config import env
except:
    from config import env
logging.basicConfig(level=env.level_logging)
logger = logging.getLogger(__name__)


class HumanMessage:
    """Represent a possible outcome message for a grading, to be presented
    to the contestants.

    """

    def __init__(self, shorthand, message, help_text):
        """Initialization.

        shorthand (str): what to call this message in the code.
        message (str): the message itself.
        help_text (str): a longer explanation for the help page.

        """
        self.shorthand = shorthand
        self.message = message
        self.help_text = help_text

class MessageCollection:
    """Represent a collection of messages, with error checking."""

    def __init__(self, messages=None):
        self._messages = {}
        self._ordering = []
        if messages is not None:
            for message in messages:
                self.add(message)

    def add(self, message):
        if message.shorthand in self._messages:
            logger.error("Trying to registering duplicate message `%s'.",
                         message.shorthand)
            return
        self._messages[message.shorthand] = message
        self._ordering.append(message.shorthand)

    def get(self, shorthand):
        if shorthand not in self._messages:
            error = "Trying to get a non-existing message `%s'." % \
                shorthand
            logger.error(error)
            raise KeyError(error)
        return self._messages[shorthand]

    def all(self):
        ret = []
        for shorthand in self._ordering:
            ret.append(self._messages[shorthand])
        return ret