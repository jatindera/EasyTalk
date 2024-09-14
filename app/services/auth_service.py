from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request
import os
from dotenv import load_dotenv
import httpx
load_dotenv()

# Load environment variables
config = Config(".env")

oauth = OAuth(config)
azure_ad = oauth.register(
    name='azure_ad',
    client_id=os.getenv("AZURE_AD_CLIENT_ID"),
    client_secret=os.getenv("AZURE_AD_CLIENT_SECRET"),
    authorize_url=f"{os.getenv('AZURE_AD_AUTHORITY')}/oauth2/v2.0/authorize",
    token_endpoint=f"{os.getenv('AZURE_AD_AUTHORITY')}/oauth2/v2.0/token",
    jwks_uri=f"https://login.microsoftonline.com/{os.getenv('AZURE_AD_TENANT_ID')}/discovery/v2.0/keys",
    client_kwargs={'scope': os.getenv("AZURE_AD_SCOPES")},
    redirect_uri=os.getenv("AZURE_AD_REDIRECT_URI")
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f'https://login.microsoftonline.com/{os.getenv("AZURE_TENANT_ID")}/oauth2/v2.0/authorize',
    tokenUrl=f'https://login.microsoftonline.com/{os.getenv("AZURE_TENANT_ID")}/oauth2/v2.0/token'
)

# Redirect user to Azure AD for login
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    print(request)
    print(redirect_uri)
    return await azure_ad.authorize_redirect(request, redirect_uri)

# Handle the callback after user authentication
async def auth_callback(request: Request):
    try:
        # Get the token from Azure AD
        token = await azure_ad.authorize_access_token(request)
        # print("*" * 50)
        # print(token)
        # print("*" * 50)
        nonce = token.get('userinfo').get('nonce')
        # Parse the ID token
        user_info = await oauth.azure_ad.parse_id_token(token=token, nonce=nonce)
        
        if not user_info:
            raise HTTPException(status_code=401, detail="Authentication failed")
        
        request.session['user'] = dict(user_info)

        return {"user_info": user_info}

    except httpx.HTTPStatusError as e:
        # This will catch specific HTTP errors
        print(f"HTTP Error occurred: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {e.response.text}")

    except Exception as e:
        # Catch any other exception and log the details
        print(f"General Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"General Error: {str(e)}")
    
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        response = await oauth.azure.parse_id_token(request, token)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )