from pydantic import BaseModel


class LoginBody(BaseModel):
    username: str
    password: str


class IpSet(BaseModel):
    ip: str


class DutySet(BaseModel):
    start_work: str
    get_off: str
