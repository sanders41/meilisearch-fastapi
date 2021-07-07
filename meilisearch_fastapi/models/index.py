from typing import Dict, List, Optional

from camel_converter.pydantic_base import CamelBase


class AttributesForFaceting(CamelBase):
    attributes_for_faceting: Optional[List[str]] = None


class AttributesForFacetingWithUID(AttributesForFaceting):
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


class StopWords(CamelBase):
    stop_words: Optional[List[str]] = None


class StopWordsWithUID(StopWords):
    uid: str


class Synonyms(CamelBase):
    synonyms: Optional[Dict[str, List[str]]] = None


class SynonymsWithUID(Synonyms):
    uid: str
