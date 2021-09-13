from typing import List, Optional, Union

from camel_converter.pydantic_base import CamelBase


class SearchParameters(CamelBase):
    uid: str
    query: Optional[str] = None
    offset: int = 0
    limit: int = 20
    filter: Optional[Union[str, List[Union[str, List[str]]]]] = None
    facets_distribution: Optional[List[str]] = None
    attributes_to_retrieve: List[str] = ["*"]
    attributes_to_crop: Optional[List[str]] = None
    sort: Optional[List[str]] = None
    crop_length: int = 200
    attributes_to_highlight: Optional[List[str]] = None
    matches: bool = False
