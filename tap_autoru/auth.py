import requests

from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase
from typing import Type, Optional
from singer import utils
from datetime import datetime
from singer_sdk.helpers._util import utc_now


class AuthoRuAuthenticator(APIAuthenticatorBase):
    def __init__(
        self,
        stream: RESTStreamBase,
        access_token: str,
    ) -> None:

        super().__init__(stream=stream)
        auth_credentials = {"x-authorization": access_token}


        if self._auth_headers is None:
            self._auth_headers = {}
        self._auth_headers.update(auth_credentials)

        self.request_payload = {}


        # Initialize internal tracking attributes
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.last_refreshed: Optional[datetime] = None
        self.expires_in: Optional[int] = None

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.is_token_valid():
            self.update_access_token()
        result = super().auth_headers
        result["Authorization"] = f"Bearer {self.access_token}"
        return result

    def is_token_valid(self) -> bool:
        """Check if token is valid.

        Returns:
            True if the token is valid (fresh).
        """
        if self.last_refreshed is None:
            return False
        if not self.expires_in:
            return True
        if self.expires_in > (utils.now() - self.last_refreshed).total_seconds():
            return True
        return False

    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time = utc_now()
        auth_request_payload = self.request_payload
        token_response = requests.post("login", data=auth_request_payload)
        try:
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
        except Exception as ex:
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            )
        token_json = token_response.json()
        self.access_token = token_json["access_token"]
        self.expires_in = token_json.get("expires_in", self._default_expiration)
        if self.expires_in is None:
            self.logger.debug(
                "No expires_in receied in OAuth response and no "
                "default_expiration set. Token will be treated as if it never "
                "expires."
            )
        self.last_refreshed = request_time

    @classmethod
    def create_for_stream(
        cls: Type["AuthoRuAuthenticator"],
        stream: RESTStreamBase,
        access_token: str,
    ) -> "AuthoRuAuthenticator":

        return cls(stream=stream, access_token=access_token)








