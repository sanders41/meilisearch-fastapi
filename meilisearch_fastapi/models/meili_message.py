from camel_converter.pydantic_base import CamelBase


class MeiliSearchMessage(CamelBase):
    msg: str
