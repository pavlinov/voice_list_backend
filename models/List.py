import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models import BaseDataClass

@dataclass
class List(BaseDataClass):
    id: str
    name: str
    items: list
    created_at: str
    updated_at: str
    description: Optional[str] = None

    def __init__(self, **kwargs):
        if not kwargs.get('id'):
            kwargs['id'] = str(uuid.uuid4())
        if not kwargs.get('created_at'):
            kwargs['created_at'] = datetime.now().isoformat()
        if not kwargs.get('updated_at'):
            kwargs['updated_at'] = datetime.now().isoformat()
        super().__init__(**kwargs)
