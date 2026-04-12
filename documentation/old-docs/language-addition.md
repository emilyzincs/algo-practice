# Adding a Language
Let `<language>` be the name of the language (lowercase).

## Concepts

## Step‑by‑step instructions

### 1. Create a Test Runner

### 2. Update `run_tests` Function in `user_testing/test.py`

### 3. Update `boilerplate/language`
Create a file in the directory named `<language>.py` holding a class named `<Langugage>Bp` that extends the `BpInterface` class in `boileplate/interface`. (`<Language>` means `<language>` but capitalized).

### 4. Update App Tests
In the `app_tests` directory, create a folder named `<language>`. In it, create directories named `boilerplate_files` and `solution_files`. 

### 5. Update `match` Statements
In `enums.py`, add the appropriate entry to the `Language` enum. I.e., add the line 
```
<LANGUAGE> = (".<extension>", "<comment_symbol>")
```
where `.<extension>` and `<comment_symbol>` are the file extension and line-lebel comment symbol that correspond to `<language>`. 

Next, update the match statements throughout the project that switch on Language member to include handle the case for `<language>`. These are mostly miscellaneous, the challenging ones were the previous few steps.

This will be much easier with mypy, since after the previous step, it will raise the unhandled language in these match statements as a problem.


### 6. Add Algorithm Solutions