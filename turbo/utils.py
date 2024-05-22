import logging
import urllib
from argparse import ArgumentParser

from turbo.constants import LOG_FORMAT, LOG_LEVEL, TRACE, VERSION


def setup_logging(args):
    loglevel = logging.getLevelName(LOG_LEVEL)

    if args.debug or TRACE:
        loglevel = logging.DEBUG

    if TRACE:
        logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
            logging.DEBUG
        )

    console = logging.StreamHandler()
    logging.getLogger("").setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger("").addHandler(console)


def get_argument_parser():
    BasicArgs = ArgumentParser(add_help=False)
    BasicArgs.add_argument("-d", "--debug", dest="debug", action="store_true")
    BasicArgs.add_argument("-V", "--version", action="version", version=VERSION)
    return ArgumentParser(parents=[BasicArgs], add_help=False)


def is_http_proxy(proxy_url):
    """Checks if the provided proxy URL is for HTTP."""
    try:
        url_parts = urllib.parse.urlparse(proxy_url)
        return url_parts.scheme.lower() == "http"
    except (ValueError, urllib.parse.ParseResult):
        return False  # Handle invalid URLs gracefully
