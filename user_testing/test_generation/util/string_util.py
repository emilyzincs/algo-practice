import random

def get_random_string(size: int, num_allowed_chars: int) -> str:
  base_char_code = 33
  allowed_chars = [chr(base_char_code + i) for i in range(num_allowed_chars)]
  
  return ''.join(random.choices(allowed_chars, k=size))