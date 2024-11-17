import json
import os
from threading import Lock
from flex_database import FlexDatabase

class FlexDB(FlexDatabase):
  def __init__(self, storage_file="database.json"):
    super().__init__()
    self.storage_file = storage_file
    self.lock = Lock()
    self._load_from_file()

  def _load_from_file(self):
    """Load data from the storage file into memory."""
    if not os.path.exists(self.storage_file):
      print(f"File '{self.storage_file}' not found. Starting with an empty database.")
      return
    
    try:
      with open(self.storage_file, "r") as file:
        data = json.load(file)
        if isinstance(data, dict):
          self.collections = data
          print(f"Database loaded from '{self.storage_file}'.")
        else:
          print(f"Invalid data format in '{self.storage_file}'. Starting fresh.")
    except (json.JSONDecodeError, IOError) as e:
      print(f"Error reading '{self.storage_file}': {e}. Starting with an empty database.")

  def _save_to_file(self):
    """Save in-memory data to the storage file safely."""
    temp_file = self.storage_file + ".tmp"
    try:
      with open(temp_file, "w") as file:
        json.dump(self.collections, file, indent=2)
      os.replace(temp_file, self.storage_file)
      print(f"Database saved to '{self.storage_file}'.")
    except IOError as e:
      print(f"Error writing to '{self.storage_file}': {e}.")

  def create_collection(self, collection_name):
    with self.lock:
      super().create_collection(collection_name)
      self._save_to_file()

  def insert(self, collection_name, record_id, record):
    with self.lock:
      super().insert(collection_name, record_id, record)
      self._save_to_file()

  def update(self, collection_name, record_id, updates):
    with self.lock:
      super().update(collection_name, record_id, updates)
      self._save_to_file()

  def delete(self, collection_name, record_id):
    with self.lock:
      super().delete(collection_name, record_id)
      self._save_to_file()

  def delete_collection(self, collection_name):
    with self.lock:
      if collection_name in self.collections:
        del self.collections[collection_name]
        self._save_to_file()
        print(f"Collection '{collection_name}' deleted.")
      else:
        print(f"Collection '{collection_name}' does not exist.")