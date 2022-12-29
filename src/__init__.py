# Needed for searching packages under the main project
import site

__version__ = "1.3"


def main(args=None):
    site.addsitedir('.')
