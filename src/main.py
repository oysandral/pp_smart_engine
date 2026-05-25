from fastapi import FastAPI, Depends
from database import DatabaseManager  
from crud import get_all_products, create_product
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

@app.get("/products")
def read_products(db = Depends(get_db)):
    try:
        products = get_all_products(db)
        return {"products": products}
    
    except Exception as e:
        return {"error": f"Something went wrong: {e}"}

@app.post("/add_product")
def add_product(name : str, description : str, category : str, price : float, db = Depends(get_db)):
    create_product(db, name, description, category, price)

    return {"message" : f"The product {name} has been added correctly! Finally!"}