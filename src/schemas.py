from pydantic import BaseModel, ValidationError
from typing import Optional, List

class CreateProduct(BaseModel):
    name: str 
    description : str
    category : str 
    price : Optional[float] = None 
    embedding: Optional[List[float]] = None

class ReadProduct(BaseModel):
    name: str
    description: str
    category: str 
    price: Optional[float] = None
    
    class Config:
        from_attributes = True

class UpdateProduct(BaseModel):
    name : str | None 
    description: str | None
    price: float | None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nowa nazwa produktu",
                "description" : "New description",
                "price": 99.99
            }
        }