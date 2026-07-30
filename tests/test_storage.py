import json
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from storage import json_storage


@pytest.fixture(autouse=True)
def clean_data(tmp_path, monkeypatch):
    monkeypatch.setattr(json_storage, "BASE_DIR", tmp_path)
    yield


def test_save_new_data():
    storage = json_storage.JsonStorage()
    storage.save("senamhi", "diario", {"temp": 25})
    assert (json_storage.BASE_DIR / "senamhi" / "latest" / "diario.json").exists()


def test_save_creates_history():
    storage = json_storage.JsonStorage()
    storage.save("senamhi", "diario", {"temp": 25}, run_at=datetime(2026, 7, 30, 8, 0, 0, tzinfo=ZoneInfo("America/La_Paz")))
    history = json_storage.BASE_DIR / "senamhi" / "history" / "2026" / "07" / "30" / "080000" / "diario.json"
    assert history.exists()


def test_no_changes_skips_history():
    storage = json_storage.JsonStorage()
    data = {"temp": 25}
    run_at = datetime(2026, 7, 30, 8, 0, 0, tzinfo=ZoneInfo("America/La_Paz"))
    storage.save("senamhi", "diario", data, run_at=run_at)

    storage.save("senamhi", "diario", data, run_at=datetime(2026, 7, 30, 9, 0, 0, tzinfo=ZoneInfo("America/La_Paz")))
    histories = list((json_storage.BASE_DIR / "senamhi" / "history" / "2026" / "07" / "30").iterdir())
    assert len(histories) == 1


def test_detects_changes():
    storage = json_storage.JsonStorage()
    run_at = datetime(2026, 7, 30, 8, 0, 0, tzinfo=ZoneInfo("America/La_Paz"))
    storage.save("senamhi", "diario", {"temp": 25}, run_at=run_at)
    storage.save("senamhi", "diario", {"temp": 30}, run_at=datetime(2026, 7, 30, 9, 0, 0, tzinfo=ZoneInfo("America/La_Paz")))
    histories = list((json_storage.BASE_DIR / "senamhi" / "history" / "2026" / "07" / "30").iterdir())
    assert len(histories) == 2


def test_latest_always_updated():
    storage = json_storage.JsonStorage()
    run_at = datetime(2026, 7, 30, 8, 0, 0, tzinfo=ZoneInfo("America/La_Paz"))
    storage.save("senamhi", "diario", {"temp": 25}, run_at=run_at)
    storage.save("senamhi", "diario", {"temp": 30}, run_at=datetime(2026, 7, 30, 9, 0, 0, tzinfo=ZoneInfo("America/La_Paz")))
    latest = json.loads((json_storage.BASE_DIR / "senamhi" / "latest" / "diario.json").read_text())
    assert latest == {"temp": 30}
