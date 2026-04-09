# Attempts to convert a string using the given type constructor (e.g., int, float).
# Returns True if conversion succeeds without ValueError, otherwise False.
def is_type(str: str, type_constructor) -> bool:
  try:
    type_constructor(str)
    return True
  except ValueError:
    return False


# Converts a case‑insensitive string 'true' or 'false' to a boolean.
# Raises ValueError if the string is neither 'true' nor 'false'.
def string_to_bool(str: str) -> bool:
  str = str.strip().lower()
  if str == "true":
    return True
  elif str == "false":
    return False
  else:
    raise ValueError(f"Str must be either 'true' or 'false'. Was {str}")
