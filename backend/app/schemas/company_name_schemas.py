from pydantic import BaseModel, Field


class CompanyNameRequest(BaseModel):
    product_description: str = Field(
        ...,
        min_length=5,
        strip_whitespace=True,
        description="Product description cannot be blank or whitespace",
    )
    target_audience: str = Field(
        ...,
        min_length=5,
        strip_whitespace=True,
        description="Target audience cannot be blank or whitespace",
    )


class CompanyNameResponse(BaseModel):
    product_description: str
    target_audience: str
    suggested_company_name_1: str
    suggested_company_name_2: str
    suggested_company_name_3: str
