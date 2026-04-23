#include "helpers.hpp"
using std::string, std::cerr;
using json = nlohmann::json;


void usage(int argc, char** argv) {
  string usageMsg = (
    string("Usage: ./runner.exe") + 
    " <debug>, where <debug> is True or False." +
    " <infoFilePath>.json" +
    " <testFilePath>.json" + 
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
  cerr << msg << std::endl;
  std::exit(1);
}


json getJsonFromPath(string path) {
  std::ifstream file(path);
  if (!file.is_open()) {
    printErr("Could not open " + path + ".");
  }
  json data;
  file >> data;
  return data;
}


bool AgnosticComparator::operator()(const json& a, const json& b) const {
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


json standardizeOutput(json val, const json& def) {
  std::string type_str = def["type"];
  
  if (type_str == "list" || type_str == "array" || type_str == "unordered_list") {
    json standardized = json::array();
    for (auto& item : val) {
      standardized.push_back(standardizeOutput(item, def["items"]));
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


bool validateOutput(json actual, json expected, bool unique, int test_num) {
  if (unique) {
    if (actual == expected) {
      return true;
    } else{
      cerr << "Failed test " << test_num+1 << ". Expected " << 
            expected << ", but was " << actual << "." << std::endl;
      return false;
    }
  } else {
    if (!expected.is_array()) {
      cerr << "Error: 'unique' is false but multiple answers are not expected." << std::endl;
      return false;
    }
    bool matched = false;
    for (const auto& candidate : expected) {
      if (actual == candidate) {
        matched = true;
        break;
      }
    }
    if (!matched) {
      cerr << "Failed test " << test_num+1 << ". Expected one of " << 
          expected << ", but was " << actual << "." << std::endl;
      return false;
    }
  }
  return true;
}
