import pytest
from modules.darkweb_integration import search_darksearch, torbot_crawl, darkweb_lookup


@pytest.fixture
def mock_darksearch_response(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "data": [{"title": "Test Result", "link": "http://example.onion"}]
                }

        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)


def test_search_darksearch(mock_darksearch_response):
    result = search_darksearch("test")
    assert result["results"]
    assert result["results"][0]["title"] == "Test Result"


def test_torbot_crawl():
    result = torbot_crawl("test")
    assert isinstance(result, dict)
    assert result["keyword"] == "test"


def test_darkweb_lookup(mock_darksearch_response):
    result = darkweb_lookup("test")
    assert "darksearch" in result
    assert "torbot" in result
    assert result["keyword"] == "test"
