from fastapi import FastAPI, Depends

# Relative Path
from .db.database import create_tables
from .api import company_name_routes, general_chat_route


app = FastAPI()

# Create the database tables (if not done in database.py)
# create_tables() # using alembic to create tables

# Include the NameCrafter routes
app.include_router(company_name_routes.router)
app.include_router(general_chat_route.router)
