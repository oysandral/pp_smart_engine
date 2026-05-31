from ai_service import get_embedding

def get_all_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products;")
    conn.commit()

    result = cursor.fetchall()

    return result

def create_product(conn, name : str, description : str, category : str, price : float):
    cursor = conn.cursor()
    query = ('''
            INSERT INTO products (name, description, category, price, embedding)
                VALUES (%s, %s, %s, %s, %s);
            ''')
    
    vector = get_embedding(description)

    if not vector:
        vector = [0.0] * 3072
    
    cursor.execute(query, (name, description, category, price, str(vector)))
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