from util.file_paths import get_boilerplate_language_file_path
from typing import assert_never, Any
from util.enums import Language, ParseType, member_from_string, member_to_capitalized_words
from util.general import load_module_from_path
from boilerplate.util import validate_type
from boilerplate.interface import BpInterface


# Instance of the class that implements the BpInterface
# corresponding to the current language
BP_LANG_INSTANCE: BpInterface


# Gets the boilerplate text to prepopulate a practice file with
# if the prepopulate boilerplate setting is set to true
#
# Parameters:
# - parameter_names: The variable names to use for the parameters, in order
# - input_types: Recursive language-agnostic representations of the types of
#                the paremeters, in order
# - expected_type: Recursive language-agnostic representation of the return type
# - one_indent: The string to use as one indent (e.g. "  ")
# - alg_name: The name of the algorithm this is boilerplate for
# - comment_symbol: The line-level comment symbol for the current language (e.g. '#' for Python)
# - solution_class_name: Name to use for the class
# - solution_function_name: Name to use for the method that tests call
# - language: The current program language
def get_boilerplate_text(
  parameter_names: list[str],
  input_types: list[dict[str, Any]],
  expected_type: dict[str, Any],
  one_indent: str,
  comment_symbol: str,
  alg_name: str,
  solution_class_name: str,
  solution_function_name: str,
  language: Language
) -> str:
  _set_bp_lang_class(language)

  parameter_type_strings = [BP_LANG_INSTANCE.parse_type_string(input_type) for input_type in input_types]
  return_type_string = BP_LANG_INSTANCE.parse_type_string(expected_type)
  included_types: set[ParseType] = _add_all_nested_types(input_types, expected_type)

  start = BP_LANG_INSTANCE.get_start()
  imports = BP_LANG_INSTANCE.get_imports(included_types)

  class_prefix = f"{comment_symbol} Algorithm: {alg_name}.\n"
  class_declaration = (class_prefix + 
          BP_LANG_INSTANCE.get_class_declaration(solution_class_name, one_indent))
  
  method_declaration = BP_LANG_INSTANCE.get_method_declaration(
    solution_function_name,
    parameter_names, 
    parameter_type_strings, 
    return_type_string, 
    one_indent
  )

  end = BP_LANG_INSTANCE.get_end(one_indent)

  if start:
    start += "\n"
  if imports:
    imports += "\n"

  ret = "".join([
    start,
    imports,
    class_declaration, 
    method_declaration,
    end
  ])

  return ret


# Updates BP_LANG_INSTANCE using the given Language
# Raises:
# - ImportError if loading the module containing the class fails
# - TypeError if the class does not inherit from BpInterface
def _set_bp_lang_class(lang: Language) -> None:
  lang_class_name = member_to_capitalized_words(lang).replace(" ", "") + "Bp"
  path = get_boilerplate_language_file_path(lang)

  global BP_LANG_INSTANCE
  module = load_module_from_path(lang_class_name, path)
  BP_LANG_INSTANCE = getattr(module, lang_class_name)()
  if not issubclass(type(BP_LANG_INSTANCE), BpInterface):
    raise TypeError(f"{lang_class_name} must inherit from BpInterface.")


# Recursively adds all ParseTypes specified by 'typ' to the set 's',
# where 'typ' is a language-agnostic representation of a type.
#
# Example: If typ is { "type": "array", "items": { "type": "int" }},
#   then this function will add ParseType.ARRAY and ParseType.INT to s.
def _add_nested_types(typ: dict[str, Any], s: set[ParseType]) -> None:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])
  s.add(curr_type)
  match curr_type:
    case ParseType.INT | ParseType.LONG | ParseType.FLOAT | ParseType.BOOLEAN | ParseType.STRING:
      pass
    case ParseType.ARRAY | ParseType.LIST | ParseType.HASHABLE_LIST | ParseType.SET | ParseType.HASHABLE_SET:
      _add_nested_types(typ["items"], s)
    case ParseType.MAP:
      _add_nested_types(typ["keys"], s)
      _add_nested_types(typ["values"], s)
    case _:
      assert_never(curr_type)


# Returns the set of all ParseTypes appearing in input_types and expected_type
# To understand what it means for a ParseType to appear in a language-agnostic
# type representation, see the comment for the _add_nested_types() function
def _add_all_nested_types(input_types: list[dict[str, Any]],
                          expected_type: dict[str, Any]) -> set[ParseType]:
  ret: set[ParseType] = set()
  for input_type in input_types:
    _add_nested_types(input_type, ret)
  _add_nested_types(expected_type, ret)
  return ret


# Recursively searches through 'typ' until finding a 'typ' whose "type" value 
#   is the string representation of the ParseType 'to_find', and returns that 'typ'.
# Returns None if no such 'typ' exists.
def _find_type(typ: dict[str, Any], to_find: ParseType) -> dict[str, Any] | None:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])
  if curr_type == to_find:
    return typ
  match curr_type:
    case ParseType.INT | ParseType.LONG | ParseType.FLOAT | ParseType.BOOLEAN | ParseType.STRING:
      return None
    case ParseType.ARRAY | ParseType.LIST | ParseType.HASHABLE_LIST | ParseType.SET | ParseType.HASHABLE_SET:
      return _find_type(typ["items"], to_find)
    case ParseType.MAP:
      key_typ = _find_type(typ["keys"], to_find)
      return key_typ if key_typ is not None else _find_type(typ["values"], to_find)
    case _:
      assert_never(curr_type)


# Recursively searches the language-agnostic type representations in
# 'input_types' and 'expected_type' to find a (possibly nested) representation
# of a type whose "type" value is a string representation of 'to_find'.
# Then returns the language-specific representation of that types 'field' field.
# 
# For example, if 'to_find' is ParseType.LISTNODE and 'field' is 'val', and
# the first part of this function finds { "type": "ListNode", "val": "float" },
# then if the language is Java, it will return "double", since double is the Java
# representation of ParseType.FLOAT.
#
# Raises RuntimError if the first part of the function fails.
def _get_nested_type_string(to_find: ParseType, field: str, 
                           input_types: list[dict[str, Any]], expected_type: dict[str, Any]) -> str:
  typ: dict[str, Any] | None = None
  for input_type in input_types:
    curr = _find_type(input_type, to_find)
    if curr is not None:
      typ = curr
      break
  if typ is None:
    typ = _find_type(expected_type, to_find)
  if typ is None:
    raise RuntimeError(f"Type not found: {to_find}")
  return BP_LANG_INSTANCE.parse_type_string(typ[field])
