import json
import uuid
import urllib3

import requests as r
import config as c

from fastapi import HTTPException

urllib3.disable_warnings()  # 關閉跨域warning


def add_ip_and_save(ip: str):
    """
    儲存ip位置
    """
    try:  # check ip exist
        response = r.get(f"https://{ip}", verify=False, timeout=2)
        text = response.text.lower()  # 全部轉成小寫
        if "unifi" in text:  # unifi 網頁回傳值中，必定會有unifi這個字樣
            c.IP = ip
        else:
            raise Exception()
    except Exception as e:
        print(f"Error message: {e}")
        raise HTTPException(status_code=400, detail=f"輸入的IP位置({ip})無法連接到Unifi主機，請重新嘗試")

    # 開始儲存ip
    data = {"ip": ip}
    with open(c.IP_FILE, "w") as json_file:
        json.dump(data, json_file)


def save_duty(start_work: str, get_off: str):
    """
    儲存上下班時間
    """
    data = {"start_work": start_work, "get_off": get_off}
    with open(c.WORK_FILE, "w") as json_file:
        json.dump(data, json_file)


def get_duty() -> dict:
    """
    取得上下班時間
    """
    try:
        with open(c.WORK_FILE, "r") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(e)
        return {"start_work": "", "get_off": ""}


def generate_and_save_api_token(session, headers):
    """
    產生 unifi access api token
    """
    name = str(uuid.uuid4())  # 生成一個唯一的名字作為token名稱
    request_body = {"name": name, "validity_period": c.VALIDITY_PERIOD, "scopes": c.TOKEN_SCOPES}
    # 並非Unifi access api doc內api
    get_token_url = f"https://{c.IP}/proxy/access/api/v1/developer/tokens"

    response = session.post(get_token_url, json=request_body, verify=False, headers=headers)
    api_token = response.json()["data"]["api_key"]
    c.API_TOKEN = api_token

    data = {"token": api_token}
    with open(c.TOKEN_FILE, "w") as json_file:
        json.dump(data, json_file)


def login(username: str, password: str, api_token_check: bool) -> dict:
    """
    透過unifi access 帳號登入

    成功登入後會先檢查是否已產生unifi access api token，若沒有則自動產生及儲存
    - 需先成功登入，才可產生unifi access api token
    - unifi access 權限需為 Full Management，才可成功產生
    """
    session = r.Session()
    # 並非Unifi access api doc內api
    login_url = f"https://{c.IP}/api/auth/login"
    body = {"username": username, "password": password, "token": "", "rememberMe": False}

    response = session.post(login_url, json=body, verify=False)

    result = dict(response.json())
    headers = response.headers  # 登入後unifi後端會自動set header
    result["headers"] = headers  # 若要使用unifi v2 api需要headers中的CSRF token

    if response.status_code != c.SUCCESS_STATUS_CODE:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not api_token_check:
        # 須將登入後的headers set在add token的api上，才可順利取得token
        generate_and_save_api_token(session, headers)

    return result


def get_users() -> dict:
    """
    取得所有已註冊unifi access人員
    """
    url = f"https://{c.IP}:12445/api/v1/developer/users"
    headers = {"Authorization": f"Bearer {c.API_TOKEN}"}

    response = r.get(url, verify=False, headers=headers)

    if response.status_code != c.SUCCESS_STATUS_CODE:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


def get_log(since: int, until: int) -> dict:
    """
    取得所有時間區間內的 log
    """
    url = f"https://{c.IP}:12445/api/v1/developer/system/logs"
    body = {"topic": c.TOPIC, "since": since, "until": until}
    headers = {"Authorization": f"Bearer {c.API_TOKEN}"}

    response = r.post(url, json=body, verify=False, headers=headers)

    if response.status_code != c.SUCCESS_STATUS_CODE:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
