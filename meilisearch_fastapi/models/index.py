from __future__ import annotations

from camel_converter.pydantic_base import CamelBase
from meilisearch_python_sdk.models.settings import Faceting
from meilisearch_python_sdk.models.settings import FilterableAttributes as SdkFilterableAttributes
from meilisearch_python_sdk.models.settings import TypoTolerance as TypoToleranceInfo


class FacetingWithUID(Faceting):
    uid: str


class FilterableAttributes(CamelBase):
    filterable_attributes: list[str] | list[SdkFilterableAttributes] | None = None


class FilterableAttributesWithUID(FilterableAttributes):
    uid: str


class DisplayedAttributes(CamelBase):
    displayed_attributes: list[str]


class DisplayedAttributesUID(DisplayedAttributes):
    uid: str


class DistinctAttribute(CamelBase):
    attribute: str | None = None


class DistinctAttributeWithUID(CamelBase):
    uid: str
    attribute: str


class IndexUpdate(CamelBase):
    uid: str
    primary_key: str | None = None


class RankingRules(CamelBase):
    ranking_rules: list[str]


class RankingRulesWithUID(RankingRules):
    uid: str


class PrimaryKey(CamelBase):
    primary_key: str | None = None


class SearchableAttributes(CamelBase):
    searchable_attributes: list[str]


class SearchableAttributesWithUID(SearchableAttributes):
    uid: str


class SortableAttributes(CamelBase):
    sortable_attributes: list[str]


class SortableAttributesWithUID(SortableAttributes):
    uid: str


class StopWords(CamelBase):
    stop_words: list[str] | None = None


class StopWordsWithUID(StopWords):
    uid: str


class Synonyms(CamelBase):
    synonyms: dict[str, list[str]] | None = None


class SynonymsWithUID(Synonyms):
    uid: str


class TypoTolerance(CamelBase):
    typo_tolerance: TypoToleranceInfo | None = None


class TypoToleranceWithUID(TypoTolerance):
    uid: str
