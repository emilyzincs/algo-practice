if [ "$1" == "python" ]; then 
  python -m unittest tests.practice_run_tests.python.test_python_run_test
elif [ "$1" == "java" ]; then
  python -m unittest tests.practice_run_tests.java.test_java_run_test
fi