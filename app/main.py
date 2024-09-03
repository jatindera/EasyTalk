from fastapi import FastAPI, Depends
#Relative Path
from .db.database import Base, engine
from .api.v1 import user_routes


app = FastAPI()

# Create the database tables (if not done in database.py)
Base.metadata.create_all(bind=engine)

# Include the user and product routes
app.include_router(user_routes.router, prefix="/api/v1")

