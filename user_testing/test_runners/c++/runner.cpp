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
  HASHABLE_LIST,
  SET,
  HASHABLE_SET,
  MAP,
};

vector<string> PARSE_TYPE_LIST = {
  "int", 
  "long", 
  "boolean", 
  "float", 
  "string", 
  "array",
  "list",
  "hashable_list",
  "set",
  "hashable_set",
  "map",
};

void usage(int argc, char** argv);
void validateParseTypeEnumList(vector<string> parseTypesString);
void printErr(string msg) {
  cerr << msg;
  std::exit(1);
};
json get_json_from_path(string path);

int main(int argc, char** argv) {
  if (argc != 8 || ("True" != argv[4] && "False" != argv[4])) {
    usage(argc, argv);
  }
  bool debug = argv[4] == "True";
  string requiredClassName = argv[5];
  string requiredMethodName = argv[6];
  
  vector<string> parseTypesString = json::parse(argv[7]).get<vector<string>>();
  validateParseTypeEnumList(parseTypesString);

  string info_path = argv[2];
  json info = get_json_from_path(info_path);

  

  return 0;
}

void usage(int argc, char** argv) {
  string usageMsg = (
    std::string("Usage: java Runner") + 
    " <practiceFilePackage>" +
    " <infoFilePath>.json" +
    " <testFilePath>.json" + 
    " <debug>, where <debug> is True or False." +
    " <SolutionClassName>" + 
    " <SolutionMethodName>" +
    " <ParseTypes list string>"
  );
  string argsMsg = ("Given args: [");
  if (argc != 0) {
    argsMsg += argv[0];
    for (int i = 1; i < argc; i++) {
      argsMsg += ", ";
      argsMsg += argv[i];
    }
  }
  argsMsg += "]";
  printErr(usageMsg + argsMsg);
}

void validateParseTypeList(vector<string> parseTypesString) {
  if (parseTypesString != PARSE_TYPE_LIST) {
    printErr("Given ParseTypes enum entries do not match the expected.");
  }
}

json get_json_from_path(string path) {
  std::ifstream file(path);
  if (!file.is_open()) {
    printErr("Could not open " + path + ".");
  }
  json data;
  data << file;
  return data;
}