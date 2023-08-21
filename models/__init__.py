import dataclasses
from dataclasses import dataclass
from copy import copy
from typing import (
    Dict,
    List,
    Union,
)

JSONPrimitive = Union[bool, float, int, str, None]
Object = Dict[str, Union[JSONPrimitive, List[Union[JSONPrimitive, "Object"]], "Object"]]
JSONData = Union[JSONPrimitive, Object]


def drop_nulls(data: JSONData):
    """Process dict representing JSON object
    removing all the attributes with `None` values.
    """

    if isinstance(data, Dict):
        for k, v in copy(data).items():
            if v is None:
                del data[k]
            else:
                data[k] = drop_nulls(v)

    if isinstance(data, List):
        data = [drop_nulls(d) for d in data]

    return data

@dataclass
class BaseDataClass:

    # TODO: Current `__init__` implementation is crunky:
    # If the required field is not passed the instance will still be created
    # but the the error will raise unexpectedly once it's being accessed later on.
    def __init__(self, **kwargs):
        """
        1. The base functionality of this class is to simply filter out fields that are not specified in our models.
        Original dataclass functionality throws an error in this case.
        """
        names = {f.name: f for f in dataclasses.fields(self)}

        for default_attr, default_values in names.items():
            if type(default_values.default_factory) != dataclasses._MISSING_TYPE:
                try:
                    setattr(self, default_attr, default_values.default_factory())
                except Exception as e:
                    pass

        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

    def to_vlb(self):
        return drop_nulls(dataclasses.asdict(self))
