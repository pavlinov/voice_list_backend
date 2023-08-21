import json
import re
import hashlib

import jsonify as jsonify
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from mangum import Mangum

from dependencies import get_query_token, get_token_header
from routers import items, users
from routers import login

app = FastAPI(dependencies=[]) # [Depends(get_query_token)]
handler = Mangum(app)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://54.226.99.181"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="frontend/templates")

#app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/chakra-pro", StaticFiles(directory="frontend/static/chakra-pro"), name="chakra-pro")

app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)

class LoginRequest(BaseModel):
    email: str

@app.get("/echo")
async def root():
    return {"message": "Hello Bigger Applications!"}


def is_email_valid(email: str) -> bool:
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_regex.match(email)

def generate_api_key(email: str) -> str:
    secret_key = "your_secret_key"
    api_key = hashlib.sha256((email + secret_key).encode()).hexdigest()
    return api_key


# @app.post('/login')
# def login(login_request: LoginRequest):
#     email = login_request.email
#
#     if not is_email_valid(email):
#         raise HTTPException(status_code=400, detail="Invalid email address")
#
#     if email != 'john.doe@example.com':
#         raise HTTPException(status_code=401, detail="Wrong user email")
#
#     api_key = generate_api_key(email)
#     return {"api_key": api_key}


@app.get('/mini/getMarketCapitalization')
def get_nft_volume_data():
    nft_volume_data = {
        'marketCapRatio': 0.035,
        'marketCap': 25000,
        'volumeRatio': -0.021,
        'volume': 12000,
        'circulatingSupplyRatio': 0.045,
        'circulatingSupply': 500
    }
    return nft_volume_data


@app.get("/itemsssss/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    #uvicorn.run(app, host="0.0.0.0", port=8000)


