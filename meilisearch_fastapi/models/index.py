from typing import Optional

from camel_converter.pydantic_base import CamelBase


class DistinctAttribute(CamelBase):
    attribute: Optional[str] = None


class DistinctAttributeWithUID(CamelBase):
    uid: str
    attribute: str


class IndexUpdate(CamelBase):
    uid: str
    primary_key: Optional[str] = None


class RankingRules(CamelBase):
    ranking_rules: list[str]


class PrimaryKey(CamelBase):
    primary_key: Optional[str] = None
