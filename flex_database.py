class FlexDatabase:
  def __init__(self):
    self.collections = {}

  def create_collection(self, collection_name):
    if collection_name in self.collections:
      print(f"Collection {collection_name} already exists.")
    else:
      self.collections[collection_name] = {}
      print(f"Collection '{collection_name}' created.")

  def insert(self, collection_name, record_id, record):
    if collection_name not in self.collections:
      print(f"Collection '{collection_name}' does not exist.")
      return
    if record_id in self.collections[collection_name]:
      print(f"Record with ID '{record_id}' already exists in '{collection_name}'.")
      return
    self.collections[collection_name][record_id] = record
    print(f"Record added to '{collection_name}' with ID '{record_id}'.")

  def read(self, collection_name, record_id=None):
    if collection_name not in self.collections:
      print(f"Collection '{collection_name}' does not exist.")
      return None
    if record_id:
      return self.collections[collection_name].get(record_id, f"No record with ID '{record_id}'.")
    return self.collections[collection_name]
  
  def update(self, collection_name, record_id, updates):
    if collection_name not in self.collections:
      print(f"Collection '{collection_name}' does not exist.")
      return
    if record_id not in self.collections[collection_name]:
      print(f"No record with ID '{record_id}' in '{collection_name}'.")
      return
    self.collections[collection_name][record_id].update(updates)
    print(f"Record with ID '{record_id}' updated in '{collection_name}'.")

  def delete(self, collection_name, record_id):
    if collection_name not in self.collections:
      print(f"Collection '{collection_name}' does not exist.")
      return
    if record_id in self.collections[collection_name]:
      del self.collections[collection_name][record_id]
      print(f"Record with ID '{record_id}' deleted from '{collection_name}'.")
    else:
      print(f"No record with ID '{record_id}' to delete in '{collection_name}'.")

  def add_relation(self, collection_name, record_id, related_collection, related_id):
    if collection_name not in self.collections or related_collection not in self.collections:
      print("One or both collections do not exist.")
      return
    if record_id not in self.collections[collection_name] or related_id not in self.collections[related_collection]:
      print("One or both records do not exist.")
      return
    
    record = self.collections[collection_name][record_id]

    if "_relations" not in record:
      record["_relations"] = {}
    if related_collection not in record["_relations"]:
      record["_relations"][related_collection] = []

    record["_relations"][related_collection].append(related_id)
    print(f"Relation added: {record_id} -> {related_collection}:{related_id}")
