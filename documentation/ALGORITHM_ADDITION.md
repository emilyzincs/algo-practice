# Adding an Algorithm

This guide walks through adding a new algorithm to the system. You’ll update enums, create config files, and (if needed) set up test generation.

> **Before you start**  
> Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](#concepts)). 

## Concepts

Take **depth‑first search (DFS)**:
- It is a *specific* algorithm – one way to implement the more general “reachable” algorithm (BFS is another).
- **Binary search** is *not* specific – there is no broader “search” general algorithm that both binary search and linear search implement (in our system’s sense).

We use three naming conventions:

| Concept | Format | Example (DFS) |
|---------|--------|----------------|
| Alias | lowercase, spaces between words | `"dfs"`, `"depth first search"` |
| Specific name | snake_case | `depth_first_search` |
| General name | snake_case; if not specific, same as specific | `reachable` (for DFS) |

> The algorithm’s own name (in lowercase with spaces) is always an alias. So `"depth first search"` is an alias of itself.

## Step‑by‑step instructions

We’ll use **depth‑first search** as the running example.  
Assume its specific name is `depth_first_search` and its general name is `reachable`.

### 1. Update `enums.py`

- Add `<SPECIFIC_NAME>` (all caps, snake case) to `SpecificAlgorithm`:
  ```python
  class SpecificAlgorithm(Enum):
      # ...
      DEPTH_FIRST_SEARCH = auto()
  ```

- Add each alias to `INPUT_ALG_TO_SPECIFIC`:
  ```python
  INPUT_ALG_TO_SPECIFIC = {
      # ...
      "dfs": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
      "depth first search": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  }
  ```

- Add `<GENERAL_NAME>` to `GeneralAlgorithm` if new:
  ```python
  class GeneralAlgorithm(Enum):
      # ...
      REACHABLE = auto()
  ```

- Add mapping from specific → general in `SPECIFIC_ALG_TO_GENERAL`:
  ```python
  SPECIFIC_ALG_TO_GENERAL = {
      # ...
      SpecificAlgorithm.DEPTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  }
  ```

**If `<GENERAL_NAME>` already existed**, you’re done. Otherwise, continue to create the general algorithm folder.

### 2. Create the general algorithm folder (only if new)

Inside the `problems/` directory, create a folder named `<general_name>` (e.g., `problems/reachable/`).  
Inside it, create `info.json` with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `"unique_answer"` | boolean | Does this algorithm have exactly one solution per problem instance? |
| `"parameter_names"` | array of strings | Human‑readable names for parameters, in order (e.g., `["graph", "start"]`) |
| `"input_types"` | array of [language‑agnostic types](#languageagnostic-types-reference) | Types of the parameters, in order |
| `"expected_type"` | [language‑agnostic type](#languageagnostic-types-reference) | Return type |

### 3. Generate tests (if the general algorithm is new)

- Go to `test_generation/problems/` and create `<general_name>.py` (e.g., `reachable.py`).
- Define a class named `<GeneralName>Generator` (PascalCase) that extends `BaseGenerator`.
- Override all `@abstractmethod` methods. Do **not** override `@final` methods.
- Use helpers from `command_util` and write custom helpers as needed.

The program will automatically use the generator to create the tests when necessary. Since these tests will be used to validate the correctness of algorithm implementations, it is paramount that they are as exhaustive as possible.

