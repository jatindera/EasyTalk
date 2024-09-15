from fastapi import FastAPI, Depends

from app.db.database import create_tables
from app.api import company_name_routes, general_chat_routes, user_routes, auth_routes
from app.services.user_service import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the list of allowed origins (you can limit this to specific origins)
origins = [
    "http://localhost:8000",
    "https://login.microsoftonline.com/",
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from the specified origins
    allow_credentials=True,  # Allows sending cookies and credentials
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers (like Authorization, Content-Type)
)


# Create the database tables (if not done in database.py)
# create_tables() # using alembic to create tables

# Include the NameCrafter routes
app.include_router(company_name_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(general_chat_routes.router)



@app.get("/public")
async def public_route():
    return {"message": "This is a public route!"}

@app.get("/secure")
async def secure_page(user: str = Depends(get_current_user)):
    return {"user": user}


