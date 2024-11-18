from .persistence import PersistentStorage
from .locks import SafeLock
from .schema_validation import SchemaValidator

class FlexDB:
  def __init__(self, storage_file="database.json"):
    self.storage = PersistentStorage(storage_file)
    self.lock = SafeLock()
    self.collections = self.storage.load()
    self.schemas = {}

  def create_collection(self, collection_name, schema=None):
    @self.lock.synchronized
    def create():
      if collection_name in self.collections:
        print(f"Collection '{collection_name}' already exists.")
        return

      self.collections[collection_name] = {}
      if schema:
        self.schemas[collection_name] = SchemaValidator(schema)
      self.storage.save(self.collections)
      print(f"Collection '{collection_name}' created.")
    create()

  def insert(self, collection_name, record_id, record):
    @self.lock.synchronized
    def insert():
      if collection_name not in self.collections:
        print(f"Collection '{collection_name}' does not exist.")
        return
    
      if collection_name in self.schemas:
        try:
          self.schemas[collection_name].validate(record)
        except (ValueError, TypeError) as e:
          print(f"Insert failed: {e}")
          return
      
      self.collections[collection_name][record_id] = record
      self.storage.save(self.collections)
      print(f"Record added to '{collection_name}' with ID '{record_id}'.")
    insert()

  def read(self, collection_name, record_id=None):
    @self.lock.synchronized
    def read():
      if collection_name not in self.collections:
        print(f"Collection '{collection_name}' does not exist.")
        return None
      if record_id:
        return self.collections[collection_name].get(record_id, f"No record with ID '{record_id}'.")
      return self.collections[collection_name]
    return read()
  
  def update(self, collection_name, record_id, updates):
    @self.lock.synchronized
    def update():
      if collection_name not in self.collections:
        print(f"Collection '{collection_name}' does not exist.")
        return
      if record_id not in self.collections[collection_name]:
        print(f"No record with ID '{record_id}' in '{collection_name}'.")
        return
      
      # Apply updates and validate
      current_record = self.collections[collection_name][record_id]
      updated_record = {**current_record, **updates}
      if collection_name in self.schemas:
        try:
          self.schemas[collection_name].validate(updated_record)
        except (ValueError, TypeError) as e:
          print(f"Update failed: {e}")
          return
      
      self.collections[collection_name][record_id] = updated_record
      self.storage.save(self.collections)
      print(f"Record with ID '{record_id}' updated in '{collection_name}'.")
    update()

  def delete(self, collection_name, record_id):
    @self.lock.synchronized
    def delete():
      if collection_name not in self.collections:
        print(f"Collection '{collection_name}' does not exist.")
        return
      
      if record_id in self.collections[collection_name]:
        del self.collections[collection_name][record_id]
        self.storage.save(self.collections)
        print(f"Record with ID '{record_id}' deleted from '{collection_name}'.")
      else:
        print(f"No record with ID '{record_id}' to delete in '{collection_name}'.")
    delete()

  def delete_collection(self, collection_name):
    @self.lock.synchronized
    def delete():        
      if collection_name in self.collections:
        del self.collections[collection_name]
        self.storage.save(self.collections)
        print(f"Collection '{collection_name}' deleted.")
      else:
        print(f"Collection '{collection_name}' does not exist.")
    delete()

