import json
import os

class PersistentStorage:
  def __init__(self, storage_file = "flex_db.json"):
    self.storage_file = storage_file

  def load(self):
    """
    Load data from the storage file.
    """

    if not os.path.exists(self.storage_file):
      print(f"File '{self.storage_file}' not found. Starting with an empty database.")
      return {}
    
    try:
      with open(self.storage_file, "r") as file:
        data = json.load(file)
        if isinstance(data, dict):
          return data
        else:
          print(f"Invalid data format in '{self.storage_file}'. Starting fresh.")
          return {}
    except (json.JSONDecodeError, IOError) as e:
      print(f"Error reading '{self.storage_file}': {e}. Starting with an empty database.")
      return {}
    
  def save(self, data):
    """
    Save data to the storage file safely.
    """

    temp_file = self.storage_file + ".tmp"
    try:
      with open(temp_file, "w") as file:
        json.dump(data, file, indent=2)
        os.replace(temp_file, self.storage_file)
        print(f"Database saved to '{self.storage_file}'.")
    except IOError as e:
      print(f"Error writing to '{self.storage_file}': {e}.")

