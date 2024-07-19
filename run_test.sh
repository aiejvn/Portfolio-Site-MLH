#!/bin/bash

# If there are spaces in the parent directory, quotation marks are needed
"$PWD"/python3-virtualenv/bin/python -m unittest discover -v tests/