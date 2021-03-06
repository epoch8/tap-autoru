"""autoru tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_autoru.streams import (
    autoruStream,
    OfferStatsStream
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [

]

OFFER_STATS_PRODUCTS = [
    "placement",
    "premium",
    "special-offer",
    "boost",
    "highlighting",
    "badge",
    "sto-top",
    "turbo-package"
]

class Tapautoru(Tap):
    """autoru tap class."""
    name = "tap-autoru"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "autoru_login",
            th.StringType,
        ),
        th.Property(
            "autoru_password",
            th.StringType
        ),
        th.Property(
            "offer_stats_date",
            th.DateType,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        streams = [stream_class(tap=self) for stream_class in STREAM_TYPES]
        offer_stats_streams = [OfferStatsStream(tap=self, product=product) for product in OFFER_STATS_PRODUCTS]
        streams.extend(offer_stats_streams)
        return streams
