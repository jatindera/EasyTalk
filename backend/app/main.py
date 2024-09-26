from fastapi import FastAPI
import os

from app.db.database import create_tables
from app.routes import user_routes, chat_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the list of allowed origins (you can limit this to specific origins)
origins = [
    os.environ["FRONTEND_URL"],
    os.environ["BACKEND_URL"],
    os.environ["MICOROSOFT_LOGIN_URL"],
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from the specified origins
    allow_credentials=True,  # Allows sending cookies and credentials
    allow_methods=["GET", "POST"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers (like Authorization, Content-Type)
)


# Create the database tables (if not done in database.py)
create_tables()

# Include the NameCrafter routes
# app.include_router(company_name_routes.router)
app.include_router(user_routes.router)
app.include_router(chat_routes.router)









