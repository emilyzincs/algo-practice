#ifndef HELPERS_HPP
#define HELPERS_HPP

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

inline vector<string> PARSE_TYPE_LIST = {
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
void printErr(string msg);
json getJsonFromPath(string path);
struct AgnosticComparator {
  bool operator()(const json& a, const json& b) const;
};
json standardizeOutput(json val, const json& def);
bool validateOutput(json actual, json expected, bool unique, int test_num);

#endif  // HELPERS_HPP