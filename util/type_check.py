def is_type(str: str, type_constructor) -> bool:
  try:
    type_constructor(str)
    return True
  except ValueError:
    return False

def string_to_bool(str: str) -> bool:
  str = str.strip().lower()
  if str == "true":
    return True
  elif str == "false":
    return False
  else:
    raise ValueError(f"Str must be either 'true' or 'false'. Was {str}")
