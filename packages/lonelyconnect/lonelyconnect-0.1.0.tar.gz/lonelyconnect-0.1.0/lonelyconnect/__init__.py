import os
import sys
import random
import pickle
import warnings
from asyncio import Lock

# starlette's use of Jinja2 causes a warning
warnings.filterwarnings(
    action="ignore", category=DeprecationWarning, module=r".*starlette"
)

import yaml
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, Request, Response, File
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

from starlette.responses import RedirectResponse

from . import auth, game
from .models import User, BuzzState
from .route_ui import subapp as ui_routes

BUZZLOCK = Lock()
CONTROLLED_SHUTDOWN = False

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/ui", ui_routes)


def entrypoint():
    return uvicorn.run("lonelyconnect:app", host="0.0.0.0", port=8000, log_level="info")


@app.get("/")
async def index():
    return RedirectResponse("/ui/login")


@app.post("/login")
async def login(
    response: Response,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # username is actually ignored. These are random single-use non-critical codes.
    username = auth.CODES.pop(form_data.password.upper(), None)
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = random_token(32)
    auth.TOKENS[token] = username
    if request.headers.get("HX-Request"):
        response.headers["HX-Trigger-After-Settle"] = "ocResponse"
    return {"access_token": token, "token_type": "bearer"}


def random_token(length=6):
    return "".join(random.choices("ABCDEFGHKLMNPQRSTUVWXYZ23456789", k=length))


@app.on_event("startup")
async def startup():
    if "lonelyconnect_admin_code" in os.environ:
        code = os.environ["lonelyconnect_admin_code"]
    else:
        code = random_token(6)
        print("admin code:", code)
    auth.CODES[code] = "admin"
    try:
        with open("swap.bin", "rb") as f:
            game.GAME = pickle.load(f)
    except FileNotFoundError:
        pass


@app.on_event("shutdown")
async def shutdown():
    if CONTROLLED_SHUTDOWN:
        return
    with open("swap.bin", "wb") as f:
        pickle.dump(game.GAME, f)


@app.post("/pair/{username}")
async def pair(username: str, user: User = Depends(auth.admin)):
    code = random_token(6)
    auth.CODES[code] = username
    return code


@app.post("/load")
async def load(user: User = Depends(auth.admin), file: bytes = File(...)):
    game.GAME = game.Game()
    game.GAME.load(yaml.load(file, Loader=yaml.SafeLoader))


@app.get("/codes")
async def codes(user: User = Depends(auth.admin)):
    return auth.CODES


@app.get("/stage")
async def stage():
    return game.GAME.stage()


@app.get("/secrets")
async def secrets(user: User = Depends(auth.admin)):
    return game.GAME.secrets()


@app.post("/shutdown")
async def secrets(user: User = Depends(auth.admin)):
    global CONTROLLED_SHUTDOWN
    CONTROLLED_SHUTDOWN = True
    sys.exit(0)


@app.get("/actions")
async def state(user: User = Depends(auth.admin)):
    return game.GAME.actions()


@app.post("/action/{key}")
async def state(key: str, user: User = Depends(auth.admin)):
    return game.GAME.action(key)


@app.post("/buzz")
async def buzz(user: User = Depends(auth.player)):
    async with BUZZLOCK:
        try:
            return game.GAME.buzz(user.name)
        except PermissionError:
            raise HTTPException(
                status_code=409,
                detail="Can't buzz right now",
            )


@app.put("/buzz/{state}")
async def set_buzz(state: BuzzState, user: User = Depends(auth.admin)):
    async with BUZZLOCK:
        game.GAME.buzz_state = state.value
    return game.GAME.buzz_state


@app.post("/score/{username}")
async def add_to_score(
    request: Request, username: str, user: User = Depends(auth.admin)
):
    form_data = await request.form()
    game.GAME.points[username] += int(form_data["points"])


@app.post("/name/{username}")
async def add_to_score(
    request: Request, username: str, user: User = Depends(auth.admin)
):
    form_data = await request.form()
    auth.USERS[username].descriptive_name = form_data["teamname"].upper()
