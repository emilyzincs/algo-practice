export PYTHONPATH="${PYTHONPATH}:$(pwd)"
cmd="python -m unittest tests.python.test_python_boilerplate"
eval "$cmd"