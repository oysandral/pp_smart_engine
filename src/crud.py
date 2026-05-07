def get_all_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products;")
    conn.commit()

def create_product(conn, name, descr, category, price, vector):
    cursor = conn.cursor()
    query = ('''
            INSERT INTO products (name, description, category, price, embendding)
                VALUES (%s, %s, %s, %s, %s);
            ''')
    
    cursor.execute(query, (name, descr, category, price, vector))
    conn.commit()