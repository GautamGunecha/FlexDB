from threading import Lock

class SafeLock:
  def __init__(self):
    self._lock = Lock()

  def synchronized(self, func):
    """
    Decorator to make a method thread-safe.
    """
    def wrapper(*args, **kwargs):
      with self._lock:
        return func(*args, **kwargs)
    return wrapper
