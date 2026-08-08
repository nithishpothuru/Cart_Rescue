from flask import Blueprint, jsonify
from database import products_collection

product_routes = Blueprint("product_routes", __name__)

# Seed some products if collection is empty (run once)
def seed_products():
    if products_collection.count_documents({}) == 0:
        products = [
            {
                "product_id": "P1001",
                "name": "SoundMax Pro",
                "category": "Electronics",
                "price": 89.00,
                "original_price": 149.00,
                "discount": 40,
                "rating": 4.8,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
                "badge": "40% OFF",
            },
            {
                "product_id": "P1002",
                "name": "Core Charge Stand",
                "category": "Electronics",
                "price": 29.00,
                "original_price": 39.00,
                "discount": 25,
                "rating": 4.7,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400",
                "badge": "25% OFF",
            },
            {
                "product_id": "P1003",
                "name": "Sleek Folio Leather Case",
                "category": "Accessories",
                "price": 45.00,
                "original_price": 53.00,
                "discount": 15,
                "rating": 4.6,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400",
                "badge": "15% OFF",
            },
            {
                "product_id": "P1004",
                "name": "Nova Mechanical Keyboard",
                "category": "Electronics",
                "price": 135.00,
                "original_price": 193.00,
                "discount": 30,
                "rating": 4.9,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400",
                "badge": "30% OFF",
            },
            {
                "product_id": "P1005",
                "name": "Alpha Fitband v2",
                "category": "Wearables",
                "price": 79.00,
                "original_price": 99.00,
                "discount": 20,
                "rating": 4.8,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",
                "badge": None,
            },
            {
                "product_id": "P1006",
                "name": "Orbit Smart Mug",
                "category": "Home",
                "price": 59.00,
                "original_price": 79.00,
                "discount": 25,
                "rating": 4.7,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400",
                "badge": None,
            },
            {
                "product_id": "P1007",
                "name": "Vertex Backpack Pack",
                "category": "Fashion",
                "price": 110.00,
                "original_price": 140.00,
                "discount": 21,
                "rating": 4.8,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
                "badge": None,
            },
            {
                "product_id": "P1008",
                "name": "Horizon Air Purifier",
                "category": "Home",
                "price": 199.00,
                "original_price": 249.00,
                "discount": 20,
                "rating": 4.9,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",
                "badge": None,
            },
            # Featured products from homepage
            {
                "product_id": "P2001",
                "name": "SonicBass Wireless Headset",
                "category": "Electronics",
                "price": 149.00,
                "original_price": 199.00,
                "discount": 25,
                "rating": 4.8,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
                "badge": None,
            },
            {
                "product_id": "P2002",
                "name": "Chronos Smartwatch Elite",
                "category": "Wearables",
                "price": 299.00,
                "original_price": 349.00,
                "discount": 14,
                "rating": 4.7,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
                "badge": None,
            },
            {
                "product_id": "P2003",
                "name": "AeroDry Sport Sneakers",
                "category": "Sports",
                "price": 120.00,
                "original_price": 150.00,
                "discount": 20,
                "rating": 4.9,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
                "badge": None,
            },
            {
                "product_id": "P2004",
                "name": "Nebula Smart Projector",
                "category": "Electronics",
                "price": 450.00,
                "original_price": 550.00,
                "discount": 18,
                "rating": 4.6,
                "reviews": 48,
                "image": "https://images.unsplash.com/photo-1601944179066-29786cb9d32a?w=400",
                "badge": None,
            },
        ]
        products_collection.insert_many(products)
        print("✅ Products seeded")

@product_routes.route("/api/products", methods=["GET"])
def get_products():
    seed_products()  # safe to call every time
    products = list(products_collection.find({}, {"_id": 0}))
    return jsonify({"success": True, "products": products})

@product_routes.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    product = products_collection.find_one({"product_id": product_id}, {"_id": 0})
    if not product:
        return jsonify({"success": False, "error": "Product not found"}), 404
    return jsonify({"success": True, "product": product})
