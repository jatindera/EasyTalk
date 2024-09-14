from fastapi import FastAPI, Depends

# Relative Path
from .db.database import create_tables
from .api import company_name_routes, general_chat_routes, user_routes, auth_routes
# from app.services.auth_service import login
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import os


app = FastAPI()

# Define the list of allowed origins (you can limit this to specific origins)
# origins = [
#     "http://localhost:3000",  # Example: React app running on localhost
#     "https://your-frontend-domain.com",  # Add your frontend domain here
# ]




# Add the session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from the specified origins
    allow_credentials=True,  # Allows sending cookies and credentials
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers (like Authorization, Content-Type)
)


# Create the database tables (if not done in database.py)
# create_tables() # using alembic to create tables

# Include the NameCrafter routes
# app.include_router(company_name_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(general_chat_routes.router)

# Example protected route
@app.get("/protected")
async def protected_route(request: Request):
    user = request.session.get('user')
    return {"message": "Welcome, you are logged in!", "user": user}

@app.get("/public")
async def public_route():
    return {"message": "This is a public route!"}
