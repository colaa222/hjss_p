from pydantic import BaseModel


class SendRequest(BaseModel):
    target: str
    message: str
