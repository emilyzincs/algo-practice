# Developer Documentation

This document explains the core concepts and components of the project. It is intended for contributors who need to understand the architecture before adding algorithms, languages, or tests.


## Table of Contents
- [Developer Documentation](#developer-documentation)
  - [Table of Contents](#table-of-contents)
  - [Test Runners](#test-runners)
    - [Command-Line Arguments](#command-line-arguments)
    - [Implementation Advice](#implementation-advice)
  - [Info Files (`info.json`)](#info-files-infojson)
  - [Test Files (`test.json`)](#test-files-testjson)
  - [Language‑Agnostic Types](#languageagnostic-types)
    - [Basic structure](#basic-structure)
  - [Language-Agnostic Types to Language Types](#language-agnostic-types-to-language-types)
    - [JSON](#json)
    - [Python](#python)
    - [Java](#java)
  - [Writing an Algorithm Solution File](#writing-an-algorithm-solution-file)
    - [Motivation](#motivation)
    - [Steps](#steps)
  - [App Tests](#app-tests)
    - [Running the tests](#running-the-tests)
      - [Additional arguments](#additional-arguments)
    - [Auxiliary Files](#auxiliary-files)
      - [The `test_run_tests` test](#the-test_run_tests-test)
      - [The `test_boilerplate` test](#the-test_boilerplate-test)

---

## Test Runners

A **test-runner** is the core of a language implementation. It is an executable that runs algorithm tests for a language, placed in `test_runners/<language>/`. 

The runner should typically be written in the target language itself, but under certain circumstances, it may be advantageous in to write it in a scripting language (e.g., Python) that invokes the target language’s toolchain.

**Required behavior:**

Given a user's algorithm implementation, written in the target language, the test-runner:
1. Reads the algorithm's [test file](#TODO) and [info file](#todo).
2. Parses each test case in the test file from JSON into **concrete** values of the target language (using the [type definitions](#TODO) in the info file).
3. Calls the user’s algorithm implementation with those concrete inputs.
4. Compares the **actual** output to the **expected** output.
5. Raises an **error** if any previous step fails.
6. Prints a message and exits with:
   - **Exit code 0** if all tests pass.
   - **Non‑zero exit code** if any test fails (along with an error message).

### Command-Line Arguments

Test-runners must be passed the necessary command-line arguments to fulfill their duty. These arguments vary by language (for example, the Java test-runner requires class-paths as one argument). However, some arguments should usually or pretty much always be included. They are shared below.

| Variable | Description |
|----------|-------------|
| `<practice_file>` | Path to the user’s implementation file for the current algorithm in the current language. |
| `<info_file>` | Path to the `info.json` file for the current algorithm. |
| `<test_file>` | Path to the `test.json` file for the current algorithm. |
| `<PROJECT_ROOT>` | Path to the project root. |
| `<debug>` | String that is either `"True"` or `"False"` indicating whether to print stacktraces/detailed error messages. |
| `<required_class_name>` | The name the class containing the algorithm implementation must have. |
| `<required_method_name>` | The name the method implementing the algorithm must have. |
| `<parse_types_list>` | The list of current language‑agnostic types the program supports as strings in order (e.g. `["int", "long", ...]`), serialized as a JSON string. This enables runners to check that their handled types are not outdated.

### Implementation Advice
- Use a JSON library to initially load the JSON files into concrete types.
- Validate command-line arguments match the expected form.
- Use a custom version of the `ParseType` enum for static type safety, and check that the `ParseType` enum matches `<parse_types_list>` argument for runtime safety.
- Create a recursive function for parsing the (initially loaded) test JSON items into values in the target language that match their language-agnostic type.
- Potentially, add a function for parsing a language-agnostic type into a type in the target language. 

> **Tip:** Look at existing test runners (e.g., `runner.py`) for concrete examples.

---

## Info Files (`info.json`)

Every **general algorithm** has exactly one `info.json` file, located in `problems/<general_name>/` (where `<general_name>` is the snake‑case name of the general algorithm).

The file is a JSON object with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `"unique_answer"` | boolean | Does this algorithm have exactly one correct solution per problem instance? (Used for certain test generation strategies.) |
| `"parameter_names"` | array of strings | Human‑readable names for the algorithm’s parameters, in order (e.g., `["graph", "start"]`). |
| `"input_types"` | array of [language‑agnostic types](#languageagnostic-types) | The expected type of each parameter, in the same order. |
| `"expected_type"` | [language‑agnostic type](#languageagnostic-types) | The return type of the algorithm. |

Example `info.json` for binary search:
```json
{
  "unique_answer": false,
  "parameter_names": ["nums", "target"],
  "input_types": [
    { "type": "array",
      "items": { "type": "int" }
    },
    { "type": "int" }
  ],
  "expected_type": { "type": "int" }
}
```

---

## Test Files (`test.json`)

Each **general algorithm** also has exactly one `test.json` file, stored in the same folder as its `info.json` file (`problems/<general_name>/test.json`).

The file is a JSON **array** of test case objects. Each test case object has two fields:

- `"inputs"`: an array of input values (in the same order as `parameter_names` in the info file).
- `"expected"`: the expected output value.

The JSON representation of each input and the expected output must match the corresponding [language‑agnostic type](#languageagnostic-types) from the info file.

---

## Language‑Agnostic Types

These types are used in `info.json` files to describe algorithm interfaces irrespective of programming language. Each type is a JSON object with a `"type"` key. The allowed values correspond to the `ParseType` enum in `enums.py`.

### Basic structure

Let `<T>` represent a nested language‑agnostic type.

| Category   | Example                                         |
|------------|-------------------------------------------------|
| Primitive  | `{ "type": "int" }`, `{ "type": "string" }`     |
| Collection | `{ "type": "array", "items": <T> }`             |
| Map        | `{ "type": "map", "keys": <T>, "values": <T> }` |

**Allowed primitives:** `int`, `long`, `float`, `boolean`, `string`  
**Allowed collections:** `array`, `list`, `immutable_list`, `set`

> The distinction between `array`, `list`, and `immutable_list` is only relevant for languages that differentiate them (e.g., Python’s `list` vs `tuple`). Test runners should map them to the most natural mutable/immutable sequence type.

---

## Language-Agnostic Types to Language Types

### JSON

| Language-Agnostic Type                   | Language Type  |
|------------------------------------------|------------|
| `int`, `long`, `float`                   | number     |
| `boolean`                                | boolean    |
| `string`                                 | string     |
| `array`, `list`, `immutable_list`, `set` | Array      |
| `map`                                    | Array of two equal-length arrays (first corresponds to keys, second to values) |

### Python

| Language-Agnostic Type                   | Language Type|
|------------------------------------------|------------|
| `int`, `long`                            | int        |
| `float`                                  | float      |
| `boolean`                                | bool       |
| `string`                                 | str        |
| `array`, `list`                          | list       |
| `immutable_list`                         | tuple      |
| `set`                                    | set        |
| `map`                                    | dict       |

### Java

| Language-Agnostic Type                   | Language Type  |
|------------------------------------------|------------|
| `int`                                    | int        |
| `long`                                   | long       |
| `float`                                  | double     |
| `boolean`                                | boolean    |
| `string`                                 | string     |
| `array`, `immutable_list`                | Array      |
| `list`                                   | List       |
| `set`                                    | Set        |
| `map`                                    | Map        |

>Note: If a primitive appears in a non-array language-agnostic collection type, then its Java type will be boxed to an object. For example, below, the language-agnostic `"int"` corresponds to Java `Integer`.
```
{ "type": "list", "items": { "type": "int" } } <-> List<Integer>
```

---

## Writing an Algorithm Solution File

This section explains how to create a solution file for a specific algorithm in a given language.

### Motivation

Solution files enable the `solution` command. When a user practices an algorithm, they can load the official solution into their working file. Additionally, app‑level tests verify that every solution passes its generated tests, ensuring correctness across language implementations.

>**Before you start**
>Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](algorithm-addition.md#concepts) in the algorithm addition guide).

### Steps

Pick a supported language. Let `<extension>` be the file extension for that language (e.g., `.py` for Python).

- **If the algorithm is specific** (i.e., it implements a more general algorithm, like DFS for `reachable`):  
  Path: `problems/<general_name>/<specific_name>/solution.<extension>`  
  Example: `problems/reachable/depth_first_search/solution.py`

- **If the algorithm is not specific** (i.e., it stands alone, like binary search):  
  Path: `problems/<specific_name>/solution.<extension>`  
  Example: `problems/binary_search/solution.py`

Write the solution in the file specified by the above path, (create any files or directories that do not exist). Make sure to follow the [implementation requirements](USER_IMPLEMENTATION.md#TODO), and note that the solution method signature types must match the description in the corresponding `info.json` file.

Once test generation is implemented for that algorithm, you can run the [app tests](#TODO) to validate your solution. They will fail if your solution does not pass the generated tests.

---

## App Tests

The app tests are the files at the top level of the `app_tests` folder whose names start with `test_`. 

### Running the tests
The script used to run the app tests is `test.py`, located in the project root. To run all the tests, navigate to the project root in the terminal and enter
```
python test.py
```

#### Additional arguments
| Argument  | Description                                                                                          |
|------------|------------------------------------------------------------------------------------------------------|
| `test`     | A specific test to run. This is the name of a test file, but without the `test_` prefix or the language extension.  E.g., `boilerplate` instead of `test_boilerplate.py`. |
| `language` | The language to test, for tests that depend on language. If not specified, all languages are tested. |
| `alg`      | The algorithm to test, for tests that run specific algorithms. If not specified, all algorithms are tested. |
| `num`      | The `num`th set of files to test, for tests that use the files in `app_tests/json_files`. See [TODO]() for more details. If not specified, all files are tested.                                                                            |
| `debug`    | String that is `"true"` or `"false"` indicating whether stacktraces and detailed error messages should be printed. |

For example, to test the Java boilerplate generation for the 14th pair of JSON files, run
```
python test.py --test boilerplate --num 14 --language Java
```
from the project root. Note the order of the additional arguments does not matter.

### Auxiliary Files
The `app_tests/json_files` contains a number (lets say `N`) of test-info file pairs, named `test1.json, info1.json`, `test2.json, info2.json`, ..., `testN.json, infoN.json`.

As hinted above, some tests make use of these files.

#### The `test_run_tests` test

This test checks that the `run_tests` function in `user_testing/test.py` accurately reports the correctness of implementations for the auxiliary files.

In addition to using the auxiliary files, it requires that for each language there is a directory 
```
app_test/language/<language>/solution_files/
```
containing files `<sol>1.<extension>`, `<sol>2.<extension>`, ..., `<sol>N.<extension>`, where `<language>` is the language name in lowercase, `<sol>` is "sol" in the language's file-name-case (e.g., "Sol" in Java), and `<extension>` is the language's file extension (e.g., ".py" in Python).

The `k`th solution file should correctly implement the `k`th pair of auxiliary files if the `k`th entry of the `expected_values` list (one-indexed) in the `language_test_run_tests` function is `True`, otherwise it should not.

>Implementation Tip: If you are adding a new language, copy and paste the `solution_files` folder of an already implemented language, and translate it into the new language. Alternatively, it may be faster to start with the [boilerplate files](TODO) for the language, and write the implementations for there.

#### The `test_boilerplate` test
This test checks that the starting boilerplate text generation for practice files works correctly

In addition to using the auxiliary files, it requires that for each language there is a directory 
```
app_test/language/<language>/boilerplate_files/
```
containing files `<bp>1.<extension>`, `<bp>2.<extension>`, ..., `<bp>N.<extension>`, where `<language>` is the language name in lowercase, `<bp>` is "bp" in the language's file-name-case (e.g., "Bp" in Java), and `<extension>` is the language's file extension (e.g., ".py" in Python).

The `k`th boilerplate file must contain a character-perfect copy of the expected boilerplate for the `k`th pair of auxiliary files in the target language.
