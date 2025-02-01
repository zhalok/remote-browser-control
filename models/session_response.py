from pydantic import BaseModel


class SessionResponse(BaseModel):
    sessionId: str
    message: str
