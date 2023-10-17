import json

import function as func
import config as c
import schemas

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()  # create fastapi object
# set middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Check up on token and ip after server run
@app.on_event("startup")
def check_token_and_ip_exist():
    try:  # check api token exist
        with open(c.TOKEN_FILE, "r") as json_file:
            loaded_data = json.load(json_file)
        c.API_TOKEN = loaded_data.get("token")
    except Exception as e:
        print(f"Error loading API token: {e}")

    try:  # check ip exist
        with open(c.IP_FILE, "r") as json_file:
            loaded_data = json.load(json_file)
        c.IP = loaded_data.get("ip")
    except Exception as e:
        print(f"Error loading c.IP address: {e}")


@app.post("/login")
def login(login_body: schemas.LoginBody):
    if not c.IP:
        raise HTTPException(status_code=400, detail="尚未設定IP，請先設定後再試")
    api_token_check = True if c.API_TOKEN else False
    return func.login(username=login_body.username,
                      password=login_body.password,
                      api_token_check=api_token_check)


@app.post("/ip")
def set_ip(ip_body: schemas.IpSet):
    func.add_ip_and_save(ip=ip_body.ip)
    return "Set ip success"


@app.get("/ip")
def get_ip():
    return c.IP


@app.post("/duty")
def set_duty(duty_body: schemas.DutySet):
    func.save_duty(start_work=duty_body.start_work,
                   get_off=duty_body.get_off)
    return "Set duty success"


@app.get("/duty")
def get_ip():
    return func.get_duty()


@app.get("/access/users")
def get_user():
    return func.get_users()


@app.get("/access/log")
def get_access_log(since: int, until: int):
    return func.get_log(since=since, until=until)
