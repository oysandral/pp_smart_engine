from src.crud import get_product_with_id, get_all_products, delete_product_crud, create_product, search_products
from src.schemas import CreateProduct

def test_connection(test_connection):
    with test_connection.cursor() as cursor:
        query = ('''
                SELECT 2 * 2;
                ''')
        cursor.execute(query)

        result = cursor.fetchone()

    assert result[0] == 4

def test_get_product_with_id(generate_data):
    test_product = get_product_with_id(generate_data, 2)

    assert test_product["name"] == "Vintage Leather Jacket"

def test_get_all_products(generate_data):
    products = get_all_products(generate_data)

    assert len(products) == 8

def test_delete_product_crud(generate_data):
    result = delete_product_crud(generate_data, 1)
    assert result is True 

    result = delete_product_crud(generate_data, 1)
    assert result is False

def test_create_product(generate_data):
    product = CreateProduct(
        name = "Sky Glider", 
        description = "Remote control airplane made of durable foam", 
        category = "Toy", 
        price = 89.9
    )
    create_product(generate_data, product)

    assert len(get_all_products(generate_data)) == 9

def test_search_products(generate_data):
    result = search_products(generate_data, "Something from Uji Japan")
    assert result[0]["name"] == "Organic Matcha Green Tea"

    result = search_products(generate_data, "Something for ice")
    assert result == []