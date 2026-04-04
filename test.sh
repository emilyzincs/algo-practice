#!/bin/bash
set -e

snake="hello_world_example"
pascal=""
IFS='_' read -ra parts <<< "$snake"
for part in "${parts[@]}"; do
  first="${part:0:1}"
  first="${first^}"  # uppercase first letter
  pascal+="$first${part:1}"
done
echo "$pascal"  # HelloWorldExample

# export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# usage() {
#   cat <<EOF
# Usage: $0 <command> [options]



# Examples:
#   $0 all
#   $0 lang python
#   $0 test TestMath test_addition
#   $0 test TestSort test_quicksort quick
# EOF
#   exit 1
# }

# case "$1" in
#   all)
#     shift
#     echo "Running all tests..."
#     python -m unittest tests.abstract_test_run_tests.AbstractTestRunTests.test_all
#     python -m unittest tests.abstract_test_boilerplate.AbstractTestBoilerplate.test_all
#     ;;
#   lang)
#     shift
#     if [ $# -ne 1 ]; then
#       echo "Error: 'lang' requires exactly one argument (language name)"
#       usage
#     fi
#     LANG="$1"
#     echo "Running language tests for: $LANG"
#     python -m unittest "tests.${LANG}.test_${LANG}_run_test"
#     python -m unittest "tests.${LANG}.test_${LANG}_boilerplate"
#     ;;
#   test)
#     shift
#     if [ $# -lt 2 ]; then
#       echo "Error: 'test' requires at least class and testname"
#       usage
#     fi
#     CLASS="$1"
#     TESTNAME="$2"
#     shift 2
#     if [ $# -ge 1 ]; then
#       SPECIFIER="$1"
#       echo "Running with specifier: $SPECIFIER"
#       export TEST_SPECIFIER="$SPECIFIER"
#     fi
#     # Adjust the path to match your actual test hierarchy
#     python -m unittest "tests.${CLASS}.${TESTNAME}"
#     ;;
#   *)
#     usage
#     ;;
# esac