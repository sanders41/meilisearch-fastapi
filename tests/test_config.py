import pytest

from meilisearch_fastapi._config import get_config


def test_config_with_key(meilisearch_url, master_key):
    config = get_config()

    assert config.meilisearch_api_key == master_key
    assert config.meilisearch_url == meilisearch_url


def test_config_no_key(meilisearch_url, master_key, monkeypatch):
    # make sure there isn't an environmet vairable present
    monkeypatch.delenv("MEILISEARCH_API_KEY", raising=False)

    get_config.cache_clear()

    config = get_config()

    assert config.meilisearch_api_key is None
    assert config.meilisearch_url == meilisearch_url

    # recreate the environment vairable


def test_config_no_url(meilisearch_url, monkeypatch):
    # make sure there isn't an environmet vairable present
    monkeypatch.delenv("MEILISEARCH_URL", raising=False)

    get_config.cache_clear()

    with pytest.raises(ValueError):
        get_config()

    # recreate the environment vairable
