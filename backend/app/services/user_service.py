from fastapi import Depends
from fastapi import HTTPException, Depends
from app.services.auth_service import validate_jwt, httpBearer
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.models.user_models import User
from app.db.database import get_db
from app.schemas import user_schemas
from app.schemas.user_schemas import UserCreate


# JWT validation dependency
# def get_current_user(token: str = Depends(oauth2_scheme)):
def get_authenticated_user(httpCredentails: HTTPBasicCredentials = Depends(httpBearer)):
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


def get_user_by_userid(db:Session, user_id: str) -> UserCreate:
        # Call the CRUD function to get the user by email
    user_record = user_crud.get_user_by_userid(db, user_id)
    return user_record


def create_new_user(db: Session, userCreate: user_schemas.UserCreate) -> str:
    # Call the CRUD function to create a new user
    user_id = user_crud.create_new_user(db, userCreate)
    return user_id
