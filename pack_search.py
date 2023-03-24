import pytest
from your_module import PackSearch

@pytest.fixture
def pack_search():
    return PackSearch()

def test_common_regex(pack_search):
    query = "Please call me on +123-456-7890"
    expected_result = [
        "Please call me on ",
        [
            {
                "token": "+123-456-7890",
                "metaData": {
                    "relation": "phone_no"
                }
            }
        ]
    ]
    pack_search.common_regex(query)
    assert pack_search.regex_result == expected_result

def test_email_regex(pack_search):
    query = "My email address is test@example.com"
    expected_result = {
        "regex_result": ["My email address is ", [{
            "entityClass": "email",
            "token": "test@example.com",
            "parentClass": "/",
            "metaData": {
                "match": 100,
                "relation": "email"
            }
        }]],
    }
    pack_search.relation = "email"
    pack_search.email_regex(query)
    assert pack_search.regex_result == expected_result

def test_num_regex(pack_search):
    query = "The value is 123.45"
    expected_result = {
        "regex_result": ["The value is ", [{
            "entityClass": "float",
            "token": "123.45",
            "parentClass": "/",
            "metaData": {
                "match": 100,
                "relation": "float"
            }
        }]],
    }
    pack_search.relation = "num"
    pack_search.num_regex(query)
    assert pack_search.regex_result == expected_result

def test_vehicle_regex(pack_search):
    query = "The vehicle number is MH-01-AB-1234"
    expected_result = {
        "regex_result": ["The vehicle number is ", [{
            "entityClass": "vehicle no",
            "token": "MH-01-AB-1234",
            "parentClass": "/",
            "metaData": {
                "match": 100,
                "relation": "vehicle no"
            }
        }]],
    }
    pack_search.relation = "vehicle no"
    pack_search.vehicle_regex(query)
    assert pack_search.regex_result == expected_result

def test_roman_converter(pack_search):
    query = "This is a roman numeral: IX"
    expected_result = {
        "regex_result": ["This is a roman numeral: ", [{
            "entityClass": "roman",
            "token": "IX",
            "parentClass": "/",
            "metaData": {
                "match": 100,
                "relation": "roman"
            }
        }]],
    }
    pack_search.relation = "roman"
    pack_search.roman_converter(query)
    assert pack_search.regex_result == expected_result
