from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Depends

from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from dependencies import check_session_cookie

from services.dynamodb import UsersDBService
from utils import get_stage

router = APIRouter(
    prefix="/voicelist",
    tags=["items"],
    dependencies=[Depends(check_session_cookie)],
    responses={404: {"description": "Not found"}},
)
STAGE = get_stage()
users_db = UsersDBService(f'voice-list-users-{STAGE}')

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/voicelist/item/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
