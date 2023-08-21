import os
import uuid

import boto3
from utils import get_aws_region
from datetime import datetime

STAGE = os.getenv('STAGE', 'dev')
dynamodb = boto3.resource('dynamodb', get_aws_region())

def insert_new_user():
    table = dynamodb.Table(f'voice-list-users-{STAGE}')

    new_id = str(uuid.uuid4()) + "_test_user"

    # Insert a new user
    user = {
        'id': new_id,
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password123',
        'password_hash': "$2b$12$adwPE2D7Nt18aWWUY2loD.sdB8yw8fQqXyVoMGC9xZILEPPkAkK4S",
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    table.put_item(Item=user)

    # Retrieve the user
    response = table.get_item(Key={'id': new_id})
    print(response['Item'])


def insert_new_list(items_list):
    table = dynamodb.Table(f'voice-list-lists-{STAGE}')
    new_id = str(uuid.uuid4()) + "_test_list"

    # Insert a new list
    voice_list = {
        'id': new_id,
        'name': 'New List',
        'description': 'This is a new list',
        'items': items_list,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    table.put_item(Item=voice_list)

    # Retrieve the list
    response = table.get_item(Key={'id': new_id})
    print(response['Item'])

def insert_new_item(item_index):
    table = dynamodb.Table(f'voice-list-items-{STAGE}')
    new_id = str(uuid.uuid4()) + "_test_item"

    # Insert a new list
    voice_item = {
        'id': new_id,
        'title': f'New Item {item_index}',
        'done': 'no',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    table.put_item(Item=voice_item)

    # Retrieve the list
    response = table.get_item(Key={'id': new_id})
    print(response['Item'])
    return new_id



def main():
    insert_new_user()
    items_list = []
    for i in range(10):
        item_id = insert_new_item(i)
        items_list.append(item_id)
    print(items_list)

    insert_new_list(items_list)

    # insert_new_list()



if __name__ == '__main__':
    main()
