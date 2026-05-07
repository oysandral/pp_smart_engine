from fastapi import FastAPI
from database import DatabaseManager  
from crud import get_all_products

app = FastAPI()

config = DatabaseManager.load_settings("settings.json")

db_manager = DatabaseManager(
    localhost=config["localhost"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

@app.get("/products")
def read_products():

    conn = db_manager.get_connection()
    
    if conn is None:
        return {"error": "Could not connect to database"}

    try:
        products = get_all_products(conn)
        return {"products": products}
    
    except Exception as e:
        return {"error": f"Something went wrong: {e}"}
        
    finally:
        conn.close()