# Algorithm Practice
A strong understanding of fundamental algorithms is paramount, no matter the language. This project is built to enable users to exercise these algorithms with consistent, automated testing across languages.

## Installing the Project
Start by cloning the repository: 

Using your terminal, navigate to the directory that you want to contain the project, then enter
```
git clone https://github.com/emilyzincs/algo-practice.git
```
The directory will then contain the algo-practice folder.

Before running the project, all that remains is checking that you use the [required language versions](#supported-languages) for python and the languages you practice.

## Running the Project
Navigate to the root of the algo-practice directory and enter

```python app.py```, or ```python app.py <language>``` to practice a specific language.  

Currently, the project operates through a command-line interface with three menus:

| Menu     | Description                                              |
|----------|----------------------------------------------------------|
| main     | Where the program starts.                                |
| practice | For algorithm practice.                                  |
| settings | For settings adjustment.                                 |

**Main Loop**
- Entering an algorithm ```<name>``` or  ```<ID>``` at the main menu begins practice for that algorithm, with a path to the practice file printed to the terminal (openable via cmd/ctrl+click in most editors). See [implementation requirements](/documentation/user-implementation.md) to see the specific form an implementation must match.
- Entering ```done``` then runs tests for the current implementation, which returns to the main menu and prints the time spent if all tests pass.
- Entering ```quit``` from any menu at any time gracefully exits the program.  

**In General** 

Each menu consists of a few, manageable commands, with functional descriptions given by entering ```help```.

## Supported Languages
- Python 3.12.1+
- Java 17+

## Suppported Algorithms
- Binary Search
- Breadth First Search
- Depth First Search
- Merge Sort
