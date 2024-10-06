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


@router.post("/suggest-names/", response_model=CompanyNameResponse)
def create_company_name_suggestions(
    request: CompanyNameRequest,
    db: Session = Depends(get_db),
):
    print("*" * 100)

    # Generate company name suggestions. Plugin Langchain and LLM
    suggested_names_json = langchain_service.generate_company_names(
        request.product_description, request.target_audience
    )

    print(f"Generated names JSON: {suggested_names_json}")  # Debugging output

    # Check if the response is empty or invalid
    if not suggested_names_json:
        raise HTTPException(status_code=500, detail="No suggestions returned")
    try:
        # Parse the JSON response
        parsed_names = json.loads(suggested_names_json)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse JSON: {str(e)}")
    name_1, name_2, name_3 = parsed_names["company_name_suggestions"]
    # Ensure we received valid names
    if not all([name_1, name_2, name_3]):
        raise HTTPException(status_code=500, detail="Incomplete suggestions returned")

    print("=" * 100)
    print(f"1. {name_1}, 2. {name_2}, 3. {name_3}")
    print("=" * 100)

    generated_names = CompanyNameSuggestionDBModel(
        product_description=request.product_description,
        target_audience=request.target_audience,
        suggested_company_name_1=name_1,
        suggested_company_name_2=name_2,
        suggested_company_name_3=name_3,
    )

    # Save the suggestions in the database and return the saved instance
    save_generated_company_names(db, generated_names)

    return CompanyNameResponse(
        product_description=request.product_description,
        target_audience=request.target_audience,
        suggested_company_name_1=name_1,
        suggested_company_name_2=name_2,
        suggested_company_name_3=name_3,
    )
