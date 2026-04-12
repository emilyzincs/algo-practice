# Adding a Language

This guide explains how to add support for a new programming language to the system. After completing these steps, users will be able to practice all algorithms that have already been implemented, in that language.

Let `<language>` be the name of the language in lowercase (e.g., `java`).  
Let `<Language>` be the same name capitalized (e.g., `Java`).

## Step‑by‑step instructions

### 1. Create a Test Runner

A test runner is an executable that runs algorithm tests for the language. It must be placed in `test_runners/<language>/` (create the directory if it doesn’t exist). The runner can be written in the target language itself or in a scripting language (e.g., Python) that invokes the target language’s toolchain.

The test runner must accept the following command‑line arguments:

```
<runner> <test_file> <info_file> <solution_file>
```

- `<test_file>`: path to `test.json` (an array of test cases).
- `<info_file>`: path to `info.json` (describes parameter types).
- `<solution_file>`: path to the user’s implementation file (or a directory containing it).

**Required behaviour:**

1. Parse `<test_file>` and `<info_file>`.
2. For each test case, convert the JSON inputs and expected output into concrete values of the target language according to the [language‑agnostic types](DEVELOPER.md#languageagnostic-types).
3. Call the function defined in `<solution_file>` with those inputs. The function signature must match the parameter names and types from `<info_file>`.
4. Compare the actual result to the expected value.
5. If any test fails, print an error message (including which test failed) and exit with a non‑zero status code. If all pass, print a success message and exit with 0.

> **Tip:** Look at existing test runners (e.g., `test_runners/python/runner.py`) for a concrete example.

### 2. Update `run_tests` Function in `user_testing/test.py`

The main test orchestration function needs to know how to invoke your new test runner. Locate the `run_tests` function (or equivalent) and add a branch for `<language>` that constructs the appropriate command line.

Example for Python:
```python
case Language.PYTHON:
    cmd = ["python", test_runner_file, practice_file, 
           info_file, test_file, fp.PROJECT_ROOT, debug]
```

Add a similar block for your language.

### 3. Update `boilerplate/<language>`

Create a file named `<language>.py` inside the `boilerplate/language` directory. In it, define a class named `<Language>Bp` that extends `BpInterface` from `boilerplate/interface.py`.

This class is responsible for generating the initial boilerplate code when a user starts practicing an algorithm. It must implement all abstract methods of `BpInterface`.

See existing implementations (e.g., `boilerplate/language/python.py`) for guidance.

### 4. Update App Tests

The app tests ensure that boilerplate generation and solution loading work correctly. In the `app_tests/` directory, create a folder named `<language>`. Inside it, create two subdirectories:

- `boilerplate_files/` – store expected boilerplate outputs for various algorithms.
- `solution_files/` – store expected solution file contents.

Then update the app test runner to include your new language. The exact test cases can be copied and adapted from an existing language folder.

### 5. Update `match` Statements in the Codebase

First, add the language entry to the `Language` enum in `enums.py`:

```python
class Language(Enum):
    # ...
    <LANGUAGE> = (".<extension>", "<comment_symbol>")
```

Replace `.<extension>` with the file extension (e.g., `.py` for Python) and `<comment_symbol>` with the line‑level comment symbol (e.g., `//` for Java).

After adding the enum member, **use mypy (or your IDE’s type checker)** to find all `match` (or `switch`) statements that switch on `Language`. The type checker will complain about non‑exhaustive patterns. Update each one to handle your new language.

### 6. Add Algorithm Solutions for the New Language

After the language is fully integrated, you are encouraged to add solution files for existing algorithms. For each algorithm, create a solution file in the appropriate path:

- For specific algorithms: `problems/<general_name>/<specific_name>/solution.<extension>`
- For non‑specific algorithms: `problems/<specific_name>/solution.<extension>`

The content must be a correct implementation of the algorithm following the [implementation requirements](USER_IMPLEMENTATION.md#TODO). You can copy and adapt solutions from an already supported language.

> **Tip:** Start with a few core algorithms (e.g., binary search, depth‑first search) to validate the language integration before adding all solutions.

## Verification

Run the full test suite:

```bash
python run_tests.py --all-languages
```

All tests for your new language should pass. Also run the app tests:

```bash
python app_tests/run_app_tests.py
```

If everything succeeds, the new language is ready for users.