"""Stream type classes for tap-autoru."""

from pathlib import Path
from datetime import date
from typing import Optional

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
            "id",
            th.StringType,
        ),
        th.Property(
            "created",
            th.StringType,
        ),

        th.Property("mark", th.StringType),
        th.Property("model", th.StringType),

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

        th.Property("salon_id", th.StringType),
        th.Property("rur_price", th.IntegerType),

        th.Property("owners_number", th.IntegerType),
        th.Property("year", th.IntegerType),
        th.Property("pts", th.StringType),
        th.Property("vin", th.StringType),

        th.Property("calls_all", th.IntegerType),
        th.Property("card_view_phone_show_conversion_all", th.NumberType),
        th.Property("card_view_call_conversion_all", th.NumberType),
        th.Property("service", th.StringType),

        th.Property("date", th.StringType),
        th.Property("product", th.StringType),
        th.Property("sum", th.IntegerType),
        th.Property("count", th.IntegerType),

    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        to_pop = []
        res = row["offer"]
        for key in res.keys():
            if key not in ["id", "created", "car_info", "status", "category", "section", "salon", "price_info",
                           "documents", "counters", "services"]:
                to_pop.append(key)
        for key in to_pop:
            res.pop(key)

        car_info = res.pop('car_info', None)
        res['mark'] = car_info['mark']
        res['model'] = car_info['model']

        salon = res.pop("salon")
        res["salon_id"] = salon["salon_id"]

        price_info = res.pop("price_info")
        res["rur_price"] = price_info["rur_price"]

        documents = res.pop("documents")
        res["owners_number"] = documents["owners_number"]
        res["year"] = documents["year"]
        res["pts"] = documents["pts"]
        res["vin"] = documents["vin"]

        counters = res.pop("counters")
        res["calls_all"] = counters["calls_all"]
        res["card_view_phone_show_conversion_all"] = counters["card_view_phone_show_conversion_all"]
        res["card_view_call_conversion_all"] = counters["card_view_call_conversion_all"]

        if res.get('services', False):
            services = res.pop("services")
            res["service"] = services[0]["service"]

        stats = row["stats"]
        res["date"] = stats[0]["date"]
        res["product"] = stats[0]["product"]
        res["sum"] = stats[0]["sum"]
        res["count"] = stats[0]["count"]

        return res
