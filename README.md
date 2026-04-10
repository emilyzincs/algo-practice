# Algorithm Practice
A strong understanding of fundamental algorithms is paramount, no matter the language. This project is built to enable users to exercise these algorithms with consistent, automated testing across languages.

# Installing the project
Start by cloning the repository. Using the terminal, navigate to the directory that you want to contain the project, then enter
```
git clone https://github.com/emilyzincs/algo-practice.git
```
The directory will then contain a folder named algo-practice. Enter it with ```cd algo-practice``` and install the required dependencies. <-- TODO DEPENDECIES

# Running the project
Navigate to the root of the algo-practice directory and enter

```python app.py```, or ```python app.py <language>``` to practice a specific language.  

Currently, the project operates through a command-line interface with three menus:

| Menu     | Description                                              |
|----------|----------------------------------------------------------|
| main     | Where the program starts.                                |
| practice | For algorithm practice.                                  |
| settings | For settings adjustment.                                 |

**Main loop**
- Entering an algorithm ```<name>``` or  ```<ID>``` at the main menu begins practice for that algorithm, with a path to the practice file given in the terminal (openable via cmd/ctrl+click in most editors). See IMPLEMENTATION REQUIREMENTS <--- TODO  to see the specific form an implementation must match.
- Entering ```done``` then runs tests for the current implementation, which returns to the main menu and prints the time spent if all tests pass.
- Entering ```quit``` from any menu at any time gracefully exits the program.  

**In general** 

Each menu consists of a few, manageable commands, with functional descriptions given by entering ```help```.
