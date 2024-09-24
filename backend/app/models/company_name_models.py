from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import Base


class CompanyNameSuggestionDBModel(Base):  # Renamed to indicate DB model
    __tablename__ = "company_name_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    product_description = Column(String(255), nullable=False)
    target_audience = Column(String(255), nullable=False)
    suggested_company_name_1 = Column(String(255), nullable=False)
    suggested_company_name_2 = Column(String(255), nullable=False)
    suggested_company_name_3 = Column(String(255), nullable=False)
    created_at = Column(
        TIMESTAMP, server_default=func.now()
    )  # Use `func.now()` which is compatible with MySQL
