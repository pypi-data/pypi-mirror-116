import six
import pytest
from six import iteritems
import base64
import pendulum
from swimbundle_utils.helpers import asset_parser, check_input, InputChecker, create_test_conn, create_attachment
from swimbundle_utils.helpers import SwimlaneAttachments, QueryStringParser, ComparisonTimeval
from swimbundle_utils.validation import PositiveIntRange, NegativeIntRange, IntRange
from swimbundle_utils.exceptions import SwimlaneIntegrationException as swx
from swimbundle_utils.exceptions import SwimlaneException
from swimbundle_utils.rest import BasicRestEndpoint


class Auth(object):
    pass


a = Auth()
asset_parser_test_data = [
    # Format is {asset data}, {parser options}, {attributes to test equality in created class, sub attrs split by '.'}
    ({"host": "abc.com", "username": "bb", "password": "cc"}, {"auth": "basic"}, {"host": "abc.com", "session.auth": ("bb", "cc")}),  # Test basic auth
    ({"host": "abc.com"}, {}, {"host": "abc.com", "session.auth": None}),  # Test no auth
    ({"host": "abc.com", "client_id": "asdf"}, {"auth": a}, {"host": "abc.com", "session.auth": a}),  # Test class auth
    ({"client_id": "asdf"}, {}, {"host": None}),  # Test no host
    ({"host": "asdfasdf.com"}, {"host": "https://123.123.123.123"}, {"host": "https://123.123.123.123"})  # Test kwarg overwriting of 'host' key
]


def fail(exception_class, f, args, **kwargs):
    try:
        SwimlaneException.disable_tb_stream()  # Temp disable TB stream to clear up output of expected failures
        f(*args, **kwargs)
        raise ValueError("Didn't throw expected exception!")
    except Exception as e:
        if six.PY3:
            assert exception_class == type(e)
        else:
            assert e.__class__ == exception_class
    finally:
        SwimlaneException.reset_tb_stream()  # Make sure to turn it back on after


@pytest.mark.parametrize("data", asset_parser_test_data)
def test_asset_parser_helper(data):
    asset_data = data[0]
    parser_opts = data[1]
    result_data = data[2]

    class Context(object):
        asset = asset_data

    class T(BasicRestEndpoint):
        def __init__(self, context):
            super(T, self).__init__(**asset_parser(context.asset, **parser_opts))

    t = T(Context)
    for k, v in iteritems(result_data):  # Go through all keys
        attrs = k.split(".")
        obj = t
        for attr in attrs:  # Traverse attributes with dots, ie the string "session.auth" -> t.session.auth (object)
            obj = getattr(obj, attr)
        assert obj == v


