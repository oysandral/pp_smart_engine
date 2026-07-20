from ai_service import get_embedding
from schemas import CreateProduct, UpdateProduct
from psycopg2.extras import RealDictCursor
import traceback

def get_all_products(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        query =('''
                SELECT id, name, description, category, price 
                FROM products;
                ''')
        cursor.execute(query)
        result = cursor.fetchall()

    return result

def get_product_with_id(conn, product_id : int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        query = ('''
                SELECT name, description, category, price 
                 FROM products 
                 WHERE id = %s;
                ''')
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()

    return result 

def create_product(conn, product: CreateProduct):
    vector = get_embedding(product.description)

    if not vector:
        vector = [0.0] * 3072
        
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        query = ('''
                INSERT INTO products (name, description, category, price, embedding)
                    VALUES (%s, %s, %s, %s, %s);
                ''')
        
        cursor.execute(query, (
            product.name, 
            product.description,
            product.category,
            product.price,
            str(vector)
            ))
        
        conn.commit()

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
    
    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, tuple(values))
            updated_product = cursor.fetchone()

            conn.commit()

            return updated_product
    
    except Exception as e:
        print(f"Technical database problem: {e}.")
        traceback.print_exc()
        return None

def delete_product_crud(conn, product_id : int):
    existing_product = get_product_with_id(conn, product_id)

    if not existing_product:
        return False

    with conn.cursor(cursor_factory=RealDictCursor) as cursor: 
        query = ('''
                DELETE FROM products WHERE id = %s;
                ''')
        cursor.execute(query, (product_id,))
        conn.commit()

    return True

def search_products(conn, descr : str):
    descr_embeddings = get_embedding(descr)

    if not descr_embeddings:
            return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = ('''
                    SELECT id, name, description, category, price, 1 - (embedding <=> %s::vector) AS similarity
                    FROM products
                    WHERE (1 - (embedding <=> %s::vector)) > 0.6
                    ORDER BY similarity DESC
                    LIMIT 5;
                    ''')
            cursor.execute(query, (descr_embeddings, descr_embeddings,))

            return cursor.fetchall()
    
    except Exception as e:
        print(f"The search description could not be vectorized: {e}")
        traceback.print_exc()
        return []