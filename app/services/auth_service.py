from fastapi import HTTPException
from fastapi.security import HTTPBearer
import os
from jose import jwt, JWTError
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
import requests
from datetime import datetime


# Configuration
AZURE_AD_TENANT_ID = os.getenv("AZURE_AD_TENANT_ID")
AZURE_AD_CLIENT_ID = os.getenv("AZURE_AD_CLIENT_ID")
AZURE_AD_SCOPES = os.getenv("AZURE_AD_SCOPES")
AZURE_AD_REDIRECT_URI = os.getenv("AZURE_AD_REDIRECT_URI")
AZURE_AD_AUTHORITY = os.getenv('AZURE_AD_AUTHORITY')
AZURE_AD_CLIENT_SECRET = os.getenv("AZURE_AD_CLIENT_SECRET")
ISSUER = f"https://sts.windows.net/{AZURE_AD_TENANT_ID}/"
JWKS_URL = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}/discovery/v2.0/keys"
ALGORITHM = "RS256"
AUDIENCE = f"api://{AZURE_AD_CLIENT_ID}"


httpBearer = HTTPBearer()

# Fetch and cache the JWKS (public keys) from Azure AD
def get_jwks():
    response = requests.get(JWKS_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch JWKS")
    return {key['kid']: key for key in response.json()['keys']}


def validate_jwt(token):
    try:
        # Decode the token header to get the key ID (kid)
        headers = jwt.get_unverified_header(token)
        kid = headers.get('kid')

        # Fetch the public keys from Azure AD
        keys = get_jwks()

        # Get the corresponding JWK for this token
        if kid not in keys:
            raise HTTPException(status_code=401, detail="Token validation error: Key ID not found.")

        public_key = keys[kid]

        # print(public_key)

        # Decode and validate the token
        claims = jwt.decode(
            token,
            key=public_key,
            audience=AUDIENCE,  # Replace with your API's full scope
            algorithms=['RS256'],  # Azure AD uses RS256 for token signing
            options={"verify_aud": True}  # Ensure audience claim is validated
        )
        
        # Validate issuer
        if claims.get('iss') != ISSUER:
            raise HTTPException(status_code=401, detail="Invalid issuer")

        # Validate audience
        if claims.get('aud') != AUDIENCE:
            raise HTTPException(status_code=401, detail="Invalid audience")

        # Validate expiration
        if claims.get('exp') < datetime.now().timestamp():
            raise HTTPException(status_code=401, detail="Token has expired")
        
        # Validate client id
        if claims.get('appid') != AZURE_AD_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Invalid client id")
        
        # Optional: Validate tenant ID if you have specific tenant requirements
        if claims.get('tid') != AZURE_AD_TENANT_ID:
            raise HTTPException(status_code=401, detail="Invalid tenant ID")
    
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")
    
    return claims

    
    

    
    

