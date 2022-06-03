"""Stream type classes for tap-autoru."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_autoru.client import autoruStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")



class UsersStream(autoruStream):
    """Define custom stream."""
    name = "offer_stats"
    path = "/dealer/wallet/product/placement/activations/offer-stats?service=autoru&date=2022-05-30"

    records_jsonpath = "$[offer_product_activations_stats][*]"

    primary_keys = ["id"]
    replication_key = None
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

