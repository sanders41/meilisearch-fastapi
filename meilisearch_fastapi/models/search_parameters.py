from typing import List, Optional, Union

from camel_converter.pydantic_base import CamelBase


class SearchParameters(CamelBase):
    uid: str
    query: str
    offset: int = 0
    limit: int = 20
    filters: Optional[str] = None
    facet_filters: Optional[List[Union[str, List[str]]]] = None
    facets_distribution: Optional[List[str]] = None
    attributes_to_retrieve: List[str] = ["*"]
    attributes_to_crop: Optional[List[str]] = None
    crop_length: int = 200
    attributes_to_highlight: Optional[List[str]] = None
    matches: bool = False
