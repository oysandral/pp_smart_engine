import pytest 
import os
from src.database import DatabaseManager 
from pgvector.psycopg2 import register_vector
from src.ai_service import get_embedding

@pytest.fixture
def test_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SETTINGS_PATH = os.path.join(BASE_DIR, "test_settings.json")

    config = DatabaseManager.load_settings(SETTINGS_PATH)

    db_manager = DatabaseManager(
        localhost=config["localhost"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    connection = db_manager.get_connection()

    if connection is None:
        raise RuntimeError("No connection to the new test database.")
    yield connection

    connection.close()

@pytest.fixture
def generate_data(test_connection):
    with test_connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS products CASCADE;")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;") 

        query = ('''
                CREATE TABLE products(
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(255), 
                    description VARCHAR(255), 
                    category VARCHAR(255), 
                    price NUMERIC,
                    embedding vector(3072));
                ''')
        cursor.execute(query)

        data_to_insert = [
            ('A dall', 'Its a beautifull rare doll from the first ever collection', 'toy', 99.95),
            ('Vintage Leather Jacket', 'Authentic 90s brown bomber jacket in perfect condition', 'clothing', 145.00),
            ('Wireless Noise-Canceling Headphones', 'Premium over-ear headphones with 40 hours of battery life', 'electronics', 189.99),
            ('Organic Matcha Green Tea', 'Ceremonial grade pure green tea powder from Uji Japan', 'food', 24.50),
            ('Ergonomic Mechanical Keyboard', 'Compact 75 percent layout keyboard with hot-swappable switches', 'electronics', 120.00),
            ('Stainless Steel Water Bottle', 'Double-walled vacuum insulated flask that keeps drinks cold', 'kitchen', 29.95),
            ('Minimalist Leather Wallet', 'Slim RFID blocking card holder made of genuine leather', 'accessories', 35.00),
            ('Professional Yoga Mat', 'Non-slip extra thick eco-friendly mat for daily practice', 'sports', 65.00)
            ]

        register_vector(test_connection)

        with test_connection.cursor() as cursor:
            for name, description, category, price in data_to_insert:
                vector = get_embedding(description)

                query = ('''
                            INSERT INTO products (name, description, category, price, embedding)
                            VALUES (%s, %s, %s, %s, %s)
                            ''')
                cursor.execute(query, (name, description, category, price, vector,))
    
        test_connection.commit()

    yield test_connection