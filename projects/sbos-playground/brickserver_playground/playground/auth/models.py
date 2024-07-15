from pydantic import BaseModel


class AppLoginResponse(BaseModel):
    redirect_url: str
    app_token: str
