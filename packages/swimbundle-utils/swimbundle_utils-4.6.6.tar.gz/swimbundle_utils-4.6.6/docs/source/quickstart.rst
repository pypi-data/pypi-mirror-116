Quickstart
**********
The Swimbundle Utils package has many

- REST_

  - `Making a basic request`_
  - `GET Example`_
  - `POST/PATCH Example`_
  - `DELETE Example`_
  - Authentication_

  - `Polling requests`_
  - `Setting a custom user-agent`_

  - `BasicPaginationEndpoint`_
    
    - `LinkHeadersPaginationEndpoint`_

  - Mixins_

- Exceptions_

- Flattener_
  
  - `Misc Flattening Funcs`_ 
    
    - `hoist_key`_
    - `hoist_keys`_
    - `replace_dict_prefix`_
    - `merge_dicts`_
    - `is_simplelist`_
    - `flatten_single_lists`_
    - `combine_listdict`_
    - `clean_xmltodict_result`_

- Helpers_

  - `asset_parser`_
  - `create_attachment`_

    - `SwimlaneAttachments`_

  - `check_input`_

    - `Input Checker`_

  - `create_test_conn`_

  - `QueryStringParser`_

- Validation_

  - `Special Classes`_

    - IntRange_
      
      - `Positive and Negative IntRange`_
    
    - InfinityVal_
    - FloatRange_
    
  - `Adding Custom Validators`_

    - RegexValidator_


.. _rest:

REST Module
===========
For a REST API, use the ``BasicRestEndpoint`` superclass, in ``swimbundle_utils.rest``


This superclass allows easily creating a task for an endpoint. For example, say we want to integrate with
example.com's indicator API. Here is a table of what their API looks like.

+------------------------------------------+-------------+-----------------------------------+
| Endpoint                                 | HTTP Method | URL Parameters                    |
+==========================================+=============+===================================+
| https://example.com/api/indicator        | GET         | indicator_id (int)                |
+------------------------------------------+-------------+-----------------------------------+
| https://example.com/api/indicator        | POST/PATCH  | indicator_name, indicator_value   |
+------------------------------------------+-------------+-----------------------------------+
| https://example.com/api/indicator/{id}   | DELETE      | (none)                            |
+------------------------------------------+-------------+-----------------------------------+

So we have 3 endpoints, each with different HTTP Methods and parameters, but the same base URL. We can create a
superclass for this integration, let's call it ``ExampleIntegration``


.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint


    class ExampleIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(ExampleIntegration, self).__init__(context.asset["host"]
            # raise_for_status=False  # If we wanted to supress non-200 http codes being raised, set this to False
            )


Basic Request
-------------
.. _`Making a basic request`:

To make a request using this library, you just use

``self.request(<method>, <endpoint>, **kwargs)``

Where ``<method>`` is an HTTP method, ``<endpoint>`` is the URL relative to the host, so like ``/api/indicator``.
The ``**kwargs`` are optional params to pass into the ``requests.request(...)`` call


Basic GET Example
-----------------

Now we create a task, say for the ``GET /api/indicator`` endpoint

.. _`GET Example`:

.. code:: python

    from sw_example import ExampleIntegration  # Import our superclass from above

    class SwMain(ExampleIntegration):
        endpoint = "/api/indicator"
        method = "GET"

        def get_kwargs(self):
            return {
                "params": {
                    "indicator_id": self.indicator_id
                }
            }

        def __init__(self, context):
            super(SwMain, self).__init__(context)
            self.indicator_id = context.inputs["indicator_id"]  # Get indicator from inputs


But we didn't actually make a request here! It is all handled by the ``BasicRestEndpoint`` superclass. The ``params``
kwarg is passed into ``self.request`` which is used to create the full url with ``self.host`` that ends
up like ``https://example.com/api/indicator?indicator_id=<id>``


.. _`POST/PATCH Example`:

Basic POST & PATCH Example
--------------------------

But what if the data required from the API isn't in the URL params? And what if the data returned from the API isn't
suitable for just returning, or needs some parsing?


Let's take a look at the second endpoint, the ``POST/PATCH /api/indicator`` It looks like if we send a ``POST``, it will
create a new indicator. And if we send a ``PATCH`` it will attempt to create a new indicator, or update an existing one,
depending on if the name exists.