input_checker_data = [
    # (test_id, (input_params, input, expected, should_fail))

    ("flags-optional-none", ({"flags": ["optional"]}, None, "asdf", False)),
    ("flags-optional-set", ({"flags": ["optional"]}, "asdf", "asdf", False)),
    ("int-range-pos-p", ({"options": {"type": "int"}}, 5, PositiveIntRange(), False)),
    ("int-range-pos-f", ({"options": {"type": "int"}}, -5, PositiveIntRange(), True)),
    ("int-range-pos-z-p", ({"options": {"type": "int"}}, 0, PositiveIntRange(include_zero=True), False)),
    ("int-range-pos-z-f", ({"options": {"type": "int"}}, 0, PositiveIntRange(include_zero=False), True)),
    ("int-range-neg-p", ({"options": {"type": "int"}}, -5, NegativeIntRange(), False)),
    ("int-range-neg-f", ({"options": {"type": "int"}}, 5, NegativeIntRange(), True)),
    ("int-range-neg-z-p", ({"options": {"type": "int"}}, 0, NegativeIntRange(include_zero=True), False)),
    ("int-range-neg-z-f", ({"options": {"type": "int"}}, 0, NegativeIntRange(include_zero=False), True)),
    ("int-range-cust-p", ({"options": {"type": "int"}}, 80, IntRange(-100, 100), False)),
    ("int-range-cust-n", ({"options": {"type": "int"}}, -80, IntRange(-100, 100), False)),
    ("int-pass", ({"options": {"type": "int"}}, 2, (1, 2, 3), False)),
    ("int-fail", ({"options": {"type": "int"}}, "a", (1, 2, 3), True)),
    ("ipv4-pass", ({"options": {"type": "ipv4"}}, "123.123.123.623", None, True)),
    ("ipv4-fail", ({"options": {"type": "ipv4"}}, "123.123.123.123", None, False)),
    ("bool-pass", ({"options": {"type": "bool"}}, True, [True, False], False)),
    ("bool-fail", ({"options": {"type": "bool"}}, 0, [True, False], True)),
    ("dt-pass", ({"options": {"type": "datetime"}}, "2019-09-03T15:17:49-06:00", "2019-09-03T15:17:49-06:00", False)),
    ("dt-fail", ({"options": {"type": "datetime"}}, "2019-10-03T15:17:49-06:00", "asdf", True)),
    ("url-pass", ({"options": {"type": "url"}}, "https://google.com", "https://google.com", False)),
    ("url-fail", ({"options": {"type": "url"}}, "google.com", "google.com", True)),
    ("domain-pass", ({"options": {"type": "domain"}}, "google.com", "google.com", False)),
    ("domain-fail", ({"options": {"type": "domain"}}, "/google.com", "google.com", True)),
    ("flags-lower", ({"flags": ["lower"]}, "ASDF", "asdf", False)),
    ("flags-caps", ({"flags": ["caps"]}, "asdf", "ASDF", False)),
    ("mapping-1", ({"mapping": {True: "enable",
                                False: "disable"}}, True, "enable", False)),
    ("mapping-2", ({"mapping": {True: "enable",
                                False: "disable"}}, False, "disable", False)),
    ("mapping-3", ({"mapping": {True: "enable",
                                False: "disable"}}, "enable", "enable", False)),
    ("mapping-4", ({"mapping": {True: "enable",
                                False: "disable"}}, "disable", "disable", False)),
]

input_checker_parsed = {
    "argvalues": [],
    "ids": []
}
for tid, val in input_checker_data:
    input_checker_parsed["argvalues"].append(val)
    input_checker_parsed["ids"].append(tid)


@pytest.mark.parametrize("use_helper", [False, True])
@pytest.mark.parametrize("data", **input_checker_parsed)
def test_input_checker(data, use_helper):
    input_params = data[0]
    in_val = data[1]
    ex_val = data[2]
    should_fail = data[3]

    if use_helper:
        run_func = check_input
    else:
        run_func = InputChecker().check

    if should_fail:
        fail(swx, run_func, [in_val, ex_val], **input_params)
    else:
        run_func(in_val, ex_val, **input_params)


@pytest.mark.parametrize("data", [
    # username, password, should_fail
    ("admin", "pw", False),
    ("admin", "invalid", True)
])
@pytest.mark.parametrize("auth_in_init", [True, False])
def test_testconn_base(data, auth_in_init):
    
    class BaseIntegration(object):
        def __init__(self, context):
            self.username = context.asset["username"]
            self.password = context.asset["password"]
            if auth_in_init:
                self.auth()
        
        def auth(self):
            if self.username != "admin" or self.password != "pw":
                raise Exception("This is an API exception!")
                
    if auth_in_init:
        SwMain = create_test_conn(BaseIntegration)
    else:
        SwMain = create_test_conn(BaseIntegration, "auth")
    
    username, password, should_fail = data
    
    class Context(object):
        asset = {
            "username": username,
            "password": password,
        }
    
    result = SwMain(Context).execute()
    
    if should_fail:
        assert not result["successful"]
        assert result["errorMessage"]  # Assert that there is an error message
    else:
        assert result["successful"]


