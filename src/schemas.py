from pydantic import BaseModel, Field
from typing import Optional, List

class CreateProduct(BaseModel):
    name: str = Field(min_length=3, max_length=100, pattern=r"^[a-zA-Z\s\-\.]+$")
    description : str = Field(min_length=3, max_length=200, pattern=r"^[a-zA-Z\s\-\.]+$")
    category : str = Field(min_length=3, pattern=r"^[a-zA-Z\s\-\.]+$")
    price : float = Field(gt=0)
    embedding: Optional[List[float]] = None

class ReadProduct(BaseModel):
    name: str = Field(min_length=3, max_length=100, pattern=r"^[a-zA-Z\s\-\.]+$")
    description : str = Field(min_length=3, max_length=200, pattern=r"^[a-zA-Z\s\-\.]+$")
    category : str = Field(min_length=3, pattern=r"^[a-zA-Z\s\-\.]+$")
    price : float = Field(gt=0)
    
    class Config:
        from_attributes = True

class UpdateProduct(BaseModel):
    name : str | None = Field(min_length=3, max_length=100, pattern=r"^[a-zA-Z\s\-\.]+$") 
    description: str | None = Field(min_length=3, max_length=200, pattern=r"^[a-zA-Z\s\-\.]+$") 
    price: float | None = Field(gt=0) 

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nowa nazwa produktu",
                "description" : "New description",
                "price": 99.99
            }
        }