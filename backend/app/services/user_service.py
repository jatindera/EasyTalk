from fastapi import Depends
from fastapi import HTTPException, Depends
from app.services.auth_service import validate_jwt, httpBearer
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.crud.user_crud import get_user_by_oid as crud_get_user_by_oid
from app.crud.user_crud import create_new_user as crud_create_new_user
from app.models.user_models import User
from app.db.database import get_db
from app.schemas import user_schemas


# JWT validation dependency
# def get_current_user(token: str = Depends(oauth2_scheme)):
def get_current_user(httpCredentails: HTTPBasicCredentials = Depends(httpBearer)):
    try:
        token = httpCredentails.credentials
        claims = validate_jwt(token)

        # Extract user information from claims (e.g., email, username)
        # Adjust based on your token's claims structure
        user = {
            "user_id": claims.get("oid"),
            "email": claims.get("email"),
            "first_name": claims.get("given_name"),
            "last_name": claims.get("family_name"),
            "ip_address": claims.get("ipaddr"),
            "provider_name": claims.get("idp"),
            "role": "user",
        }
        # Return the claims or user info
        return user
    except HTTPException as e:
        raise e  # Raise HTTPException with the appropriate status and detail if validation fails
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")


def get_user_by_oid(oid: str, db: Session = Depends(get_db)) -> User:

    # Call the CRUD function to get the user by email
    user = crud_get_user_by_oid(oid, db)
    return user


def create_new_user(db: Session, userCreate: user_schemas.UserCreate) -> User:

    # Call the CRUD function to create a new user
    user = crud_create_new_user(db, userCreate)
    return user
