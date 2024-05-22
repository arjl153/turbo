import json
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter

import requests

import turbo.constants
import turbo.custom_format
import turbo.utils
from turbo.exceptions import AuthError, NotFound


class Client(object):

    def __init__(
        self,
        remote,
        token,
        proxy=None,
        timeout=turbo.constants.TIMEOUT,
        verify_ssl=turbo.constants.SSL,
        **kwargs
    ):
        self.remote = remote
        self.token = str(token)

        self.timeout = timeout
        if verify_ssl == "False" or verify_ssl is False:
            self.verify_ssl = False
        else:
            self.verify_ssl = True

        self.session = requests.Session()
        self.session.headers["Accept"] = "application/vnd.r.renisac.v{}+json".format(
            turbo.constants.API_VERSION
        )
        self.session.headers["User-Agent"] = "ri-registry/{}".format(
            turbo.constants.VERSION
        )
        self.session.headers["Authorization"] = "Token token=" + self.token
        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["Accept-Encoding"] = "deflate"

        self.proxy = proxy
        if proxy is not None:
            assert turbo.utils.is_http_proxy(self.proxy)
            proxies = {"http": self.proxy}
            self.session.proxies.update(proxies)

    def _check_resp(self, resp, expects=200):

        if isinstance(expects, int):
            expects = [expects]

        if resp.status_code in expects:
            return True

        if resp.status_code in [401, 403]:
            raise AuthError(resp.text)

        if resp.status_code == 404:
            raise NotFound(resp.text)

        raise RuntimeError(resp.text)

    def _get(self, uri, params={}):
        if not uri.startswith("http"):
            uri = self.remote + uri

        resp = self.session.get(
            uri, params=params, verify=self.verify_ssl, timeout=self.timeout
        )
        self._check_resp(resp, 200)

        return json.loads(resp.text)

    def members(self, filters={}):
        return self._get("/members", params=filters)

    def users(self, filters={}):
        return self._get("/users", params=filters)


def main():
    p = turbo.utils.get_argument_parser()

    p = ArgumentParser(
        description=textwrap.dedent(
            """\
        Environmental Variables:
            REN_TOKEN

        example usage:
            $ REN_TOKEN=1234 ri --members
            $ ren --members 'indiana university'
            $ ren --users wes
        """
        ),
        formatter_class=RawDescriptionHelpFormatter,
        prog="ri",
        parents=[p],
    )
    p.add_argument("--token", help="specify api token", default=turbo.constants.TOKEN)
    p.add_argument(
        "--remote",
        help="specify API remote [default %(default)s]",
        default=turbo.constants.REMOTE_ADDR,
    )

    p.add_argument("--members", help="filter for members")
    p.add_argument("--users", help="filter for users")

    all_keys = [member.name for member in turbo.custom_format.PrintFormats]

    p.add_argument(
        "-f",
        "--format",
        help="specify output format [default: %(default)s]",
        default="table",
        choices=all_keys,
    )

    args = p.parse_args()

    turbo.utils.setup_logging(args)

    if not args.token:
        raise RuntimeError("missing --token")

    cli = Client(args.remote, args.token)

    if args.members:
        rv = cli.members(filters={"q": args.members})
        cols = turbo.constants.MEMBER_COLUMS

    elif args.users:
        rv = cli.users(filters={"q": args.users})
        cols = turbo.constants.USER_COLUMS

    else:
        print("Missing --users or --members flag")
        raise SystemExit

    provided_format = turbo.custom_format.initialize_format_from_string(args.format)
    format_function = provided_format.get_format_function()

    # The format function formats and prints the results
    format_function(rv, cols)


if __name__ == "__main__":
    main()
