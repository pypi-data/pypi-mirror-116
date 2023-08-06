import typing

from pydantic import BaseModel, validator


class Subcategory(BaseModel):
    id: int
    name: str
    description: typing.Optional[str]


def normalize_subcategories(subcategories: typing.List[dict]):
    return [Subcategory(**dict_category) for dict_category in subcategories]


class Category(BaseModel):
    id: int
    name: str
    description: typing.Optional[str]
    subcategories: typing.List[typing.Union[dict, Subcategory]]

    _normalize_subcategories = validator("subcategories", allow_reuse=True)(
        normalize_subcategories
    )
