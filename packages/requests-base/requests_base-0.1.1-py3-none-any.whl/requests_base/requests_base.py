"""
A Requests Session with a base URL.
"""
from typing import Any, Optional
from urllib.parse import urljoin

import requests


class BaseUrlSession(requests.Session):
    """
    A Requests Session with a URL that all requests will use as a base.

    Let's start by looking at an example:
    .. code-block:: python
        >>> from requests_base import BaseUrlSession
        >>> session = BaseUrlSession(base_url='https://example.com/resource/')
        >>> r = session.get('sub-resource/', params={'foo': 'bar'})
        >>> print(r.request.url)
        https://example.com/resource/sub-resource/?foo=bar

    Based on implementation from
    https://github.com/kennethreitz/requests/issues/2554#issuecomment-109341010
    """

    base_url: Optional[str] = None

    def __init__(self, base_url: Optional[str] = None) -> None:
        """
        Initialise the BaseUrlSession class.

        :param base_url: The base request URL
        """
        if base_url and not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        super().__init__()

    def request(
        self,
        method: str,
        url: str,
        *args: Any,
        **kwargs: Any,
    ) -> requests.models.Response:
        """
        Overrides the base Requests Session request method, generating the full request
        URL from the base URL and the given URL.

        :param method: REST method name
        :param url: The URL path of the request
        :return: The request response
        """
        full_url = self.generate_url(url)
        return super().request(
            method=method,
            url=full_url,
            *args,
            **kwargs,
        )

    def generate_url(self, url: str) -> str:
        """
        Generates the full request URL.

        :param url: The URL path
        :return: The full URL
        """
        if not url.startswith("/"):
            url = "/" + url
        return urljoin(self.base_url, url)
