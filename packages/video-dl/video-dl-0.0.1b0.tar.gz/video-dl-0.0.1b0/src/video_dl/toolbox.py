"""toolbox which provides lots of helper function.

class UserAgent deals with user agent.
class Config deals with config information.

Avaliable function:
    UserAgent().random: get a random user agent.
    Config().get_cookie(site): get a site's cookie.
    Configi().something: get the value combined to the key 'something'.

    progress_bar: print a naive progress bar.

Typical usage example:
    random_ua = UserAgent().random

    config = Config()
    bilibili_cookie = config.get_cookie('bilibili')
    threshold = config.big_file_threshold
"""
import os
import random


class UserAgent(object):
    """user agent.

    Attributes:
        random: get a random user agent.
    """

    def __init__(self, file_path: str = None):
        """read user agent list from a txt file.

        Args:
            file_path: txt file path, default: ./resource/user_agents.txt.
        """
        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'resource', 'user_agents.txt'
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            self.user_agents = [line.strip()
                                for line in f.readlines() if line.strip()]

    @property
    def random(self) -> str:
        """return a random user agent"""
        return random.choice(self.user_agents)


class ConsoleColor(object):
    """ANSI control code for color."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def info(label: str, *args, **kwargs) -> None:
    """print information to console with colors."""
    print(f'{ConsoleColor.WARNING}[{label}]{ConsoleColor.OKGREEN}',
          *args, ConsoleColor.ENDC, **kwargs)


if __name__ == '__main__':
    info('download', 'chifanba', 'lajiche ')
