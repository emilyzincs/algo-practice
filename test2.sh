export PYTHONPATH="${PYTHONPATH}:$(pwd)"
cmd="python -m unittest tests.abstract_test_boilerplate"
eval "$cmd"