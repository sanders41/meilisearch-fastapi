from typing import Dict, List, Optional

from camel_converter.pydantic_base import CamelBase
from meilisearch_python_async.models.settings import Faceting
from meilisearch_python_async.models.settings import TypoTolerance as TypoToleranceInfo


class FacetingWithUID(Faceting):
    uid: str


class FilterableAttributes(CamelBase):
    filterable_attributes: Optional[List[str]] = None


class FilterableAttributesWithUID(FilterableAttributes):
    uid: str


class DisplayedAttributes(CamelBase):
    displayed_attributes: List[str]


class DisplayedAttributesUID(DisplayedAttributes):
    uid: str


class DistinctAttribute(CamelBase):
    attribute: Optional[str] = None


class DistinctAttributeWithUID(CamelBase):
    uid: str
    attribute: str


class IndexUpdate(CamelBase):
    uid: str
    primary_key: Optional[str] = None


class RankingRules(CamelBase):
    ranking_rules: List[str]


class RankingRulesWithUID(RankingRules):
    uid: str


class PrimaryKey(CamelBase):
    primary_key: Optional[str] = None


class SearchableAttributes(CamelBase):
    searchable_attributes: List[str]


class SearchableAttributesWithUID(SearchableAttributes):
    uid: str


class SortableAttributes(CamelBase):
    sortable_attributes: List[str]


class SortableAttributesWithUID(SortableAttributes):
    uid: str


class StopWords(CamelBase):
    stop_words: Optional[List[str]] = None


class StopWordsWithUID(StopWords):
    uid: str


class Synonyms(CamelBase):
    synonyms: Optional[Dict[str, List[str]]] = None


class SynonymsWithUID(Synonyms):
    uid: str


class TypoTolerance(CamelBase):
    typo_tolerance: Optional[TypoToleranceInfo] = None


class TypoToleranceWithUID(TypoTolerance):
    uid: str