We'll give the user the choice of whether to PATCH or POST for this example.

.. code:: python

    from sw_example import ExampleIntegration  # Import our superclass from above


    class SwMain(ExampleIntegration):
        endpoint = "/api/indicator"

        def get_req_method(self):
            if self.create_new:
                return "POST"
            else:
                return "PATCH"

        def get_kwargs(self):
            return {
                "json": {
                    "indicator_name": self.indicator_name,
                    "indicator_value": self.indicator_value
                }
            }

        def parse_response(self, response):
            data = response.json()  # Basically json.loads(response.text)
            return data["data"]

        def __init__(self, context):
            super(SwMain, self).__init__(context)
            self.create_new = context.inputs["create_new"]  # boolean, if True, use POST else use PATCH
            self.indicator_name = context.inputs["indicator_name"]  # Get indicator from inputs
            self.indicator_value = context.inputs["indicator_value"]


This time, the data is passed in under the ``json`` parameter to ``requests`` which automatically formats our data for us
in the POST body. If the data were non-json, we would use ``data`` instead. We also parsed out the data returned, only
returning the JSON under the ``data`` key.


.. _`DELETE Example`:

Basic DELETE Example
--------------------

Similarly to a variable request method, we can have a variable URL. This is quite trivial

.. code:: python

    class SwMain(ExampleIntegration):
        method = "DELETE"

        def get_endpoint(self):
            return "/api/indicator/{iid}".format(iid=self.iid)

        def __init__(self, context):
            super(SwMain, self).__init__(context)
            self.iid = context.inputs["iid"]  # Get the indicator ID from inputs


This variable URL concept is heavily used in the BasicPaginationEndpoint_ example



.. _authentication:

Authentication
--------------


But what if ``example.com`` required authentication to make those calls? There are options for these
authentication methods, Basic Auth, Header Auth, Param Auth, and Custom Auth.

**Basic Auth**

.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint


    class ExampleIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(ExampleIntegration, self).__init__(
                host=context.asset["host"],
                auth=(context.asset["username"], context.asset["password"])
            )

This auth is handled by ``requests`` directly, and automatically parses it out and inserts it into the headers for us

**Header Auth**

.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint, HeaderAuth


    class ExampleIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(ExampleIntegration, self).__init__(
                host=context.asset["host"],
                auth=HeaderAuth({"X-api-key": context.inputs["api_key"]})
            )


This auth is when an API requires a certain header to be sent in each request



**Param Auth**

.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint, ParamAuth


    class ExampleIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(ExampleIntegration, self).__init__(
                host=context.asset["host"],
                auth=ParamAuth({"username": context.inputs["username"], "password" context.inputs["password"]})
            )


This auth is used when the URL contains the authenticating information, like
``https://example.com/api/indicator?indicator_id=<id>&username=<username>&password=<password>``



**Custom Auth**

.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint, AuthBase


    class CustAuth(AuthBase):
        def __init__(self, data):
            self.data = data

        def __call__(self, outgoing_response):
            # outgoing_response.headers.update(self.data)  # Update the headers
            # outgoing_response.cookies.update(sle.data)  # Update cookies
            # Can check auth timeout here too
            return outgoing_response  # Make sure to return the response or it will fail


    class ExampleIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(ExampleIntegration, self).__init__(
                host=context.asset["host"],
                auth=CustAuth(context.inputs["data"])
            )

If the API uses some sort of custom authentication, you'll have to make your own. Using ``requests.auth`` we can
create a custom auth and pass it in

.. _`Polling requests`:

Polling Requests
----------------

Sometimes an API will return a status that indicates that they are still processing your request, and you will need to
send requests until the processing is complete. We can use the polling request here.

