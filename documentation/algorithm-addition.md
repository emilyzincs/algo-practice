# Adding an Algorithm

This guide explains how to add support for a new algorithm to the system. After completing these steps, users will be able to practice the algorithm in all supported languages.

> **Before you start**  
> Make sure you understand the difference between *specific* and *general* algorithms (see [Concepts](#concepts)).

## Concepts

Take **Dijkstra's Algorithm**:
- It is a **specific** algorithm. How it finds shortest paths is **fully specified**. Generally, one might say it is a shortest path algorithm.
- Shortest Path is a **general** algorithm. It does not specify **how** the path(s) should be found. The input-output space is also not fully specified. For example, one could say that Bellman-Ford is a specific implementation of Shortest Path, but Bellman-Ford and Dijkstra expect different inputs (Dijkstra required nonnegative weights).
- Graph is a **category** of unrelated general algorithms. E.g., Shortest Path and Topological Sort are both in the Graph category of algorithms. For our purposes, category will be the main data structure or type used (E.g., Array, Graph, String).

As another example, consider **Depth-First Search** (DFS):
- It is a specific instance of the general, Reachable algorithm, in the Graph category.
- It has multiple aliases that refer to it.

We use the following naming conventions, with Depth-First Search as the example:

| Concept | Format | Example (DFS) |
|---------|--------|----------------|
| Alias | lowercase, spaces between words | `"dfs"`, `"depth first search"` |
| Specific name | snake_case | `depth_first_search` |
| General name | snake_case | `reachable` |
| Category | snake_case, plural | `graphs` |

> The algorithm’s own name (in lowercase with spaces) is always an alias. So `"depth first search"` is an alias of itself.

## Step‑by‑step instructions

We’ll use **depth‑first search** as the running example.  
Assume its specific name is `depth_first_search` and its general name is `reachable`.

### 1. Update `enums.py` (in the `util/` folder)

- Add `<CATEGORY>` (all caps, snake case, plural) to `AlgorithmCategory`:
  ```python
  class AlgorithmCategory(Enum):
      # ...
      GRAPHS = auto()
  ```


- Add `<GENERAL_NAME>` to `GeneralAlgorithm` if it does not already exist, including the corresponding `AlgorithmCategory` (from the previous step) in the value:
  ```python
  class GeneralAlgorithm(Enum):
      # ...
      REACHABLE = (AlgorithmCategory.GRAPHS, auto())
  ```


- Add `<SPECIFIC_NAME>` (all caps, snake case) to `SpecificAlgorithm`, including the following (GeneralType, InfoDir, TestDir, GeneratorFileName, Aliases) in the value:
  - **GeneralType**: The corresponding `GeneralAlgorithm` (from the previous step). E.g. `GeneralAlgorithm.REACHABLE`.
  - **InfoDir**: The `DirectoryType` representing the directory that holds the `info.json` file. For DFS this is `DirectoryType.GENERAL` since the information regarding expected inputs and outputs is uniform across all specific implementations of the general Reachable algorithm.
  - **TestDir**: The `DirectoryType` representing the directory that holds the `test.json` file. For DFS this is `DirectoryType.GENERAL` since the expected output given an input is uniform across all specific implementations of the general Reachable algorithm.
  - **GeneratorFileName**: The name of the file used to generate tests for the algorithm. This is `None` if the name mathes `<specific_name>`.
  - **Aliases**: The list of aliases for the algorithm. E.g. `[dfs, depth_first_search]`


  ```python
  class SpecificAlgorithm(Enum):
      # ...
      DEPTH_FIRST_SEARCH = (
        GeneralAlgorithm.REACHABLE, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, "general", ["dfs", "depth first search"]
      )
  ```

### 2. Create the Info File

The path to create the info file depends on `InfoDir` from the previous step. 
- If you put `DirectoryType.SPECIFIC`, the path is `problems/<category>/<general_name>/<specific_name>/info.json`. 
- If you put `DirectoryType.GENERAL`, the path is `problems/<category>/<general_name/info.json`.

Create any necessary files/directories in the path. If the `info.json` file already existed, you may continue to the next step

Otherwise, write the `info.json` file. See [Info File](DEVELOPER.md#info-files-infojson) for the required structure.

### 3. Create the Test Generator

The path to create the test generator file depends on `GeneratorFileName` from the first step. It is `user_testing/test_generation/problems/<category>/<general_name>/<GeneratorFileName>.py`.

Create any necessary files/directories in the path. If the file already existed, you may continue to the next step.

Otherwise, write the file by doing the following.
- Define a class named `Generator` that extends `BaseGenerator` (imported from `base_generator`).
- Override all `@abstractmethod` methods. Do **not** override any `@final` methods.
- Use helper functions from the test generation `util` directory and write custom helpers as needed.

>**Note**: Implementing an oracle may be difficult enough that you need to [write a solution](DEVELOPER.md#writing-an-algorithm-solution-file) first, then use that as the oracle. This is fine, but the generated tests will then provide **no** validation for that solution. If you go this route, it is recommended to start with some **hand-written tests** for basic validation, and to *very* careful in reviewing your code. Make sure to delete the `test.json` file after you are done, so that the generator can do its job. If time complexity is the issue (i.e., you have to use your own solution otherwise the tests would take too long) it is recommended to use a brute-force oracle for small inputs, with an input size threshold as reasonably high as possible to provide as much validation as possible.

>**Tip**: It may be helpful to look at an already existing test-generator for a concrete example of what to implement.

The program will automatically use this generator to create exhaustive test cases. Because these tests will be used to validate every implementation of the algorithm, ensure the tests are **as thorough as possible** (include edge cases, random inputs, and property‑based tests where applicable).

### 4. Add Solutions for the New Algorithm
This step is *optional* but **recommended**.

At this point you may add solutions for the algorithm in any of the supported languages. Follow the instructions in [Writing an Algorithm Solution File](DEVELOPER.md#writing-an-algorithm-solution-file).

When you are done, run the app tests to verify correctness.

### 5. Update Documentation

As the last step, update all documentation (the `README` and files in the `documentation/` directory) to reflect that the new algorithm was added.
