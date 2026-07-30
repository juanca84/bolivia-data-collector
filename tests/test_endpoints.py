import httpx
import pytest
from pytest_httpx import HTTPXMock

from providers.senamhi import diario, ediario


SAMPLE_DATA = [{"estacion": "Test", "temperatura": 25}]


def test_diario_ok(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=SAMPLE_DATA)
    data = diario.fetch(httpx.Client())
    assert data == SAMPLE_DATA


def test_ediario_ok(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=SAMPLE_DATA)
    data = ediario.fetch(httpx.Client())
    assert data == SAMPLE_DATA


def test_diario_http_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=500)
    with pytest.raises(httpx.HTTPStatusError):
        diario.fetch(httpx.Client())


def test_diario_empty_json(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=[])
    with pytest.raises(ValueError, match="Respuesta vacía"):
        diario.fetch(httpx.Client())


def test_diario_timeout(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(httpx.TimeoutException("timeout"))
    with pytest.raises(httpx.TimeoutException):
        diario.fetch(httpx.Client())
