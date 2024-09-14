from fastapi import APIRouter
from app.services.auth_service import login, auth_callback
from starlette.requests import Request

router = APIRouter(
    prefix="/api/auth",
    tags=["Chat API"],
)

# Redirects user to Azure AD login page
@router.get("/login")
async def azure_login(request: Request):
    return await login(request)

# Handles Azure AD callback
@router.get("/callback", name="auth_callback")
async def azure_callback(request: Request):
    return await auth_callback(request)
