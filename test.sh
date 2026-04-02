if [ "$1" == "all" ]; then
  export TEST_SPECIFIER="ALL"
  cmd="python -m unittest tests.practice_run_tests.abstract_test_run_tests"
else
  export TEST_SPECIFIER=$2
  cmd="python -m unittest tests.practice_run_tests."$1".test_"$1"_run_test"
fi
eval "$cmd"