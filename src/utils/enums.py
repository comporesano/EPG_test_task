from enum import Enum

from functools import lru_cache


class Sex(Enum):
    male: str = "male"
    female: str = "female"


@lru_cache
def get_attributes_enum(cls: object, hidden: bool = False, drop_attrs: tuple = None) -> Enum:
    enum_vals = {}
    for attr in list(cls.__dict__):
        if attr.startswith("_") or attr.startswith("mro"):
            if not hidden:
                continue
        enum_vals[attr] = attr
    for el in drop_attrs:
        enum_vals.pop(el)
        
    return Enum(cls.__name__, enum_vals)
                
