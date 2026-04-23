#include <iostream>
#include <utility>
#include <unordered_set>
#include <fstream>
#include "json.hpp"
#include "helpers.hpp"

#include "../../../problems/graphs/topological_sort/kahn/solution.cpp"

using json = nlohmann::json;
using
  std::cout,
  std::cerr, 
  std::string,
  std::vector,
  std::unordered_map,
  std::unordered_set;


int main(int argc, char** argv) {{
  bool debug = string(argv[1]) == "True";
  
  vector<string> parseTypesString = json::parse(argv[4]).get<vector<string>>();
  validateParseTypeEnumList(parseTypesString);

  string info_path = argv[2];
  string test_path = argv[3];
  json info = getJsonFromPath(info_path);
  json tests = getJsonFromPath(test_path);

  bool unique = info["unique_answer"];
  json expected_type = info["expected_type"];

  for (int i = 0; i < tests.size(); i++) {{
    auto& test = tests[i];
    // 1. Get the actual type returned by the user's function
    using ActualRetType = decltype(std::declval<Solution>().solve(std::declval<vector<vector<int>>&>()));
    using ExpectedRetType = vector<int>; 
    static_assert(std::is_same_v<ActualRetType, ExpectedRetType>, 
                  "Return type mismatch! Your function signature does not match the problem definition.");
    
    Solution solution;    auto arg0 = test["inputs"][0].get<vector<vector<int>>>();
    vector<int> raw = solution.solve(arg0);

    json actual = standardizeOutput(raw, expected_type);
    json expected = test["expected"];

    if (!validateOutput(actual, expected, unique, i)) {{
      std::exit(1);
    }}
  }}
  return 0;
}}
