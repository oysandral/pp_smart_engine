import psycopg2

try:
    connection = psycopg2.connect(
        host = "localhost",
        user = "admin_user",
        password = "1234password",
        database = "smart_rec_db"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"We successfully have connected with database {cursor}.")

    cursor.execute('''INSERT INTO products (name, description, category, price, embedding)
                       VALUES ('Green apple', 'Healthy apple from the organic farm', 'fruit', 1.5, '[0.1, 0.2, 0.3]')
                        ''')
    connection.commit()
    print(f'Data inserted successfully!')

    cursor.execute('''SELECT * FROM products;''')
    all_products = cursor.fetchall()
    for row in all_products:
        print(row, ' ')


except Exception as e:
    print(f"You have problems with connection {e}")

finally:
    if 'connection' in locals():
        cursor.close()
        connection.close()