.. code:: python

    # def poll_request(self, method, endpoint, step=5, timeout=60, poll_func=None, **kwargs):

    # By default the polling stops if you receive a 200
    # Poll /my/endpoint with default settings
    self.poll_request("GET", "/my/endpoint")

    # Poll /my/endpoint every 5 seconds, giving up after 20 seconds
    self.poll_request("GET", "/my/endpoint", step=5, timeout=60)

    # Custom polling function to check if the json returned says it's finished
    def my_poll_func(poll_method, poll_endpoint, poll_kwargs):
        result = self.request(poll_method, poll_endpoint, **poll_kwargs)
        if r.json()["status"].lower() == "done":
            return result  # Return the final response
        else:
            return False  # If what we return is falsey, then it will continue to poll

    self.poll_request("GET" "/my/endpoint", poll_func=my_poll_func)


.. _`Setting a custom user-agent`:

Setting a Custom User-Agent
---------------------------

To add a custom user agent that is Swimlane standardized, use:


.. code:: python

    self.set_user_agent("mybundle", bundle_version="1.0.0", swimlane_version="4.0.0", {"other": "kwargs here"})




.. _basicpaginationendpoint:

Basic Pagination
----------------
An API may return a single page in a list of results of pages. To make this easy to process, inherit from ``BasicPaginationEndpoint``
and implement the following functions


.. code:: python

    from swimbundle_utils.rest import BasicRestPaginationEndpoint

    def MyIntegration(BasicRestPaginationEndpoint):
        def __init__(self, context):
            # Same init as BasicRestEndpoint, excluding in example

        def get_next_page(self, response):
            data = response.json()
            if "next" in data:
                return data["next"]  # Return the URL for the next call
            else:
                return None  # If this function returns None, all pages have been seen

        def parse_response(self, response):
            data = response.json()
            data.pop("next", None)  # Remove useless keys/clean data of each response here
            return data

        def combine_responses(self, results):
            # Results is a list of parsed responses, from self.parse_response
            all_data = []
            for result in results:
                all_data.extend(result)  # Use .extend to take [1,2,3] + [4,5] -> [1,2,3,4,5]

            return all_data


.. _`LinkHeadersPaginationEndpoint`:

Link Headers Pagination
-----------------------
Some (very few) APIs implement a standard called "Link Headers" which makes pagination very easy. This implementation
is completely done so all you have to do is implement ``combine_responses``


.. code:: python

    from swimbundle_utils.rest import LinkHeadersPaginationEndpoint

    def MyIntegration(LinkHeadersPaginationEndpoint):
        def __init__(self, context):
            # Same init as BasicRestEndpoint, excluding in example

        def combine_responses(self, results):
            # do parsing here


.. _Mixins:

HTTP Method Mixins
------------------
If you have multiple tasks with the similar capabilities but different HTTP methods, it can get annoying to continually
include the ``method = "<method>"`` at the top of the class. To minimize annoyance, you can use some helper mixins


.. code:: python

    class MyTask(MyIntegration, GETMixin):
        # mytask will now use the GET Mixin

The following Mixins exist: ``GETMixin, POSTMixin, PUTMixin, DELETEMixin, PATCHMixin``
It may seem redundant, but they are also included for backwards compatibility of previous versions




.. _exceptions:

Exceptions
==========

When running into a known exception, or raising a custom exception, use ``swimbundle_utils.exceptions.SwimlaneIntegrationException``


.. code:: python

    if response == invalid:
        raise SwimlaneIntegrationException("API Returned invalid response, check inputs!")
    else:
        ...

If your exception specifically relates to Authentication, use a ``SwimlaneIntegrationAuthException``


.. _flattener:

Flattener
=========

One useful utility for making Swimlane Bundles is the Flattener, which helps to simplify complex JSON.

Basic Usage

.. code:: python

    from swimbundle_utils.flattener import Flattener, do_flatten

    data = {
        "outer_key": {
            "inner_key1": "inner val 1",
            "inner_key2": "inner val 2"
        },
        "basic_key": "value",
        "basic_list": ["1", "2", "3"],
        "mixed_list": [1, "2", "3"],
        "basic_list2": [1, 2, 3]
    }

    # Simple flatten
    flat_data = do_flatten(data)

    # Instance analogue
    flat_data = Flattener(prefix=None, stringify_lists=True, shallow_flatten=False,
               keep_simple_lists=True, autoparse_dt_strs=True).flatten(data)


``flat_data`` will now look like:

