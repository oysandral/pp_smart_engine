from fastapi import FastAPI, Depends, HTTPException
from database import DatabaseManager  
from crud import get_all_products, create_product, get_product_with_id, update_patch_product, delete_product_crud, search_products
from schemas import CreateProduct, ReadProduct, UpdateProduct
import os 
import traceback

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

config = DatabaseManager.load_settings(SETTINGS_PATH)

db_manager = DatabaseManager(
    localhost=config["localhost"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

def get_db():
    conn = db_manager.get_connection()
    if conn is None:
        raise RuntimeError("Could not connect to database." + traceback.print_exc())
    try:
        yield conn
    finally:
        conn.close()

@app.get("/products", response_model=list[ReadProduct])
def read_products(db = Depends(get_db)):
    products = get_all_products(db)
    return products

@app.post("/add_product")
def add_product(product: CreateProduct, db = Depends(get_db)):
    create_product(db, product)

    return {"message" : f"The product {product.name} has been added correctly! Finally!"}

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db = Depends(get_db)):
    product = get_product_with_id(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return product

@app.patch("/products/{product_id}")
def update_product_endpoint(product_id : int, product_update : UpdateProduct, db = Depends(get_db)):
    success = update_patch_product(db, product_id, product_update)

    if not success:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    return success

@app.delete("/products/delete/{product_id}")
def delete_product(product_id : int, db = Depends(get_db)):
    success = delete_product_crud(product_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"The product with {product_id} ID is not found.")
    
    return {"message" : "Deleted correctly!"}

@app.get("/search", response_model=list[ReadProduct])
def get_similar_products(producr_descr : str, db = Depends(get_db)):
    searched_product = search_products(db, producr_descr)
    
    if not searched_product:
        raise HTTPException(status_code=404, detail="No items found.")
    
    return searched_product