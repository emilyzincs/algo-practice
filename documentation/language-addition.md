# Adding a Language

This guide explains how to add support for a new programming language to the system. After completing these steps, users will be able to practice all algorithms that have already been implemented, in that language.

Let `<language>` be the name of the language in lowercase (e.g., `java`).  
Let `<Language>` be the same name capitalized (e.g., `Java`).

## Step‑by‑step instructions


### 1. Create a Test Runner

The first and most important step in adding a new language is to create a test-runner for it. Details about test-runners can be found [here](#TODO).


### 2. Update `run_tests` Function in `user_testing/test.py`

The main test orchestration function needs to know how to invoke your new test runner. Locate the `run_tests` function (or equivalent) and add a branch for `<language>` that constructs the appropriate command line.

Example for Python:
```python
case Language.PYTHON:
    cmd = ["python", test_runner_file, practice_file, 
           info_file, test_file, fp.PROJECT_ROOT, debug]
```

Add a similar block for your language. You may need to factor this out into its own function, especially if there are any files (including the runner itself) that may need to be compiled before running the command.


### 3. Update `boilerplate/<language>`

Create a file named `<language>.py` inside the `boilerplate/language` directory. In it, define a class named `<Language>Bp` that extends `BpInterface` from `boilerplate/interface.py`. It must implement all abstract methods of `BpInterface`.

This class is responsible for generating the initial boilerplate code when a user starts practicing an algorithm in the new language (if they have the `prepopulate_boilerplate` setting enabled, which is true by default).

As an example, the Java boilerplate generated for the `reachable` algorithms (`BFS` and `DFS`) is
```
package practice;

import java.util.List;
import java.util.Set;

public class Solution {
  public static Set<Integer> solve(List<List<Integer>> graph, int root) {
    
  }
}

```



See existing implementations (e.g., `boilerplate/language/python.py`) for guidance.

### 4. Update App Tests

The app tests ensure that boilerplate generation and test-runners work correctly. In the `app_tests/` directory, create a folder named `<language>`. Inside it, create two subdirectories:

- `boilerplate_files/` – Stores the expected boilerplate for various algorithms.
- `solution_files/` – Stores the expected solution file contents.

Then update the app test runner to include your new language. The exact test cases can be copied and adapted from an existing language folder.

>Note: The new tests will not run until after step five.


### 5. Update `match` Statements in the Codebase

First, add the language entry to the `Language` enum in `enums.py`:

```python
class Language(Enum):
    # ...
    <LANGUAGE> = (".<extension>", "<comment_symbol>")
```

Replace `.<extension>` with the file extension (e.g., `.py` for Python) and `<comment_symbol>` with the line‑level comment symbol (e.g., `//` for Java).

After adding the enum member, **use mypy (or your IDE’s type checker)** to find all `match` (or `switch`) statements that switch on `Language`. The type checker will complain about non‑exhaustive patterns. Update each one to handle your new language.

#### Verification
TODO

### 6. Add Algorithm Solutions for the New Language

After the language is fully integrated, you are encouraged to add solution files for existing algorithms. For each algorithm, create a solution file in the appropriate path:

Once the language is registered and tests exist, you can add a solution in the language for any supported algorithm. Follow the instructions in [Writing an Algorithm Solution File](DEVELOPER.md#writing-an-algorithm-solution-file).

After adding at least one solution, run the app tests to verify correctness.