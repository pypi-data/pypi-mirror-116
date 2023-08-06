from swimbundle_utils import ioc
import pytest
from deepdiff import DeepDiff
import json
with open('test_ioc_parser.json', 'rb') as f:
    tests = json.load(f)

parser = ioc.IOCParser()


@pytest.mark.parametrize('input_vars,expected_output', [(x['inputs'], x['expected_output']) for x in tests])
def test_parser(input_vars, expected_output):
    found_iocs = parser.parse_iocs(**input_vars)
    assert str(DeepDiff(expected_output, found_iocs, ignore_order=True)) == '{}'