.. code:: python

    {
    'outer_key_inner_key1': 'inner val 1',
    'basic_list': ['1', '2', '3'],  # Simple list kept as a list
    'basic_key': 'value',
    'outer_key_inner_key2': 'inner val 2',
    'basic_list2': [1, 2, 3],  # Simple list kept as list
    'mixed_list': '1,2,3'  # Nonsimple list CVSV'd
    }

Here is a description of the params you can pass to a ``Flattener()`` object or ``do_flatten``

Prefix
------
Prefix to add to the data after flattening

.. code:: python

    do_flatten({"a": 5}, prefix="my_prefix")
    # {"my_prefix_a": 5}


Stringify Lists
----------------
Turn lists with basic types into CSV, defaults to True.
This option is ignored for simple lists if ``keep_simple_lists`` is True

.. code:: python

    stringify = <True or False>
    do_flatten({"a": [1,2,3]}, stringify_lists=stringify, keep_simple_lists=False)
    # True -> {"a": "1,2,3"}
    # False -> {"a": [1,2,3]}

Shallow Flatten
---------------
Ignore the first level of nesting, and only flatten each element within it. Used for lists of dictionaries

.. code:: python

    data = [
        {"a": { "sub_a": 1 }, "b": 5},
        {"a": { "sub_a": 2 }, "b": 6},
    ]
    shallow = <True or False>
    do_flatten(data, shallow_flatten=shallow)
    # True -> [
    #    {"a_sub_a": 1, "b": 5},
    #    {"a_sub_a": 2, "b": 6}
    # ]

    # False -> {"a_sub_a": [1,2], "b": [5,6]}


Keep Simple Lists
-----------------
If a list in the resulting flattened dict is only integers or only strings, even if stringify_lists is True, keep this list


.. code:: python

    simple = <True or False>
    do_flatten({"a": [1,2,3], "b": ["c", 4]}, keep_simple_lists=simple)
    # True -> {"a": [1,2,3], "b": "c,4"}
    # False -> {"a": "1,2,3", "b": "c,4"}


Autoparse Datetime Strings
--------------------------
Attempt to automatically parse datetime looking strings/ints/floats to ISO8601. Defaults to True


.. code:: python

    autoparse = <True or False>
    do_flatten({"date": "2019-09-19 14:53:32"}, autoparse_dt_strs=autoparse)
    # True ->  {"date": "2019-09-19T14:53:32-06:00"}
    # False -> {"date": "2019-09-19 14:53:32"}



Special DateTime Formats
------------------------
List of string formats to attempt parsing on for auto DT parsing. Will be ignored if autoparse_dt_strs is False


.. code:: python


    my_format = "%Y+%m+%d"  # Odd format that uses +'s to separate Y/m/d
    # Can't use do_flatten here, since it's a special option for this instance of the flattener
    fl = Flattener(special_dt_formats=[my_format])

    data = {"date": "2019+09+19"}
    fl.flatten(data)
    # -> {"date": "2019-09-19T00:00:00+00:00"}
    # If we didn't use this format
    do_flatten(data)
    # -> {"date": "2019+09+19"}  # Not parsed



Oldest Date Time Allowed
------------------------
String of the oldest datetime that is allowed to be parsed. Defaults to 2005
This is added so that large numbers don't get treated as timestamps

.. code:: python

    data = {"maybe_date_maybe_number": 1568927281.115227, "number": 123456}
    # Can't use do_flatten here, since it's a special option for this instance of the flattener
    fl = Flattener(oldest_dt_allowed="2005")
    fl.flatten(data)
    # {"number": 123456, "maybe_date_maybe_number": '2019-09-19T21:08:01+00:00'}
    # Note how it converted the timestamp that was within the date range


.. _`Misc Flattening Funcs`:

Misc Flattening Functions
-------------------------
There are many useful flattening functions for more complicated data


**Hoist Key(s)**

.. _`hoist_key`:
.. _`hoist_keys`:

Grab keys from a list of dicts

.. code:: python

    hoist_key("a", [{"a": 5}, {"a": 6}])
    # -> [5, 6]

    hoist_keys(["a", "b"], [{"a": 5, "b": 1}, {"a": 6, "b": 2}])
    # -> [[5, 6], [1, 2]]


.. _`replace_dict_prefix`:

