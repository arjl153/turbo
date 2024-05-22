from turbo.utils import is_http_proxy


def test_http_proxy():
    proxy_url = "http://myproxy:3128"
    assert is_http_proxy(proxy_url) is True


def test_https_proxy():
    proxy_url = "https://secureproxy:8080"
    assert is_http_proxy(proxy_url) is False


def test_invalid_url():
    proxy_url = "invalid_url"
    assert is_http_proxy(proxy_url) is False


def test_missing_scheme():
    proxy_url = "myproxy:3128"  # No scheme
    assert is_http_proxy(proxy_url) is False


def test_empty_url():
    proxy_url = ""
    assert is_http_proxy(proxy_url) is False
