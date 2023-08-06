#!/bin/bash
export VERSION_JSON_PATH=$(pwd)/version.json
cd docs
sphinx-apidoc -o source ../swimbundle_utils -f
make text
make html
