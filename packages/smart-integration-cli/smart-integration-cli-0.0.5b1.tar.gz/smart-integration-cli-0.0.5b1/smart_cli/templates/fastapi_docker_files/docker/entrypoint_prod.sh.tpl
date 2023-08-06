#!/bin/bash

echo "Running command '$*'"
exec su ${PYTHON_RUN_USER} -p -s /bin/bash -c "$*"