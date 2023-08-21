import uuid
import boto3
from boto3.dynamodb.conditions import Key
from utils import get_aws_region

class UsersDBService:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb', get_aws_region())
        self.table = self.dynamodb.Table(table_name)

    def get_user_by_id(self, user_id: object) -> object:
        response = self.table.get_item(Key={'id': user_id})
        user = response.get('Item')
        return user

    def get_user_by_name(self, username):
        response = self.table.query(
            IndexName='username-index',
            KeyConditionExpression=Key('username').eq(username)
        )
        user = response.get('Items')
        if not user:
            return None
        return user[0]

    def create_user(self, user_data):
        response = self.table.put_item(Item=user_data)
        return response

    def update_user(self, user_id, user_data):
        response = self.table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET #attr1 = :val1, #attr2 = :val2, #attr3 = :val3',
            ExpressionAttributeNames={
                '#attr1': 'username',
                '#attr2': 'email',
                '#attr3': 'password'
            },
            ExpressionAttributeValues={
                ':val1': user_data['username'],
                ':val2': user_data['email'],
                ':val3': user_data['password']
            }
        )
        return response

    def update_user_named(self, user_id, user_data):
        response = self.table.update_item(
            Key={'id': user_id},
            UpdateExpression='SET #username = :username, #email = :email, #password = :password, #updated_at = :updated_at',
            ExpressionAttributeNames={
                '#username': 'username',
                '#email': 'email',
                '#password': 'password',
                '#updated_at': 'updated_at'
            },
            ExpressionAttributeValues={
                ':username': user_data['username'],
                ':email': user_data['email'],
                ':password': user_data['password'],
                ':updated_at': user_data['updated_at']
            },
            ConditionExpression='attribute_exists(id)',
        )
        return response

    def delete_user(self, user_id):
        response = self.table.delete_item(Key={'user_id': user_id})
        return response

class ListsDBService:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb', get_aws_region())
        self.table = self.dynamodb.Table(table_name)

    def get_list_by_id(self, list_id):
        response = self.table.get_item(Key={'id': list_id})
        voice_list = response.get('Item')
        return voice_list

    def create_list(self, list_data):
        list_data['id'] = str(uuid.uuid4())
        response = self.table.put_item(Item=list_data)
        return response

    def update_list(self, list_id, list_data):
        response = self.table.update_item(
            Key={'id': list_id},
            UpdateExpression='SET #attr1 = :val1, #attr2 = :val2, #attr3 = :val3, #attr4 = :val4',
            ExpressionAttributeNames={
                '#attr1': 'name',
                '#attr2': 'description',
                '#attr3': 'items',
                '#attr4': 'updated_at'
            },
            ExpressionAttributeValues={
                ':val1': list_data['name'],
                ':val2': list_data['description'],
                ':val3': list_data['items'],
                ':val4': list_data['updated_at']
            }
        )
        return response

    def delete_list(self, list_id):
        response = self.table.delete_item(Key={'id': list_id})
        return response

class ItemsDBService:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb', get_aws_region())
        self.table = self.dynamodb.Table(table_name)

    def get_items(self):
        response = self.table.scan()
        items = response.get('Items')
        return items


    #create get_items_by_user
    def get_items_by_user(self, user_id):
        response = self.table.query(
            IndexName='user_id-index',
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        items = response.get('Items')
        return items

    def get_item_by_id(self, item_id):
        response = self.table.get_item(Key={'id': item_id})
        item = response.get('Item')
        return item

    def create_item(self, item_data):
        item_data['id'] = str(uuid.uuid4())
        response = self.table.put_item(Item=item_data)
        return response

    def update_item(self, item_id, item_data):
        response = self.table.update_item(
            Key={'id': item_id},
            UpdateExpression='SET #attr1 = :val1, #attr2 = :val2, #attr3 = :val3',
            ExpressionAttributeNames={
                '#attr1': 'title',
                '#attr2': 'done',
                '#attr3': 'updated_at'
            },
            ExpressionAttributeValues={
                ':val1': item_data['title'],
                ':val2': item_data['done'],
                ':val3': item_data['updated_at']
            }
        )
        return response

    def delete_item(self, item_id):
        response = self.table.delete_item(Key={'id': item_id})
        return response

    def get_item_by_list(self, list_id):
        response = self.table.query(
            IndexName='list_id-index',
            KeyConditionExpression=Key('list_id').eq(list_id)
        )
        items = response.get('Items')
        return items

    def get_item_by_list_and_user(self, list_id, user_id):
        response = self.table.query(
            IndexName='list_id-index',
            KeyConditionExpression=Key('list_id').eq(list_id),
            FilterExpression=Key('user_id').eq(user_id)
        )
        items = response.get('Items')
        return items
