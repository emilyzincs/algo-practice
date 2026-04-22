#include <iostream>
#include <utility>
#include <unordered_set>
#include <fstream>
#include "json.hpp"
#include "helpers.hpp"

#include "../../../app_tests/language/cpp/solution_files/sol1.cpp"

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
    using ActualRetType = decltype(Solution::solve());
    using ExpectedRetType = int; 
    static_assert(std::is_same_v<ActualRetType, ExpectedRetType>, 
                  "Return type mismatch! Your function signature does not match the problem definition.");
    

    int raw = Solution::solve();

    json actual = standardizeOutput(raw, expected_type);
    json expected = test["expected"];

    if (!validateOutput(actual, expected, unique, i)) {{
      std::exit(1);
    }}
  }}
  return 0;
}}
