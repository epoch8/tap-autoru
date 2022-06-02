"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_standard_tap_tests

from tap_autoru.tap import Tapautoru

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "access_token": os.getenv("ACCESS_TOKEN"),
    "autoru_login": os.getenv("AUTORU_LOGIN"),
    "autoru_password": os.getenv("AUTORU_PASSWORD")
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        Tapautoru,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()

# TODO: Create additional tests as appropriate for your tap.
