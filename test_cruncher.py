
import cruncher
from unittest.mock import Mock
import pytest

def test_number_cruncher_likes_even_numbers():
    """Test that the crunch method saves number facts for even numbers.
    
    Given:
         A Number cruncher instance getting an even result for its "crunch" method (eg 42)

    Result:
        Method returns "Yum! 42"
        The tummy attribute contains a dict such as {'number': 42, "fact": "42 is the meaning of life."}
    
    """
    nc = cruncher.NumberCruncher(10)
    nc.requester = Mock()
    nc.requester.call.return_value = {'result': 'SUCCESS', 'number': 2, "fact": '2 is a magic number '}
    assert nc.crunch() == "Yum! 2"
    assert len(nc.tummy) == 1
    assert nc.tummy[0] == {'number': 2, "fact": '2 is a magic number '}

def test_number_cruncher_hates_odd_numbers():
    """Test that the crunch method rejects number facts for odd numbers.
    
    Given:
         A Number cruncher instance getting an odd result for its "crunch" method eg 13

    Result:
        Method returns "Yuk! 13"
        The tummy attribute is unchanged.
    
    """
    nc = cruncher.NumberCruncher(5)
    nc.requester = Mock()
    nc.requester.call.return_value = {'result': 'SUCCESS', 'number': 3, "fact": '3 is a crowd'}
    assert nc.crunch() == 'Yuk! 3'
    assert len(nc.tummy) == 0

   


def test_number_cruncher_discards_oldest_item_when_tummy_full():
    """Test that the crunch method maintains a maximum number of facts.
    
    Given:
         A Number cruncher instance with tummy size 3 having 3 items in tummy getting 
         an even result for its "crunch" method, eg 24.

    Result:
        Method deletes oldest result from tummy (eg 42)
        Method returns "Burp! 42"
        The tummy attribute contains 24 but not 42.
    
    """

    nc = cruncher.NumberCruncher(3)
    nc.requester = Mock()
    nc.requester.call.return_value = {'result': 'SUCCESS', 'number': 2, "fact": '2 turtle doves'}
    nc.crunch()
    nc.requester.call.return_value = {'result': 'SUCCESS', 'number': 4, "fact": '4 calling birds'}
    nc.crunch()
    nc.requester.call.return_value = {'result': 'SUCCESS', 'number': 6, "fact": '6 geese a-laying'}
    nc.crunch()
    nc.requester.call.return_value = {'result': 'SUCCESS', 'number': 8, "fact": '8 maids a-milking'}
    assert nc.crunch() == "Burp! 2"
    assert len(nc.tummy) == 3
    assert nc.tummy[0] == {'number': 4, "fact": '4 calling birds'}



def test_number_cruncher_raises_runtime_error_if_invalid_number_request():
    """Test that there is a runtime error if NumberRequester response is
        invalid

        Given:
            A NumberCruncher instance, receiving an invalid NumberRequester
            response (eg an AttributeError)

        Result: 
            Raises RuntimeError
    """
    nc = cruncher.NumberCruncher(3)
    nc.requester = Mock()
    nc.requester.call.return_value = {'result': 'FAILURE', 'error_code': 404}
    with pytest.raises(Exception) as e:
        nc.crunch()
    assert type(e.value) == RuntimeError
    assert "Unexpected error" in str(e.value)
   

