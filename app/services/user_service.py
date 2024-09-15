from fastapi import Depends
from fastapi import HTTPException, Depends
from app.services.auth_service import  validate_jwt, httpBearer
from fastapi.security import HTTPBasicCredentials

# JWT validation dependency
# def get_current_user(token: str = Depends(oauth2_scheme)):
def get_current_user(credentails:HTTPBasicCredentials = Depends(httpBearer)):
    try:
        token =credentails.credentials
        claims = validate_jwt(token)
        
        # Extract user information from claims (e.g., email, username)
        # Adjust based on your token's claims structure
        user = {
            'name': claims.get('name'),
            'email': claims.get('email')
        }          
        # Return the claims or user info
        return user
    except HTTPException as e:
        raise e  # Raise HTTPException with the appropriate status and detail if validation fails
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")
