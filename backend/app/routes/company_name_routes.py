from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.company_name_crud import save_generated_company_names
from app.schemas.company_name_schemas import CompanyNameRequest, CompanyNameResponse
from app.services import langchain_service
import json
from app.models.company_name_models import CompanyNameSuggestionDBModel


router = APIRouter(
    prefix="/api/name-crafter",
    tags=["Company Name Crafter API"],
)
