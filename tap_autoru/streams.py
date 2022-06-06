"""Stream type classes for tap-autoru."""

from pathlib import Path
from datetime import date
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_autoru.client import autoruStream
from singer_sdk import Tap

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class OfferStatsStream(autoruStream):
    """Define custom stream."""
    records_jsonpath = "$[offer_product_activations_stats][*]"
    primary_keys = ["id"]
    replication_key = None

    def __init__(self, tap: Tap, product: str):
        self.product = product
        self.name = f"{product}_offer_stats"
        super().__init__(tap)


    @property
    def path(self):
        offer_stats_date = self.config.get("offer_stats_date", date.today().isoformat())
        return f"/dealer/wallet/product/{self.product}/activations/offer-stats?service=autoru&date={offer_stats_date}"

    # schema_filepath = SCHEMAS_DIR / "offer_stats.json"
    schema = th.PropertiesList(
        th.Property(
            "offer",
            th.ObjectType(
                th.Property(
                    "id",
                    th.StringType,
                ),
                th.Property(
                    "created",
                    th.StringType,
                ),
                th.Property(
                    "car_info",
                    th.ObjectType(
                        th.Property("mark", th.StringType),
                        th.Property("model", th.StringType)
                    )
                ),
                th.Property(
                    "status",
                    th.StringType,
                ),
                th.Property(
                    "category",
                    th.StringType,
                ),
                th.Property(
                    "section",
                    th.StringType,
                ),
                th.Property(
                    "salon",
                    th.ObjectType(
                        th.Property("salon_id", th.StringType)
                    ),
                ),
                th.Property(
                    "price_info",
                    th.ObjectType(
                        th.Property("rur_price", th.IntegerType)
                    ),
                ),
                th.Property(
                    "documents",
                    th.ObjectType(
                        th.Property("owners_number", th.IntegerType),
                        th.Property("year", th.IntegerType),
                        th.Property("pts", th.StringType),
                        th.Property("vin", th.StringType),
                    )
                ),
                th.Property(
                    "counters",
                    th.ObjectType(
                        th.Property("calls_all", th.IntegerType),
                        th.Property("card_view_phone_show_conversion_all", th.NumberType),
                        th.Property("card_view_call_conversion_all", th.NumberType)
                    )
                ),
                th.Property(
                    "services",
                    th.ObjectType(
                        th.Property("service", th.StringType)
                    )
                ),
            )
        ),
        th.Property(
            "stats",
            th.ObjectType(
                th.Property("date", th.StringType),
                th.Property("product", th.StringType),
                th.Property("sum", th.IntegerType),
                th.Property("count", th.IntegerType)
            )
        )

    ).to_dict()

