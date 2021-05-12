import pytest

from meilisearch_fastapi._config import get_config


def test_config_with_key(meilisearch_url, master_key):
    config = get_config()

    assert config.api_key == master_key
    assert config.url == meilisearch_url


def test_config_no_key(meilisearch_url, master_key, monkeypatch):
    # make sure there isn't an environmet vairable present
    monkeypatch.delenv("MEILISEARCH_API_KEY", raising=False)

    config = get_config()

    assert config.api_key is None
    assert config.url == meilisearch_url

    # recreate the environment vairable


def test_config_no_url(meilisearch_url, monkeypatch):
    # make sure there isn't an environmet vairable present
    monkeypatch.delenv("MEILISEARCH_URL", raising=False)

    with pytest.raises(ValueError):
        get_config()

    # recreate the environment vairable
