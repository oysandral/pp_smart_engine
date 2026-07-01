from ai_service import get_embedding
from schemas import CreateProduct, UpdateProduct
from psycopg2.extras import RealDictCursor

def get_all_products(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT id, name, description, category, price FROM products;")

        result = cursor.fetchall()
    return result

def get_product_with_id(conn, product_id : int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT name, description, category, price FROM products WHERE id = %s;", 
                       (product_id,))
        result = cursor.fetchone()

    return result 

def create_product(conn, product: CreateProduct):
    cursor = conn.cursor()

    query = ('''
            INSERT INTO products (name, description, category, price, embedding)
                VALUES (%s, %s, %s, %s, %s);
            ''')
    
    vector = get_embedding(product.description)
    if not vector:
        vector = [0.0] * 3072
    
    cursor.execute(query, (
        product.name, 
        product.description,
        product.category,
        product.price,
        str(vector)
        ))
    
    conn.commit()

def search_products(conn, search_text : str):
    search_vector = get_embedding(search_text)

    if not search_vector:
        return []
    
    cursor = conn.cursor()

    query = ('''
            SELECT id, name, description, category, price 
            FROM products
            ORDER BY embedding <=> %s
            LIMIT 5;
            ''')
    cursor.execute(query, str(search_vector))
    return cursor.fetchall()

def update_patch_product(conn, product_id : int, payload : UpdateProduct):
    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        return None
    
    fields = [f"{key} = %s" for key in update_data.keys()]

    values = list(update_data.values())
    values.append(product_id)

    query = (f'''
            UPDATE products 
            SET {', '.join(fields)} 
            WHERE id = %s RETURNING *;
            ''')
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, tuple(values))
        updated_product = cursor.fetchone()
    conn.commit()

    return updated_product