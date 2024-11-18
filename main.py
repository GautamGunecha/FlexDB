from database import FlexDB

# Create a persistent database
db = FlexDB("flex_database.json")

# Create collections with schemas
# db.create_collection("users", schema={"name": str, "age": (int, True), "email": (str, False)})
# db.create_collection("products", schema={"name": str, "price": (float, True), "in_stock": (bool, True)})


# Insert records
# db.insert("users", "user1", {"name": "Alice", "age": 30, "email": "alice@example.com"})
# db.insert("products", "prod1", {"name": "Laptop", "price": 1000.0, "in_stock": True})

# Read records
print(db.read("users"))
print(db.read("products"))