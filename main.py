from flex_db import FlexDB

# Create a persistent database
db = FlexDB("flex_database.json")

# Use database
db.create_collection("users")
db.create_collection("orders")

# Insert records
db.insert("users", "user1", {"name": "Alice", "age": 30})
db.insert("users", "user2", {"name": "Bob", "age": 25})
db.insert("orders", "order1", {"item": "Laptop", "price": 1000})
db.insert("orders", "order2", {"item": "Phone", "price": 500})

# Read records
print(db.read("users"))
print(db.read("orders", "order1"))

# Update records
db.update("users", "user1", {"age": 31})

# Add relations
db.add_relation("users", "user1", "orders", "order1")
db.add_relation("users", "user2", "orders", "order2")

# Check relations
print(db.read("users", "user1"))

# Delete records
db.delete("orders", "order2")
