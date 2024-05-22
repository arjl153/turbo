import turbo.constants
from turbo.client import Client


def test_remote():
    cli = Client("https://localhost:3000", 12345)
    assert cli.remote == "https://localhost:3000"


def test_token():
    cli = Client("https://localhost:3000", 12345)
    assert cli.token == "12345"


def test_token_string_conversion():
    cli = Client("https://localhost:3000", "my-token")
    assert cli.token == "my-token"


def test_proxy():
    proxy = "http://myproxy:3128"
    cli = Client("https://localhost:3000", 12345, proxy=proxy)
    assert cli.proxy == proxy


def test_timeout():
    custom_timeout = 30
    cli = Client("https://localhost:3000", 12345, timeout=custom_timeout)
    assert cli.timeout == custom_timeout


def test_verify_ssl_true():
    cli = Client("https://localhost:3000", 12345)
    assert cli.verify_ssl is True


def test_verify_ssl_false_string():
    cli = Client("https://localhost:3000", 12345, verify_ssl="False")
    assert cli.verify_ssl is False


def test_verify_ssl_false_boolean():
    cli = Client("https://localhost:3000", 12345, verify_ssl=False)
    assert cli.verify_ssl is False


def test_session_headers():
    cli = Client("https://localhost:3000", 12345)
    expected_headers = {
        "Accept": f"application/vnd.r.renisac.v{turbo.constants.API_VERSION}+json",
        "User-Agent": f"ri-registry/{turbo.constants.VERSION}",
        "Authorization": f"Token token=12345",
        "Content-Type": "application/json",
        "Accept-Encoding": "deflate",
        "Connection": "keep-alive",  # this is added automatically
    }
    print(cli.session.headers)
    assert cli.session.headers == expected_headers
