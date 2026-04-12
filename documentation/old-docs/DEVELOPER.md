TODO update with links
# Sections
- Adding an Algorithm
- Adding a Language
- Running App Tests

## Test Runners
Test runners are the core of a language implementation. Each language has one test-runner, which is responsible for using [language-agnostic types](#todo) to parse JSON into concrete types in the language. In particular, given an algorithm, a test-runner must use the corresponding [info file](#TODO) to parse tests in the corresponding [test file](#TODO) into concrete inputs and expected outputs. It is called a test-runner, because after doing this parsing, it calls the user's current implementation of the algorithm with the concrete inputs, and verifies that the outputs matches the expected--running the tests. If any test fails, it prints an error message and exits with nonzero status code, otherwise it prints that all tests passed and exits with status code zero.

## Info Files (JSON)
Algorithm info files (named `info.json`) are JSON objects which hold useful information for [test-runners](#TODO) for parsing/validating tests in the corresponding [test file](#TODO). Each [general algorithm](#todo) has exactly one info file, located in `problems/<general_name>/`, where `<general_name>` is the general algorithm's name in snake_case. Info files hold the following.

| Key | Type | Description |
|-----|------|-------------|
| `"unique_answer"` | boolean | Does this algorithm have exactly one solution per problem instance? |
| `"parameter_names"` | array of strings | Human‑readable names for the algorithm parameters, in order (e.g., `["graph", "start"]`) |
| `"input_types"` | array of [language‑agnostic types](#TODO) | Types of the algorithm parameters, in order |
| `"expected_type"` | [language‑agnostic type](#TODO) | Return type |

## Test Files (JSON)
Algorithm test files (named test.json) are JSON arrays of test cases. Each [general algorithm](#todo) has exactly one test file, located in `problems/<general_name>/`, where `<general_name>` is the general algorithm's name in snake_case. Each test file has the form:
```
{
  "inputs": [...]
  "expected": ...
}
```
Where `"inputs"` holds the list of parameter values (in order) for the test case, and `"expected"` holds the expected output of the algorithm.

The JSON type of each parameter value and expected return value must match the corresponding [language-agnostic type](#TODO) in the corresponding [info file](#TODO). This means recursively matching:

| language-agnostic type                   | JSON type  |
|------------------------------------------|------------|
| `int`, `long`, `float`                   | number     |
| `boolean`                                | boolean    |
| `string`                                 | string     |
| `array`, `list`, `immutable_list`, `set` | Array      |
| `map`                                    | Array holding two Arrays of equal size  |


## Language‑Agnostic Types

Used in [info files](#TODO). Each type is an object with a `"type"` key. Possible values correspond to `ParseType` in `enums.py`. Letting `<T>` represent a nested language-agnostic type, language-agnostic types are as follows.

| Category   | Example                                         |
|------------|-------------------------------------------------|
| Primitive  | `{ "type": "int" }`, `{ "type": "string" }`     |
| Collection | `{ "type": "array", "items": <T> }`             |
| Map        | `{ "type": "map", "keys": <T>, "values": <T> }` |

Allowed primitives: `int`, `long`, `float`, `boolean`, `string`  
Allowed collections: `array`, `list`, `immutable_list`, `set`  


### Writing an Algorithm Solution File
This section covers how to create a solution file for an algorithm in a particular language. 

#### Motivation
Solution files enable users to use the `solution` command when the practicing the algorithm in that language, which loads the solution into their practice file. They also make the program more robust, since the app-level tests check that all solutions pass their corresponding (generated) tests.

> **Before you start**  
> Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](#TODO))

Pick a supported language. Let `<extension>` be the file extension for that language (e.g., `.py`).

- **If the algorithm is specific** (e.g., DFS):  
  Path: `problems/<general_name>/<specific_name>/solution.<extension>`  
  Example: `problems/reachable/depth_first_search/solution.py`

- **If the algorithm is not specific** (e.g., binary search):  
  Path: `problems/<specific_name>/solution.<extension>`  
  Example: `problems/binary_search/solution.py`

Follow the [implementation requirements](USER_IMPLEMENTATION.md).  
Once test generation is in place, run the [app tests](#TODO) to validate your solution – they will fail if your solution does not pass the user tests.
