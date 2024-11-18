class SchemaValidator:
  def __init__(self, schema):
    self.schema = schema

  def validate(self, record):
    """
    Validate the record against the schema.
    """

    for field, field_type in self.schema.items():
      if isinstance(field_type, tuple):
        actual_type, required = field_type
        if required and field not in record:
          raise ValueError(f"Field '{field}' is required but missing.")
      else:
        actual_type, required = field_type, False
      
      if field in record and not isinstance(record[field], actual_type):
        raise TypeError(f"Field '{field}' should be {actual_type.__name__}, got {type(record[field]).__name__}.")
      
    return True
