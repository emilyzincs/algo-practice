# Developer Documentation

This document explains the core concepts and components of the project. It is intended for contributors who need to understand the architecture before adding algorithms, languages, or tests.

> **Note**  
> Placeholder links marked `#TODO` will be replaced with actual anchors once the full documentation is assembled.

## Table of Contents
- [Developer Documentation](#developer-documentation)
  - [Table of Contents](#table-of-contents)
  - [Test Runners](#test-runners)
  - [Info Files (`info.json`)](#info-files-infojson)
  - [Test Files (`test.json`)](#test-files-testjson)
    - [Mapping language‑agnostic types to JSON](#mapping-languageagnostic-types-to-json)
  - [Language‑Agnostic Types](#languageagnostic-types)
    - [Basic structure](#basic-structure)
  - [Writing an Algorithm Solution File](#writing-an-algorithm-solution-file)
    - [Motivation](#motivation)
    - [Before you start](#before-you-start)
    - [Steps](#steps)

---

## Test Runners

A **test runner** is the core of a language implementation. Each supported language has exactly one test runner – an executable script (or compiled program) that:

1. Reads a **test file** (`test.json`) and its corresponding **info file** (`info.json`).
2. Parses each test case from the JSON into concrete values of the target language (using the language‑agnostic type definitions).
3. Calls the user’s implementation of the algorithm with those concrete inputs.
4. Compares the actual output to the expected output.
5. Prints a message and exits with:
   - **Exit code 0** if all tests pass.
   - **Non‑zero exit code** if any test fails (along with an error message).

The test runner is invoked by the main testing framework. To add a new language, you must implement its test runner (see [Adding a Language](language-addition.md#TODO)).

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

### Mapping language‑agnostic types to JSON

| language-agnostic type                   | JSON type  |
|------------------------------------------|------------|
| `int`, `long`, `float`                   | number     |
| `boolean`                                | boolean    |
| `string`                                 | string     |
| `array`, `list`, `immutable_list`, `set` | Array      |
| `map`                                    | Array of two equal-length arrays (first corresponds to keys, second to values) |

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
**Allowed collection kinds:** `array`, `list`, `immutable_list`, `set`

> The distinction between `array`, `list`, and `immutable_list` is only relevant for languages that differentiate them (e.g., Python’s `list` vs `tuple`). Test runners should map them to the most natural mutable/immutable sequence type.

---

## Writing an Algorithm Solution File

This section explains how to create a solution file for a specific algorithm in a given language.

### Motivation

Solution files enable the `solution` command. When a user practices an algorithm, they can load the official solution into their working file. Additionally, app‑level tests verify that every solution passes its generated tests, ensuring correctness across language implementations.

### Before you start

Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](algorithm-addition.md#concepts) in the algorithm addition guide).

### Steps

Pick a supported language. Let `<extension>` be the file extension for that language (e.g., `.py` for Python).

- **If the algorithm is specific** (i.e., it implements a more general algorithm, like DFS for `reachable`):  
  Path: `problems/<general_name>/<specific_name>/solution.<extension>`  
  Example: `problems/reachable/depth_first_search/solution.py`

- **If the algorithm is not specific** (i.e., it stands alone, like binary search):  
  Path: `problems/<specific_name>/solution.<extension>`  
  Example: `problems/binary_search/solution.py`

Write the solution in the file specified by the above path, creating any files or directories necessary. Make sure to follow the [implementation requirements](USER_IMPLEMENTATION.md#TODO), and note that the solution method signature types must match the description in the corresponding `info.json` file.

Once test generation is implemented for that algorithm, you can run the [app tests](#TODO) to validate your solution. They will fail if your solution does not pass the generated tests.