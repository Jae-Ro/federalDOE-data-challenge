#!/bin/bash
pip install -e .
# run test suite -- can remove if slowing things down
pytest -v tests/
# run solution
python src/codetest/main.py $@