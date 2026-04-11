TODO update with links
# Sections
- Adding an Algorithm
- Adding a Language
- Added a Required Class
- Running App Tests

## Adding an Algorithm
Let ```<alias>``` represent an alias of the algorithm's name in lowercase and wih spaces for different words. Note the algorithm's name itself (in this format) is always an alias. So, for example, ```dfs``` and ```depth first search``` are both aliases of the algorithm depth first search.

Let ```<specific_name>``` be the algorithm's name but snake-case. (E.g. binary_search).

Say that the algorithm is 'specific' if is just one way to implement of a more general algorithm that is also well-known. For example, depth first search is specific, since it and breadth first search both implement the reachable algorithm. On the other hand, binary search is not specific.

Let ```<general_name>``` be the snake-case version of the name of the general algorithm that the specific algorithm refers to, or ```<specific_name>``` if there is no such general algorithm. (E.g. reachable for depth first search, binary_search for binary search).

Finally, let capitalizing between the brackets indicate all caps. (E.g. ```<SPECIFIC_NAME>``` would be BINARY_SEARCH for binary search). 

Add the algorithm by continuing as follows.

First, in enums.py (found in the util folder):
- Update the ```SpecificAlgorithm``` enum by adding ```<SPECIFIC_NAME>``` as an entry.
- Update the ```INPUT_ALG_TO_SPECIFIC``` dictionary by adding the item ```("<alias>": SpecificAlgorithm.<SPECIFIC_NAME>)``` for each alias of the algorithm.
- Update the ```GeneralAlgorithm``` alias by adding ```<GENERAL_NAME>``` as an entry, if it does not already exist.
- Update the ```SPECIFIC_ALG_TO_GENERAL dictionary``` by adding the item ```(SpecificAlgorithm.<SPECIFIC_NAME>, GeneralAlgorithm.<GENERAL_NAME>)```.

If ```<GENERAL_NAME>``` was already an entry in ```GeneralAlgorithm```, you are done. Otherwise, continue.

Go into the problems directory and create a folder named ```<general_name>```. Enter that folder and create a file named ```info.json```, with the format as specified below.

### Format of info.json
A JSON dictionary with keys
- "unique_answer": A boolean value representing whether the algorithm has exactly one solution for each problem instance. 
- "parameter_names": An array of strings holding natural names for the parameters (in order) that make it clear what the parameters represents if you are familiar with the algorithm. (E.g. for binary search, this might be ["nums", "target"]).
- "input_types": An array of [JSON type representations](#format-of-type-representation) of the input parameter types in order.
- "expected_type": A [JSON type representation](#format-of-type-representation) of the expected return type.

### JSON Type Representations
This project uses JSON to represent types in a way that is agnostic to language. Each such representation ```<T>``` is a dictionary with a "type" key. The possible representations are layed out below.

- Primitive case: ```{ "type": <primitive> }``` where ```<primitive>``` is one of ```"int", "long", "float", "boolean", "string"```.
- Collection case: ```{ "type": <collection>, "items": <T> }``` where ```<collection>``` is one of ```"array", "list", "immutable_list", "set"```.
- Map case: ```{ "type": "map", "keys": <T>, "values": <T> }```
- Required Class case: ```{ "type": <required_class>, "val": <T> }``` where ```<required_class>``` is one of ```"ListNode", "TreeNode"```.

Note the potential values of a "type" key correspond exactly to the members of the ```ParseType``` enum in enums.py, enabling safe, exhaustive handling. 

### Generating Tests
Once 




### ParseTypes to JSON 




### Writing solution