@pytest.mark.parametrize('filename,filedata,result',
                         [("myfile.txt",
                           "asdf",
                           {'base64': 'YXNkZg==', 'filename': 'myfile.txt'}),
                          ("newfile.exe",
                           base64.b64decode("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".encode()),
                           {'base64': 'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAGCAYAAAD+Bd/7AAAMRGlDQ1BJQ0MgUHJvZmlsZQAASImVVwdYU8kWnltSIaEEEJASehOlSJcSQotUqYKNkAQSSogJQcTusqjg2kUEbOiqiKJrAcSOvSyKvT8UUVHWRVdsqLxJgXX1e+997+Sbe/975pz/lMwtA4BWDVciyUW1AcgTF0jjw4OZ41PTmKROgMAfHZgCApcnk7Di4qIAlMHzP+XdTWgL5ZqzguvH+f8qOnyBjAcAEgdxBl/Gy4N4PwB4CU8iLQCA6A31VtMKJAo8EWI9KUwQYokCZ6lwiQJnqHCl0iYxng3xTgDImlyuNAsAejPUMwt5WZCHfhtiFzFfJAZAiwxxAE/I5UMcAfGIvLx8BYZ2wD7jG56sf3BmDHFyuVlDWFWLUsghIpkklzv9/2zH/5a8XPlgDFs4NIXSiHhFzbBvt3PyIxVYE+IecUZMLMS6EH8Q8ZX2EKNUoTwiSWWPmvBkbNgzYACxC58bEgmxCcRh4tyYKLU+I1MUxoEYrhC0SFTASVT7LhTIQhPUnDXS/PjYQZwpZbPUvg1cqTKuwv6UPCeJpea/LRRwBvnfFgsTU1Q5Y9RCUXIMxHSIDWQ5CZEqG8y6WMiOGbSRyuMV+VtD7CsQhwer+LHJmdKweLW9NE82WC+2UCjixKhxVYEwMULNs5PHVeZvCHGzQMxKGuQRyMZHDdbCF4SEqmrHrgjESep6sQ5JQXC82veNJDdObY9TBbnhCr0lxCaywgS1Lx5QABekih+PkRTEJaryxDOyuWPjVPngRSAKsEEIYAI5HBkgH2QDUVtPUw+8Us2EAS6QgiwgAM5qzaBHinJGDI8JoBj8AZEAyIb8gpWzAlAI9V+GtKqjM8hUzhYqPXLAU4jzQCTIhddypZd4KFoyeAI1oh+i82CuuXAo5n7UsaAmSq2RD/IytQYtiaHEEGIEMYzogBvjAbgfHgWPQXC44d64z2C2f9sTnhLaCY8JNwgdhDtTRPOl39XDBNGgA0YIU9ec8W3NuC1k9cCDcX/ID7lxA9wYOOOjYSQWHghje0AtW525ovrvuf9RwzddV9tRXCgoZRgliGL/vSfdke4xxKLo6bcdUuWaMdRX9tDM9/HZ33SaD8+R31tiC7F92FnsBHYeO4w1ASZ2DGvGLmFHFHhoFT1RrqLBaPHKfHIgj+iHeFx1TEUnZS71Lt0un1VzBYIixfMRsPMl06WiLGEBkwWf/AImR8wbOYLp5uLqA4DiPaJ6TPVeVr4fECOdv3XziACMyRkYGDj4ty76HAD7DwFAvfW3zh4+n+l3ADi3jieXFqp0uOJAAFSgBe8oI2AGrIA9rMcNeAI/EARCwVgQCxJBKpgMuyyE61kKpoGZYB4oBeVgGVgNqsAGsBlsB7vAXtAEDoMT4Ay4CK6AG+AeXD1d4CXoBe9AP4IgJISGMBAjxByxQZwQN8QbCUBCkSgkHklF0pEsRIzIkZnIT0g5sgKpQjYhdchvyEHkBHIeaUfuII+QbuQN8gnFUE1UDzVFbdFRqDfKQiPRRHQSmoVORYvREnQJWonWojvRRvQEehG9gXagL9E+DGAamAFmgTlj3hgbi8XSsExMis3GyrAKrBZrwFrg/3wN68B6sI84EWfgTNwZruAIPAnn4VPx2fhivArfjjfip/Br+CO8F/9KoBFMCE4EXwKHMJ6QRZhGKCVUELYSDhBOw7upi/COSCQaEO2IXvBuTCVmE2cQFxPXEXcTjxPbiZ3EPhKJZERyIvmTYklcUgGplLSWtJN0jHSV1EX6QNYgm5PdyGHkNLKYPJ9cQd5BPkq+Sn5G7qdoU2wovpRYCp8ynbKUsoXSQrlM6aL0U3WodlR/aiI1mzqPWkltoJ6m3qf+paGhYanhozFOQ6QxV6NSY4/GOY1HGh81dTUdNdmaEzXlmks0t2ke17yj+ReNRrOlBdHSaAW0JbQ62knaQ9oHOoM+ks6h8+lz6NX0RvpV+istipaNFktrslaxVoXWPq3LWj3aFG1bbbY2V3u2drX2Qe1b2n06DB1XnVidPJ3FOjt0zus81yXp2uqG6vJ1S3Q3657U7WRgDCsGm8Fj/MTYwjjN6NIj6tnpcfSy9cr1dum16fXq6+qP1k/WL9Kv1j+i32GAGdgacAxyDZYa7DW4afBpmOkw1jDBsEXDGoZdHfbecLhhkKHAsMxwt+ENw09GTKNQoxyj5UZNRg+McWNH43HG04zXG5827hmuN9xvOG942fC9w++aoCaOJvEmM0w2m1wy6TM1Mw03lZiuNT1p2mNmYBZklm22yuyoWbc5wzzAXGS+yvyY+QumPpPFzGVWMk8xey1MLCIs5BabLNos+i3tLJMs51vutnxgRbXytsq0WmXVatVrbW4dbT3Tut76rg3FxttGaLPG5qzNe1s72xTbBbZNts/tDO04dsV29Xb37Wn2gfZT7WvtrzsQHbwdchzWOVxxRB09HIWO1Y6XnVAnTyeR0zqn9hGEET4jxCNqR9xy1nRmORc61zs/GmkwMmrk/JFNI1+Nsh6VNmr5qLOjvrp4uOS6bHG556rrOtZ1vmuL6xs3RzeeW7XbdXeae5j7HPdm99ejnUYLRq8ffduD4RHtscCj1eOLp5en1LPBs9vL2ivdq8brlreed5z3Yu9zPgSfYJ85Pod9Pvp6+hb47vX908/ZL8dvh9/zMXZjBGO2jOn0t/Tn+m/y7whgBqQHbAzoCLQI5AbWBj4OsgriB20NesZyYGWzdrJeBbsES4MPBL9n+7JnsY+HYCHhIWUhbaG6oUmhVaEPwyzDssLqw3rDPcJnhB+PIERERiyPuMUx5fA4dZzesV5jZ409FakZmRBZFfk4yjFKGtUSjUaPjV4ZfT/GJkYc0xQLYjmxK2MfxNnFTY07NI44Lm5c9bin8a7xM+PPJjASpiTsSHiXGJy4NPFekn2SPKk1WSt5YnJd8vuUkJQVKR3jR42fNf5iqnGqKLU5jZSWnLY1rW9C6ITVE7omekwsnXhzkt2koknnJxtPzp18ZIrWFO6UfemE9JT0HemfubHcWm5fBiejJqOXx+at4b3kB/FX8bsF/oIVgmeZ/pkrMp9n+WetzOoWBgorhD0itqhK9Do7IntD9vuc2JxtOQO5Kbm788h56XkHxbriHPGpfLP8ovx2iZOkVNIx1Xfq6qm90kjpVhkimyRrLtCDH+yX5Pbyn+WPCgMKqws/TEuetq9Ip0hcdGm64/RF058VhxX/OgOfwZvROtNi5ryZj2axZm2ajczOmN06x2pOyZyuueFzt8+jzsuZ9/t8l/kr5r/9KeWnlhLTkrklnT+H/1xfSi+Vlt5a4Ldgw0J8oWhh2yL3RWsXfS3jl10odymvKP+8mLf4wi+uv1T+MrAkc0nbUs+l65cRl4mX3VweuHz7Cp0VxSs6V0avbFzFXFW26u3qKavPV4yu2LCGuka+pqMyqrJ5rfXaZWs/VwmrblQHV++uMalZVPN+HX/d1fVB6xs2mG4o3/Bpo2jj7U3hmxprbWsrNhM3F25+uiV5y9lfvX+t22q8tXzrl23ibR3b47efqvOqq9thsmNpPVovr+/eOXHnlV0hu5obnBs27TbYXb4H7JHvefFb+m8390bubd3nva9hv83+mgOMA2WNSOP0xt4mYVNHc2pz+8GxB1tb/FoOHBp5aNthi8PVR/SPLD1KPVpydOBY8bG+45LjPSeyTnS2Tmm9d3L8yeunxp1qOx15+tyZsDMnz7LOHjvnf+7wed/zBy94X2i66Hmx8ZLHpQO/e/x+oM2zrfGy1+XmKz5XWtrHtB+9Gnj1xLWQa2euc65fvBFzo/1m0s3btybe6rjNv/38Tu6d13cL7/bfm3ufcL/sgfaDiocmD2v/5fCv3R2eHUcehTy69Djh8b1OXufLJ7Inn7tKntKeVjwzf1b33O354e6w7isvJrzoeil52d9T+ofOHzWv7F/t/zPoz0u943u7XktfD7xZ/JfRX9vejn7b2hfX9/Bd3rv+92UfjD5s/+j98eynlE/P+qd9Jn2u/OLwpeVr5Nf7A3kDAxKulKv8FMDgQDMzAXizDQBaKgCMK/D7YYJqn6cURLU3VSLwn7BqL6gUTwAa4Enxuc4+DsAeOGznQm54jg0CIDEIoO7uQ0Mtskx3NxUXvR4AksXAwJt8AChwfA4fGOiPGxj4UgOTvQ7A0eeq/aVCiHBvsNFFga6a7wPfy78BkyB/LUpcrf8AAAAJcEhZcwAAFiUAABYlAUlSJPAAAAGZaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA1LjQuMCI+CiAgIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgICAgIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjg8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpQaXhlbFlEaW1lbnNpb24+NjwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpW5h8pAAAAHGlET1QAAAACAAAAAAAAAAMAAAAoAAAAAwAAAAMAAACVlt/NTwAAAGFJREFUGBkUzEEOgjAQQNHf0nZGmMpCWXgpFl4IrkQ8mZoYYwxjXfzVS364rjf/eOa7g0jCtDCNipVEDJEwL5s/Xjvu0KtwtAOXU6VKR4ituR3uzzfyx2FgNONsiqSMR+cHAAD//9B83lEAAABSSURBVBXMwQ3CQBBD0T/GOxsUpT0aQKKWHFNPbikMJoN8/E+O135WhdnWlWdOFpssmGm+/Ij3cZVC6NHBgzkGlhgWoSA+f0D1hBtkv8xs5EANb2GuJcQ2QIgxAAAAAElFTkSuQmCC', 'filename': 'newfile.exe'})])
