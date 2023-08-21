import uuid
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from models import BaseDataClass


@dataclass
class User(BaseDataClass):
    id: str
    email: str
    username: str
    password: str
    created_at: str
    updated_at: str
    password_hash: Optional[str] = None

    def __init__(self, **kwargs):
        if not kwargs.get('id'):
            kwargs['id'] = str(uuid.uuid4())
        if not kwargs.get('created_at'):
            kwargs['created_at'] = datetime.now().isoformat()
        if not kwargs.get('updated_at'):
            kwargs['updated_at'] = datetime.now().isoformat()
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'password_hash': self.password_hash
        }



