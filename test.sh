export TEST_NUMBER=$2
cmd="python -m unittest tests.practice_run_tests."$1".test_"$1"_run_test"
eval $cmd