**Replace Dict Prefix**


Replace a prefix in a dictionary

.. code:: python

    replace_dict_prefix("aaa", "bbbb", {"aaa_data": 5})
    # -> {'bbbb_data': 5}
    # Or more commonly like:

    replace_dict_prefix("aaa_", "", {"aaa_data": 5})
    # -> {'data': 5}


.. _`merge_dicts`:

**Merge Dicts**
Merge two dictionaries together, regardless if they share keys or not. If they share keys, it uses `combine_listdict`_


.. code:: python

    merge_dicts({"a": 1}, {"b": 2})
    # -> {"a": 1, "b": 2}

    merge_dicts({"a": 1}, {"a": 2})
    # -> {"a": [1, 2]})


.. _`is_simplelist`:

**Is SimpleList**

Check if a list is purely of integers or purely of strings

.. code:: python

    is_simplelist([1,2,3])
    # -> True
    is_simplelist([1,2,"3"])
    # -> False

.. _`flatten_single_lists`:

**Flatten Single Lists**

Flatten all keys in a dict that are lists with a single entry

.. code:: python

    flatten_single_lists({"a": [1,2,3], "b": [5]})
    # -> {"b": 5,"a": [1, 2, 3]}


.. _`combine_listdict`:

**Combine ListDict**

Combine a list of dictionaries into a single dictionary


.. code:: python

    combine_listdict([{"a": 1},{"a": 2}, {"a": 3}])
    # -> {"a": [1, 2, 3]}

    complicated_data = [
        {
            "a": "entry 1",
            "b": "v1"
        },
        {
            "b": "v2"
        },
        {
            "a": "entry 2"
        }
    ]
    combine_listdict(complicated_data)
    # -> {
    #   'a': ['entry 1', None, 'entry 2'],
    #   'b': ['v1', 'v2', None]
    #}

Note how the missing entries were filled in with ``None`` This is to ensure the ordering of elements can be obtained
in the flattened dict result.

Also note that attempting to combine a list of dictionaries with nonbasic keys (subdicts or lists) can lead to odd results, or
not be possible to combine in that form



**Clean XMLToDict Result**

.. _`clean_xmltodict_result`:

XMLToDict returns very ugly data, this helps clean it up. It only cleans top-level keys, so it is most effective after
flattening

.. code:: python

    import xmltodict

    ugly_xml = "<xml><key attr=\"5\">val</key></xml>"
    xml_dict = xmltodict.parse(ugly_xml)
    clean_xmltodict_result(do_flatten(xml_dict))
    # -> {u'xml_key_text': u'val', u'xml_key_attr': "5"}


Helper Functions
================

.. _Helpers:

The ``helper`` submodule is a collection of useful functions for miscellaneous parts of building Swimlane bundles.

Asset Parser
------------

.. _asset_parser:

The ``asset_parser`` function is used to split the incoming ``Context`` object into a ``super()`` call for ``BasicRestEndpoint``

In the following example, the ``Context`` object is parsed, and with ``auth`` set to "basic" the username and password
are automatically set up for Basic HTTP auth.

.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint
    from swimbundle_utils.helpers import asset_parser


    class MyIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(MyIntegration, self).__init__(**asset_parser(context, auth="basic"))


    class Context(object):
        asset = {
            "host": "abc.com",
            "username": "bb",
            "password": "cc",
            "verify_ssl": False,
            "http_proxy": None
        }


If custom auth is needed, you can specify it in the same ``auth`` parameter, like below

.. code:: python

    from swimbundle_utils.rest import BasicRestEndpoint, HeaderAuth
    from swimbundle_utils.helpers import asset_parser


    class MyIntegration(BasicRestEndpoint):
        def __init__(self, context):
            super(MyIntegration, self).__init__(**asset_parser(context,
                                                               auth=HeaderAuth({"X-api-key": context.asset["api_key"]}))
                                                )


    class Context(object):
        asset = {
            "host": "abc.com",
            "api_key": "asdf",
            "verify_ssl": False,
            "http_proxy": None
        }


Swimlane Attachments
--------------------

.. _`create_attachment`:

.. _`SwimlaneAttachments`:

