from abc import ABC, abstractmethod
from typing import Any
from util.enums import ParseType


# Interface for boilerplate text generation that each language must implement
class BpInterface(ABC):

  # TODO: comment
  @abstractmethod
  @staticmethod
  def get_start() -> str:
    pass

  # TODO: comment
  @abstractmethod
  @staticmethod
  def get_imports(included_types: set[ParseType]) -> str:
    pass
  
  # TODO: comment
  @abstractmethod
  @staticmethod
  def get_class_declaration(class_name: str, one_indent: str) -> str:
    pass

  # Returns the string representing the language method declaration corresponding
  # to the given 'parameter_names', 'parameter_types', 'return_type', 
  # and 'required_method_name', using appropriate indentation as specified by 'one_indent'.
  @abstractmethod
  @staticmethod
  def get_method_declaration(method_name: str, parameter_names: list[str], parameter_types: list[str], 
                            return_type: str, one_indent: str) -> str:
    pass
  
  # Parses a recursive JSON type description 'typ' into the corresponding language type string
  # and returns it.
  @abstractmethod
  @staticmethod
  def parse_type_string(typ: dict[str, Any]) -> str:
    pass
  
  # Returns the string representing a nested language ListNode class with val type specified
  # by 'val_type_string'.
  # Uses appropriate indentation as specified by 'base_indent' and 'one_indent'.
  @abstractmethod
  @staticmethod
  def list_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
    pass

  # Returns the string representing a TreeNode class with val type specified
  # by 'val_type_string'.
  # Uses appropriate indentation as specified by 'base_indent' and 'one_indent'.
  @abstractmethod
  @staticmethod
  def tree_node(val_type_string: str, one_indent: str, base_indent: str) -> str:
    pass
  
  # TODO: comment
  @abstractmethod
  @staticmethod
  def get_end(one_indent: str) -> str:
    pass
