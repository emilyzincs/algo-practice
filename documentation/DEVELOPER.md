TODO update with links
# Sections
- Adding an Algorithm
- Adding a Language
- Running App Tests

## Test Runners

## Info Files

## (User) Test Files


## Language‑Agnostic Types

Used in `info.json` files. Each type is a dict with a `"type"` key. Possible values correspond to `ParseType` in `enums.py`. Letting `<T>` represent a nested language-agnostic type, language-agnostic types are as follows.

| Category | Example |
|----------|---------|
| Primitive | `{ "type": "int" }`, `{ "type": "string" }` |
| Collection | `{ "type": "array", "items": <T> }` |
| Map | `{ "type": "map", "keys": <T>, "values": <T> }` |

Allowed primitives: `int`, `long`, `float`, `boolean`, `string`  
Allowed collections: `array`, `list`, `immutable_list`, `set`  


## Python Types to JSON



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



