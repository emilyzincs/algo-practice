import sys
import time
from user_solution_testing.test import run_tests
from util.exceptions import UnhandledCaseException
from menu.util import handle_global_command, print_desc, to_description_lines
from typing import assert_never
from util.enums import (
  GlobalCommand,
  is_member,
  PracticeCommand,
  member_from_string,
  SpecificAlgorithm,
  Language
)

def handle_commands(
    alg: SpecificAlgorithm,
    language: Language,
    delete_attempts_func,
    load_solution_func,
    exit_func
) -> float|None:
  start_time = time.perf_counter()
  potential_end_time = None
  correct = False
  while not correct:
    user_input = input("\nType 'done' when you are finished or 'help' for options:\n")
    input_is_global_cmd = is_member(GlobalCommand, user_input)
    input_is_local_cmd = is_member(PracticeCommand, user_input)
    if not input_is_global_cmd and not input_is_local_cmd:
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    
    if input_is_global_cmd:
      global_cmd: GlobalCommand = member_from_string(GlobalCommand, user_input)
      if not handle_global_command(global_cmd, handle_help, exit_func):
        break
    elif input_is_local_cmd:
      local_cmd: PracticeCommand = member_from_string(PracticeCommand, user_input)
      match local_cmd:
        case PracticeCommand.D | PracticeCommand.DONE:
          potential_end_time = time.perf_counter()
          print("Running tests...")
          correct = run_tests(alg, language)
        case PracticeCommand.S | PracticeCommand.SOL | PracticeCommand.SOLUTION:
          try:
            load_solution_func(alg)
            print("Successfully loaded solution.")
          except FileNotFoundError:
            print(f"Cannot load solution because it does not exist.", file=sys.stderr)
        case _:
          assert_never()
    else:
      raise UnhandledCaseException(user_input, "input")

  delete_attempts_func()    
  if correct:
    if type(potential_end_time) != float:
      raise RuntimeError("Correct is true but potential_end_time is not a float.")
    return potential_end_time - start_time
  return None

def handle_help():
  command_descriptions = to_description_lines(GlobalCommand)
  command_descriptions.extend(to_description_lines(PracticeCommand))
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 
