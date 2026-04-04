export PYTHONPATH="${PYTHONPATH}:$(pwd)"
cmd="python -m unittest tests.java.test_java_boilerplate"
eval "$cmd"