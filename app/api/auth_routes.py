from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/api/auth",
    tags=["Login API"],
)

