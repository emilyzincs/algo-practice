from typing import Any
from util.enums import ParseType, is_member

def validate_type(typ: dict[str, Any]) -> None:
  if type(typ) != dict:
    raise ValueError(f"Not a dict: {typ}.")
  if "type" not in typ:
    raise ValueError(f"Type dicts must contain a 'type' field. Dict: {typ}.")
  if not type(typ["type"]) == str:
    raise ValueError("The  corresponding to 'type' in a type dict must be a string." +
                     f" Dict: {typ}.")
  if not is_member(ParseType, typ["type"]):
   raise ValueError("The value corresponding to 'type' in a type dict must be a ParseType type." +
                    f" Dict: {typ}.") 
