# Adding an Algorithm

This guide walks through adding a new algorithm to the system. You will update enums, create configuration files, and (if needed) set up test generation.

> **Before you start**  
> Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](#concepts)).

## Concepts

Take **depth‑first search (DFS)**:
- It is a *specific* algorithm – one way to implement the more general “reachable” algorithm (BFS is another).
- **Binary search** is *not* specific – there is no broader “search” algorithm that binary search implements (at least in our system’s sense).

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

### 1. Update `enums.py` (in the `util/` folder)

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

- Add `<GENERAL_NAME>` to `GeneralAlgorithm` if it does not already exist:
  ```python
  class GeneralAlgorithm(Enum):
      # ...
      REACHABLE = auto()
  ```

- Add the mapping from specific → general in `SPECIFIC_ALG_TO_GENERAL`:
  ```python
  SPECIFIC_ALG_TO_GENERAL = {
      # ...
      SpecificAlgorithm.DEPTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  }
  ```

<u>**If `<GENERAL_NAME>` already existed**, skip to [step four](#4-write-solution-files-optional-but-recommended)</u>. Otherwise, continue to step two.

### 2. Create the general algorithm folder (if the general algorithm is new)

Inside the `problems/` directory, create a folder named `<general_name>` (e.g., `problems/reachable/`).  
Inside it, create an `info.json` file. See [Info File Format](DEVELOPER.md#info-files-infojson) for the required structure.

### 3. Generate tests (if the general algorithm is new)

- Go to `test_generation/problems/` and create a Python file named `<general_name>.py` (e.g., `reachable.py`).
- Define a class named `<GeneralName>Generator` (PascalCase) that extends `BaseGenerator` (imported from `base_generator`).
- Override all `@abstractmethod` methods. Do **not** override any `@final` methods.
- Use helper functions from `command_util` and write custom helpers as needed.

The program will automatically use this generator to create exhaustive test cases. Because these tests will be used to validate every implementation of the algorithm, **ensure the tests are as thorough as possible** (include edge cases, random inputs, and property‑based tests where applicable).

### 4. Write solution files
This step is optional but recommended.

Once the algorithm is fully integrated, you can add a solution for the algorithm in any supported language. Follow the instructions in [Writing an Algorithm Solution File](DEVELOPER.md#writing-an-algorithm-solution-file).

When you are done adding solutions, run the app tests to verify correctness.

### 5. Update documentation

As the last step, update all documentation to reflect that the new algorithm was added.