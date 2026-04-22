#include "helpers.hpp"
using std::string, std::cerr;
using json = nlohmann::json;


void usage(int argc, char** argv) {
  string usageMsg = (
    string("Usage: java Runner") + 
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


void validateParseTypeEnumList(vector<string> parseTypesString) {
  if (parseTypesString != PARSE_TYPE_LIST) {
    printErr("Given ParseTypes enum entries do not match the expected.");
  }
}


void printErr(string msg) {
  cerr << msg;
  std::exit(1);
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

struct AgnosticComparator {
  bool operator()(const json& a, const json& b) const {
    if (a.type() != b.type()) printErr("Types in a collection are no the same.");
    if (a.is_array()) {
      if (a.size() != b.size()) return a.size() < b.size();
      for (size_t i = 0; i < a.size(); ++i) {
        if (a[i] != b[i]) return operator()(a[i], b[i]);
      }
      return false;
    }
    return a < b;
  }
};


json standardize_output(json val, const json& def) {
  std::string type_str = def["type"];
  
  if (type_str == "list" || type_str == "array" || type_str == "unordered_list") {
    json standardized = json::array();
    for (auto& item : val) {
      standardized.push_back(standardize_output(item, def["items"]));
    }
    if (type_str == "unordered_list") {
      std::sort(standardized.begin(), standardized.end(), AgnosticComparator());
    }
    return standardized;
  }
  
  if (type_str == "float" && val.is_number()) {
    double d = val.get<double>();
    return (d == 0.0) ? 0.0 : d;
  }
  
  return val;
}