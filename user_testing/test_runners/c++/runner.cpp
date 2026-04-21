#include <iostream>
#include <unordered_set>
#include <fstream>
#include "json.hpp"
#include "helpers.hpp"

using json = nlohmann::json;
using
  std::cout,
  std::cerr, 
  std::string,
  std::vector,
  std::unordered_map,
  std::unordered_set;


// compilation: g++ -std=c++11 main.cpp -o my_program

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
  string test_path = argv[3];
  json info = get_json_from_path(info_path);
  json tests = get_json_from_path(test_path);

  for (int i = 0; i < tests.size(); i++) {
    auto& test = tests[i];
    // TODO FILL auto raw = {method}({args});

    {output_type} actual = standardize_output(raw, expected_type);
    {output_type} expected = {expected};

    if (actual != expected) {
      cerr << "Failed test " << i+1 << ". Expected " << 
            expected << ", but was " << actual;
    }
  }
  cout << "All tests passed!;
  return 0;
}
