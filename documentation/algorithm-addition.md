# Adding an Algorithm

This guide explains how to add support for a new algorithm to the system. After completing these steps, users will be able to practice the algorithm in all supported languages.

> **Before you start**  
> Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](#concepts)).

## Concepts

Take **depth‑first search (DFS)**:
- It is a *specific* algorithm – one way to implement the more general “reachable” algorithm. BFS is another. Notice how DFS and BFS have the same **input-output behavior** and one is not clearly better than the other.
- **Binary search** is *not* specific. It is indisputably the best way to search arbitrary sorted data. It is not part of a more general "search" algorithm with something like linear search, since the input-output behavior is not the same *unless* the data is sorted, in which case it is **always better** to use binary search.

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

>**If `<GENERAL_NAME>` already existed**, skip to [step four](#4-add-solutions-for-the-new-algorithm). Otherwise, continue to step two.

### 2. Create the General Algorithm Folder (if the General Algorithm is New)

Inside the `problems/` directory, create a folder named `<general_name>` (e.g., `problems/reachable/`).  
Inside it, create an `info.json` file. See [Info File](DEVELOPER.md#info-files-infojson) for the required structure.

Do **not** create a `test.json` file. The next step will set up the ability to generate it, but the automatic generation will fail if the file already exists.

### 3. Generate Tests (if the General Algorithm is New)

- Go to `test_generation/problems/` and create a Python file named `<general_name>.py` (e.g., `reachable.py`).
- Define a class named `<GeneralName>Generator` (PascalCase, e.g. ReachableGenerator) that extends `BaseGenerator` (imported from `base_generator`).
- Override all `@abstractmethod` methods. Do **not** override any `@final` methods.
- Use helper functions from `command_util` and write custom helpers as needed.

>**Tip**: It may be helpful to look at an already existing test-generator for a concrete example of what to implement.

The program will automatically use this generator to create exhaustive test cases. Because these tests will be used to validate every implementation of the algorithm, ensure the tests are **as thorough as possible** (include edge cases, random inputs, and property‑based tests where applicable).

### 4. Add Solutions for the New Algorithm
This step is *optional* but **recommended**.

At this point you may add solutions for the algorithm in any of the supported languages. Follow the instructions in [Writing an Algorithm Solution File](DEVELOPER.md#writing-an-algorithm-solution-file).

When you are done, run the app tests to verify correctness.

### 5. Update Documentation

As the last step, update all documentation (the `README` and files in the `documentation/` directory) to reflect that the new algorithm was added.
