import random

def get_random_string(size: int, num_allowed_chars: int) -> str:
  if num_allowed_chars < 0 or 128 <= num_allowed_chars:
    raise ValueError("num_allowed_chars must be between 0 and 127 (inclusive).")
  # base_char_code = 33
  # allowed_chars = [chr(base_char_code + i) for i in range(num_allowed_chars)]
  
  return ''.join(random.choices([chr(i) for i in range(num_allowed_chars)], k=size))