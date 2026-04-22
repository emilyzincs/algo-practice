# Algorithm Practice
A strong understanding of fundamental algorithms is paramount, no matter the language. This project is built to enable users to exercise these algorithms with consistent, automated testing across languages.

## Installing the Project
Start by cloning the repository: 

Using your terminal, navigate to the directory that you want to contain the project, then enter
```
git clone https://github.com/emilyzincs/algo-practice.git
```
The directory will then contain the algo-practice folder.

Before running the project, all that remains is checking that you use the [required language versions](#supported-languages) for Python and the languages you practice.

## Running the Project
Navigate to the root of the algo-practice directory and enter

```python app.py``` to practice in the default language (Python if not configured), or  
```python app.py <language>``` to practice a specific language.  

Currently, the project operates through a command-line interface with three menus:

| Menu     | Description                                              |
|----------|----------------------------------------------------------|
| main     | Where the program starts.                                |
| practice | For algorithm practice.                                  |
| settings | For settings adjustment.                                 |

**Main Loop**
- Entering an algorithm ```<name>``` or  ```<ID>``` in the main menu begins practice for that algorithm, with a path to the practice file printed to the terminal (openable via cmd/ctrl+click in most editors). See [implementation requirements](/documentation/user-implementation.md) for the specific form an implementation must match.
- Entering ```done``` then runs tests for the current implementation, which returns to the main menu and prints the time spent if all tests pass.
- Entering ```quit``` from any menu at any time gracefully exits the program.  

**In General** 

Each menu consists of a few, manageable commands, with functional descriptions given by ```help```.

## Supported Languages
- Python 3.12.1+
- Java 17+
- C++ 17+

## Suppported Algorithms

### Arrays
* **Search:** Binary Search
* **Sort:** Merge Sort, Quick Sort, Heap Sort, Radix Sort, Bucket Sort
* **Subarray:** Kadane

---

### Graphs
* **Reachable:** Breadth First Search (BFS), Depth First Search (DFS)
* **Shortest Path:** Dijkstra, Bellman-Ford, Floyd-Warshall
* **Minimum Spanning Tree:** Kruskal, Prim
* **Topological Sort:** Kahn
* **Max Flow:** Ford-Fulkerson
* **Connected Components:** Tarjan

---

### Strings
* **Pattern Matching:** Knuth-Morris-Pratt (KMP)
