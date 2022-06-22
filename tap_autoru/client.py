"""REST client handling, including autoruStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from .auth import AutoRuAuthenticator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class autoruStream(RESTStream):
    """autoru stream class."""

    url_base = "https://apiauto.ru/1.0"

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @property
    @cached
    def authenticator(self) -> AutoRuAuthenticator:
        """Return a new authenticator object."""
        return AutoRuAuthenticator(
            self,
            login=self.config.get("autoru_login"),
            password=self.config.get("autoru_password")
        )


    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers["x-authorization"] = self.config.get("access_token")
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        # TODO: If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        paging = response.json()["paging"]
        total_pages = paging.get("page_count")
        if total_pages == 1:
            return None
        next_page_token = previous_token + 1 if previous_token else 2

        return None if previous_token == total_pages else next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["pageNum"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
