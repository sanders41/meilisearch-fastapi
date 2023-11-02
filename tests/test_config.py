import pytest

from meilisearch_fastapi._config import get_config


@pytest.mark.parametrize("https", ["true", "false"])
def test_config_with_key(https, meilisearch_url, master_key, monkeypatch):
    monkeypatch.setenv("MEILI_HTTPS_URL", https)
    config = get_config()

    assert config.meilisearch_api_key == master_key
    if https == "true":
        assert config.meilisearch_url == f"https://{meilisearch_url[7:]}"
    else:
        assert config.meilisearch_url == meilisearch_url


def test_config_no_key(meilisearch_url, monkeypatch):
    # make sure there isn't an environmet vairable present
    monkeypatch.delenv("MEILI_MASTER_KEY", raising=False)

    config = get_config()

    assert config.meilisearch_api_key is None
    assert config.meilisearch_url == meilisearch_url


def test_config_no_url(monkeypatch):
    # make sure there isn't an environmet vairable present
    monkeypatch.delenv("MEILI_HTTP_ADDR", raising=False)

    get_config.cache_clear()

    with pytest.raises(ValueError):
        get_config()
