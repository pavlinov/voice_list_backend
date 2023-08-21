import uuid
from datetime import datetime
from dataclasses import dataclass

from models import BaseDataClass
@dataclass
class Item(BaseDataClass):
    id: str
    title: str
    user_id: str
    created_at: str
    updated_at: str
    done: str = "no"

    def __init__(self, **kwargs):
        if not kwargs.get('id'):
            kwargs['id'] = str(uuid.uuid4())
        if not kwargs.get('created_at'):
            kwargs['created_at'] = datetime.now().isoformat()
        if not kwargs.get('updated_at'):
            kwargs['updated_at'] = datetime.now().isoformat()
        super().__init__(**kwargs)