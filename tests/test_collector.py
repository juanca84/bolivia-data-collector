from unittest.mock import patch

from providers.senamhi.collector import SenamhiProvider


def test_both_success():
    provider = SenamhiProvider()

    with (
        patch("providers.senamhi.diario.fetch", return_value={"temp": 25}),
        patch("providers.senamhi.ediario.fetch", return_value={"temp": 30}),
    ):
        results = provider.run_all()

    assert results["diario"]["success"] is True
    assert results["diario"]["data"] == {"temp": 25}
    assert results["ediario"]["success"] is True
    assert results["ediario"]["data"] == {"temp": 30}


def test_diario_fails_ediario_ok():
    provider = SenamhiProvider()

    with (
        patch("providers.senamhi.diario.fetch", side_effect=ValueError("error")),
        patch("providers.senamhi.ediario.fetch", return_value={"temp": 30}),
    ):
        results = provider.run_all()

    assert results["diario"]["success"] is False
    assert results["ediario"]["success"] is True
    assert results["ediario"]["data"] == {"temp": 30}


def test_both_fail():
    provider = SenamhiProvider()

    with (
        patch("providers.senamhi.diario.fetch", side_effect=ValueError("error")),
        patch("providers.senamhi.ediario.fetch", side_effect=ValueError("error")),
    ):
        results = provider.run_all()

    assert results["diario"]["success"] is False
    assert results["ediario"]["success"] is False
