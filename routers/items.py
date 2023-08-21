from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from models.Items import Item
from utils import get_stage
from services.dynamodb import ItemsDBService

from dependencies import get_token_header, check_session_cookie

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(check_session_cookie)],
    responses={404: {"description": "Not found"}},
)

STAGE = get_stage()
items_db = ItemsDBService(f'voice-list-items-{STAGE}')


@router.get("/all", tags=["items"])
async def get_items():
    items = items_db.get_items()
    return items

@router.get("/byuser/{user_id}", tags=["items"])
async def get_items_by_user(user_id: str):
    items = items_db.get_items_by_user(user_id)
    return items


@router.get("/bylist/{list_id}", tags=["items"])
async def get_items_by_list(list_id: str):
    items = items_db.get_items_by_list(list_id)
    return items


@router.get("/bylist/{list_id}/byuser/{user_id}", tags=["items"])
async def get_items_by_list_and_user(list_id: str, user_id: str):
    items = items_db.get_items_by_list_and_user(list_id, user_id)
    return items


@router.get("/{item_id}", tags=["items"])
async def get_item(item_id: str):
    item = items_db.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", tags=["items"])
async def create_item(item_data: dict):
    item = Item(**item_data)
    response = items_db.create_item(item.to_vlb())
    return response


@router.put("/{item_id}", tags=["items"])
async def update_item(item_id: str, item_data: dict):
    item_data['updated_at'] = str(datetime.now())
    item_full_data = Item(**items_db.get_item_by_id(item_id))
    item_full_data.done = item_data.get('done')
    response = items_db.update_item(item_id, item_full_data.to_vlb())
    return response


@router.delete("/{item_id}", tags=["items"])
async def delete_item(item_id: str):
    response = items_db.delete_item(item_id)
    return response




#
# fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
#
#
# @router.get("/")
# async def read_items():
#     return fake_items_db
#
#
# @router.get("/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
#
#
# @router.put( "/{item_id}", tags=["custom"], responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}