def test_create_attachment(filename, filedata, result):

    assert create_attachment(filename, filedata) == [result]
    swa = SwimlaneAttachments()
    swa.add_attachment(filename, filedata)
    swa.add_attachment(filename, filedata)

    assert swa.get_attachments() == [result, result]


def square_keyvals(d):
    new_d = {}
    for k, v in d.items():
        new_d[k] = v*v
    return new_d


class IsTimeVal(object):
    """ Class to test if the value is a time value"""
    def __eq__(self, other):
        return isinstance(other, type(pendulum.now())) or isinstance(other, ComparisonTimeval)


FUTURE_TIMEVAL = ComparisonTimeval.create_timeval("gte now -2 seconds")
PAST_TIMEVAL = ComparisonTimeval.create_timeval("lte now +2 seconds")

querystring_test_data = [
    # querystring, delimiter, assigner, try_type, result
    ["asdf=1,testing_key=2", ",", "=", False, {"asdf": "1", "testing_key": "2"}],
    ["asdf=1,testing_key=2", ",", "=", True, {"asdf": 1, "testing_key": 2}],
    ["asdf=1,testing_key=2,gg=teststring,time=2020-02-26T14:45:48-07:00", ",", "=", True, {"asdf": 1, "testing_key": 2, "gg": "teststring", "time": pendulum.parse("2020-02-26T14:45:48-07:00")}],
    ["asdf:2-ghjkl:3", "-", ":", square_keyvals, {"asdf": 4, "ghjkl": 9}],  # try_type is a func
    ["t1=now -15 minutes,asdf=5", ",", "=", True, {"t1": PAST_TIMEVAL, "asdf": 5}],
    ["t2=now +5 months,asdf=5", ",", "=", True, {"t2": FUTURE_TIMEVAL, "asdf": 5}],
    ["t3=now -1 months,asdf=5", ",", "=", True, {"t3": PAST_TIMEVAL, "asdf": 5}],
    ["t4=lte now -2 months,lteasdf=5", ",", "=", True, {"t4": PAST_TIMEVAL, "lteasdf": 5}],
    ["t5=gte now -2 years,asdf=5", ",", "=", True, {"t5": FUTURE_TIMEVAL, "asdf": 5}],
    ["t6=lt now -2 days,ltasdf=5", ",", "=", True, {"t6": PAST_TIMEVAL, "ltasdf": 5}],
    ["t7=gt now -2 years,asdf=5", ",", "=", True, {"t7": FUTURE_TIMEVAL, "asdf": 5}],
]


