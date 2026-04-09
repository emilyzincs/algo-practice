from typing import Any
from util.enums import ParseType, is_member


# Validates that the given 'typ' is (locally) a language-agnostic type representation
# matching the expected representation.
#
# I.e., that it is a dictionary with strings for keys where "type" is one key,
# the value corresponding to "type" is a string, and that value corresponds to a ParseType.
#
# Raises ValueError if any of the checks fail.
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
