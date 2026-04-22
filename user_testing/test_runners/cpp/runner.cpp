#include <iostream>
#include <unordered_set>
#include <fstream>
#include "json.hpp"
#include "helpers.hpp"

#include {PATH: "../../../problems/arrays/search/binary_search/solution.cpp"}

using json = nlohmann::json;
using
  std::cout,
  std::cerr, 
  std::string,
  std::vector,
  std::unordered_map,
  std::unordered_set;


int main(int argc, char** argv) {
  bool debug = argv[1] == "True";
  
  vector<string> parseTypesString = json::parse(argv[7]).get<vector<string>>();
  validateParseTypeEnumList(parseTypesString);

  string info_path = argv[2];
  string test_path = argv[3];
  json info = get_json_from_path(info_path);
  json tests = get_json_from_path(test_path);

  bool unique = info["unique"];
  json expected_type = info["expected_type"];

  for (int i = 0; i < tests.size(); i++) {
    auto& test = tests[i];
    // 1. Get the actual type returned by the user's function
    using ActualRetType = decltype({solution_class}::{method_name}({call_args}));
    using ExpectedRetType = {cpp_expected_type}; 
    static_assert(std::is_same_v<ActualRetType, ExpectedRetType>, 
                  "Return type mismatch! Your function signature does not match the problem definition.");
    
    {output_type} raw = {solution_class}::{method}({call_args});

    json actual = standardize_output(raw, expected_type);
    json expected = test["expected"];

    bool unique;
    if (!validate_output(actual, expected, unique, i)) {
      std::exit(1);
    }
  }
  cout << "All tests passed!";
  return 0;
}