@pytest.mark.parametrize("data", querystring_test_data)
def test_querystring_parse(data):
    string, delm, assign, try_type, result = data
    qsp = QueryStringParser(string, delm, assign, try_type)
    parsed = qsp.parse()
    assert result == parsed


PERIOD_START = ComparisonTimeval.create_timeval("now")
PERIOD_1SEC = PERIOD_START.subtract(seconds=1)
PERIOD_1MIN = PERIOD_START.subtract(minutes=1)
PERIOD_1HOUR = PERIOD_START.subtract(hours=1)
PERIOD_1DAY = PERIOD_START.subtract(days=1)
PERIOD_1MONTH = PERIOD_START.subtract(months=1)
PERIOD_1YEAR = PERIOD_START.subtract(years=1)
PERIOD_ALL = PERIOD_START.subtract(years=2, months=5, days=3, hours=12, minutes=30, seconds=5)

iso_period_test_data = [
    # Compare val, other val, result
    [PERIOD_START, PERIOD_1SEC, "PT1S"],
    [PERIOD_START, PERIOD_1MIN, "PT1M"],
    [PERIOD_START, PERIOD_1HOUR, "PT1H"],
    [PERIOD_START, PERIOD_1DAY, "P1D"],
    [PERIOD_START, PERIOD_1MONTH, "P1M"],
    [PERIOD_START, PERIOD_1YEAR, "P1Y"],
    [PERIOD_START, PERIOD_ALL, "P2Y5M3DT12H30M5S"],
    [PERIOD_START, PERIOD_START, "P0D"]
]


@pytest.mark.parametrize("data", iso_period_test_data)
def test_iso_period(data):
    val, other, result = data
    res = ComparisonTimeval.to_iso8601_period(val, other_time=other)
    assert result == res