This helper function is to create attachments easily, in Swimlane output format. You can either create a single attachment,
with ``create_attachment``

.. code:: python

    from swimbundle_utils.helpers import create_attachment

    output = {
        "attachment_key1": create_attachment("myfile.txt", "this is a text file")
        "attachment_key2": create_attachment("myfile.exe", <byte data here>)
    }

Or multiple attachments with ``SwimlaneAttachments``

.. code:: python

    from swimbundle_utils.helpers import SwimlaneAttachments


    swa = SwimlaneAttachments()


    swa.add_attachment("myfile.txt", "this is a text file")
    swa.add_attachment("myfile.exe", <byte data here>)


    output = {
        "attachment_list": swa.get_attachments()
    }


Input Checking
--------------

.. _`check_input`:

.. _`Input Checker`:

Basic input checking can be done for single instances with ``check_input`` or a reusable instance with ``InputChecker``

Apply Order:

1. flags
2. mappings
3. options


InputChecking Params:

**Flags**:

Current flags available

.. code:: python

    lower - forces the input to lowercase (will fail on nonstrings)
    upper - forces the inputs to uppercase (will fail on nonstrings)
    optional - marks the input as optional, so it won't fail on None

**Mappings**:

Map incoming data to another value, most useful when receiving "enable" or "disable" to map to "True" and "False"

**Options**:

The only option currently implemented is the ``type`` option, with multiple types pre-implemented

.. code:: python

    ipv4 - input is an ipv4 address
    url  - input is a url
    domain - input is a domain
    int - input is an integer
    bool - input is a boolean
    datetime - input is datetime parsable


Custom type validations can be implemented and added to the validator list using the Validation_ submodule.

Import statements for examples:

.. code:: python

    from swimbundle_utils.helpers import InputChecker, check_input
    from swimbundle_utils.validation import IntRange, PositiveIntRange, NegativeIntRange, InfinityVal


Check input is within list

.. code:: python

    my_input = "asdf"
    r = check_input(my_input, ("aaaa", "asdf"))


Check that input is capitalized

.. code:: python

    my_input = "asdf"
    r = check_input(my_input, "ASDF", flags=["caps"])


Create an input checker for re-use
Map ``enable -> True``, ``disable-> False``

.. code:: python

    inp = InputChecker(mapping={"enable": True, "disable": False})
    # Since mapping is done before option checking, the mapped string will be a boolean
    inp.check("enable", [True, False], options={"type": "bool"})


Flag the input as optional, ignore if none

.. code:: python

    inp = InputChecker()
    inp.check(None, flags=["optional"])


Check that the input is an int [0, 6)

.. code:: python

    my_input = 5
    r = check_input(my_input, IntRange(0, 6), options={"type": "int"})


Check that the input is an int [0, +infinity)

.. code:: python

    my_input = 5
    r = check_input(my_input, PositiveIntRange(include_zero=True), options={"type": "int"})


Check that the input is an int (-infinity, 0]

.. code:: python

    my_input = 5
    r = check_input(-1 * my_input, NegativeIntRange(include_zero=True), options={"type": "int"})


Check input is an int [4, +inf)

.. code:: python

    my_input = 5
    r = check_input(my_input, IntRange(4, InfinityVal()), options={"type": "int"})

Check that input is a datetime parsable

.. code:: python

    my_input = "2019-09-03T15:17:49-06:00"
    r = check_input(my_input, None, options={"type": "datetime"})


Create Test Connection
----------------------

.. _`create_test_conn`:

Creating test connections can be repetitive, so a test connection that looks like this:

.. code:: python

    from swimbundle_utils.helpers import create_test_conn

    # My Integration Auth, copied from __init__.py for example purposes
    class MyIntegration(object):
        def __init__(self, context):
            # Do auth here
            pass

        def do_auth(self):
            pass


    class SwMain(object):
        def __init__(self, context):
            self.context = context

        def execute(self):
            try:
                MyIntegration(self.context).do_auth()

                return {"successful": True}
            except Exception as e:
                return {"successful": False, "errorMessage": str(e)}




Can be easily turned into

.. code:: python

    SwMain = create_test_conn(MyIntegration, execute_func="do_auth")

Note that if you do authentication in ``__init__`` you can exclude the ``execute_func`` param

