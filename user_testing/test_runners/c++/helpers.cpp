#include "helpers.hpp"

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