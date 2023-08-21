from typing import Annotated

from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBasic

security = HTTPBasic()
users = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$ATYZ1S2D2qJqWCTOBvVOPeeTV4S12adlnWgMu8dmWX3qEl.wHYprC",
        # "$2b$12$ATYZ1S2D2qJqWCTOBvVOPeeTV4S12adlnWgMu8dmWX3qEl.wHYprC",  # password: testpassword
    },
}


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "mia":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def check_session_cookie(x_session: Annotated[str, Header()]):
    if x_session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Add your logic to validate the session cookie against your user database or session management system
    # Here, we check if the session cookie value exists in the users database
    if x_session not in users:
        raise HTTPException(status_code=401, detail="Invalid session")

    return x_session
