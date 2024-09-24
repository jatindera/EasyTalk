from sqlalchemy.orm import Session
from ..models.company_name_models import CompanyNameSuggestionDBModel  # Database model
from fastapi import HTTPException


def save_generated_company_names(
    db: Session, name_suggestions: CompanyNameSuggestionDBModel
):

    # Add to the session, commit to the database, and refresh the instance
    try:
        db.add(name_suggestions)
        db.commit()
        db.refresh(name_suggestions)

    except:
        raise HTTPException(
            status_code=500,
            detail="Unable to store company names in Database. Please check the DB connectivity.",
        )
