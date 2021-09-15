from pydantic import BaseModel, Field

class AppLoginResponse(BaseModel):
    redirect_url: str
    app_token: str
