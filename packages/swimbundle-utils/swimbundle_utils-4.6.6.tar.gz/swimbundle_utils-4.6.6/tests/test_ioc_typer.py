import sys
import os
from swimbundle_utils import ioc
import pytest
import json

ioct = ioc.IOCTyper()

with open('test_ioc_typer.json', 'rb') as f:
    data = json.load(f)

inputs = []
for type, values in data.items():
    for value in values:
        inputs.append((type, value))


@pytest.mark.parametrize('expected_type,value', inputs)
def test_typer(expected_type, value):
    found_type = ioct.type_ioc(value)
    assert expected_type == found_type
