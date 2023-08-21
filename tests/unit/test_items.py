import pytest
import uuid
import json
import os
import copy
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
import routers.items

from .main import app

UTC_NOW = 'localmodules.utils.DateUtils.utc_now'
LOCAL_NOW = 'localmodules.utils.DateUtils.local_now'
DYNAMODB_CLIENT = 'localmodules.utils.services.dynamodb_client.DynamoDbBotoClient'


MOCK_DATETIME_STRING = '2023-06-22T15:46:17+0000'
MOCK_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S%z'
MOCK_DATETIME = datetime.strptime(MOCK_DATETIME_STRING, MOCK_DATETIME_PATTERN)
MOCK_TS = str(int(MOCK_DATETIME.timestamp()))


@patch(DYNAMODB_CLIENT)
def test_create_item():
    item_id = str(uuid.uuid4())
    item_title = "New Item"
    item_description = "This is a new item"

    with patch(UTC_NOW, return_value=MOCK_DATETIME_STRING):
        with patch(LOCAL_NOW, return_value=MOCK_DATETIME_STRING):
            with patch(DYNAMODB_CLIENT) as mock_dynamodb:
                item = routers.items.create_item(item_id, item_title, item_description)

    assert item["id"] == item_id
    assert item["title"] == item_title
    assert item["description"] == item_description