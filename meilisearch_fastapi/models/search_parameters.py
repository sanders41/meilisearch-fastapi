from __future__ import annotations

from typing import Literal

from camel_converter.pydantic_base import CamelBase


class SearchParameters(CamelBase):
    uid: str
    query: str | None = None
    offset: int = 0
    limit: int = 20
    filter: str | list[str | list[str]] | None = None
    facets: list[str] | None = None
    attributes_to_retrieve: list[str] = ["*"]
    attributes_to_crop: list[str] | None = None
    sort: list[str] | None = None
    crop_length: int = 200
    attributes_to_highlight: list[str] | None = None
    show_matches_position: bool = False
    highlight_pre_tag: str = "<em>"
    highlight_post_tag: str = "</em>"
    crop_marker: str = "..."
    matching_strategy: Literal["all", "last", "frequency"] = "last"
    hits_per_page: int | None = None
    page: int | None = None