To add additional debug functions, you can include the ``custom_test_funcs`` parameter, which is a list of functions that
have the following signature.

.. code:: python

    def my_custom_test_function(self, **kwargs):
        # kwargs is identical to context.asset
        if "Test Passes":
            return True
        else:
            return Exception("Test didn't pass because...")

    SwMain = create_test_conn(MyIntegration, custom_test_funcs=[my_custom_test_function])

Query String Parser
-------------------

.. _`QueryStringParser`:

Parsing in strings for a key/value setup within a single input line can be difficult, especially when the characters might need a different delimiter or assigner.
This sort of issue has popped up in multiple places, so it's been standardized here


.. code:: python

    from swimbundle_utils.helpers import QueryStringParser
    QueryStringParser("a=1,b=2").parse()
    >>>{"a": "1", "b": "2"}  # Note that the types have not been changed, they are strings
    QueryStringParser("ss==gg:5|fss_+=4:8", delimiter="|", assigner=":", try_type=True).parse()
    >>>{"ss==gg": 5, "fss_+=4": 8}  # Note that the types have been converted from strings to ints
    def square_ints(parsed_data):
        # parsed_data is a dict of key->value already been typecasted, apply custom types in this func
        # So we will take integers and square them
        new_data = {}
        for k, v in parsed_data.items():
            if isinstance(v, int):
                new_data[k] = v*v  # Square if int
            else:
                new_data[k] = v  # Otherwise ignore
    QueryStringParser("asdf=5,ghjkl=10,hhhh=iiii", try_type=square_ints)
    >>>{"asdf": 25, "ghjkl": 100, "hhhh": "iiii"}



Validation
==========

.. _Validation:


The ``validation`` submodule is used with `Input Checker`_ to create more complex validation schemas

Special Classes
---------------

.. _`Special Classes`:

**Int Range**:

.. _IntRange:

Create a value that is a range of integers like

.. code:: python

    # Effective range [start, end)
    IntRange(start, end)  # Doesn't include end, like range()

**Positive and Negative IntRange**:

.. _`Positive and Negative IntRange`:

Useful when checking to make sure an ID is positive. Also have negative counterpart

.. code:: python

    PositiveIntRange(include_zero=False)  # [1, +infinity)
    PositiveIntRange(include_zero=True)  # [0, +infinity)
    NegativeIntRange(include_zero=False)  # (-infinity, -1]
    PositiveIntRange(include_zero=True)  # (-infinity, 0]

**InfinityVal**:

.. _InfinityVal:

To create a range with infinity, such as a range with an offest of 5, use ``InfinityVal``

.. code:: python

    IntRange(5, InfinityVal()) # [5, +infinity)

**FloatRange**:

.. _FloatRange:

Less common are ranges that need to be floats, used similarly to ``IntRange``

.. code:: python

    FloatRange(-0.5, 0.5) # [-0.5, 0.5) doesn't include 0.5

Adding Custom Validators
------------------------

.. _`Adding Custom Validators`:


When validating input, the given classes may not be enough, so you can create your own. A good start is the ``RegexValidator``
but for more control you can override the Validator class

**Regex Validator**:

.. _RegexValidator:

Adding a validator with ``RegexValidator``

.. code:: python

    from swimbundle_utils.helpers import InputChecker
    from swimbundle_utils.validation import RegexValidator

    inp = InputChecker()
    reg = RegexValidator("myregex", name="myregex")

    # If override is true, can override default validators like url,ipv4, etc..
    inp.validators.add_type_validator_inst(reg, override=False)


    inp.check("myregex", options={"type": "myregex"})


Adding a function as a validator

.. code:: python

    from swimbundle_utils.helpers import InputChecker
    from swimbundle_utils.validation import ValidValue, InvalidValue


    def check_is_myinput(value):
        if value == "myinput":
            return ValidValue(value)
        else:
            return InvalidValue(value)


    inp = InputChecker()

    # Name of validator is myvalidator
    # If override is true, can override default validators like url,ipv4, etc..
    inp.validators.add_type_validator("myvalidator", check_is_myinput, override=False)

    inp.check("myinput", options={"type": "myvalidator"})



