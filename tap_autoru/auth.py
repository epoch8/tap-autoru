import requests

from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase
from typing import Type, Optional
from singer import utils
from datetime import datetime
from singer_sdk.helpers._util import utc_now


class AutoRuAuthenticator(APIAuthenticatorBase):
    def __init__(
        self,
        stream: RESTStreamBase,
        login: str = None,
        password: str = None,
        default_expiration: Optional[int] = None,
    ) -> None:

        super().__init__(stream=stream)

        self.headers = stream.http_headers
        self.request_payload = {"login": login, "password": password}
        self.url_base = stream.url_base
        self._default_expiration = default_expiration

        # Initialize internal tracking attributes
        self.session_id: Optional[str] = None
        self.last_refreshed: Optional[datetime] = None
        self.expires_in: Optional[int] = None

    @property
    def auth_headers(self) -> dict:
        if not self.is_session_id_valid():
            self.update_session_id()
        result = super().auth_headers
        result["x-session-id"] = self.session_id
        return result

    @property
    def auth_endpoint(self):
        return f"{self.url_base}/auth/login"

    def is_session_id_valid(self) -> bool:
        if self.last_refreshed is None:
            return False
        if not self.expires_in:
            return True
        if self.expires_in > (utils.now() - self.last_refreshed).total_seconds():
            return True
        return False

    def update_session_id(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time = utc_now()
        auth_request_payload = self.request_payload
        auth_response = requests.post(self.auth_endpoint, json=auth_request_payload, headers=self.headers)
        try:
            auth_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
        except Exception as ex:
            raise RuntimeError(
                f"Failed login, response was '{auth_response.json()}'. {ex}"
            )
        auth_json = auth_response.json()
        self.session_id = auth_json["session"]["id"]
        self.expires_in = auth_json["session"].get(
            "expire_timestamp", self._default_expiration
        )
        if self.expires_in is None:
            self.logger.debug(
                "No expires_in receied in OAuth response and no "
                "default_expiration set. Token will be treated as if it never "
                "expires."
            )
        self.last_refreshed = request_time

    @classmethod
    def create_for_stream(
        cls: Type["AutoRuAuthenticator"],
        stream: RESTStreamBase,
        login: str = None,
        password: str = None,
        default_expiration=None,
    ) -> "AutoRuAuthenticator":

        return cls(
            stream=stream,
            login=login,
            password=password,
            default_expiration=default_expiration,
        )
