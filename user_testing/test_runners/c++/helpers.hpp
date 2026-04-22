#include <iostream>
#include <unordered_set>
#include <fstream>
#include "json.hpp"

using json = nlohmann::json;
using
  std::cerr, 
  std::string,
  std::vector,
  std::unordered_map,
  std::unordered_set;


// compilation: g++ -std=c++11 main.cpp -o my_program

enum class ParseType {
  INT,
  LONG,
  BOOLEAN,
  FLOAT,
  STRING,
  ARRAY,
  LIST,
  UNORDERED_LIST,
};

vector<string> PARSE_TYPE_LIST = {
  "int", 
  "long", 
  "boolean", 
  "float", 
  "string", 
  "array",
  "list",
  "unordered_list",
};

void usage(int argc, char** argv);
void validateParseTypeEnumList(vector<string> parseTypesString);
void printErr(string msg) {
  cerr << msg;
  std::exit(1);
};
json get_json_from_path(string path);
struct AgnosticComparator {
  bool operator()(const json& a, const json& b) const;
};
json standardize_output(json val, const json& def);

