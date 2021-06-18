from unittest.mock import call, patch

import fizzbuzz

# import pytest

"""
Write a program that prints the numbers from 1 to 100. But for multiples of three print “Fizz” instead of the number
and for the multiples of five print “Buzz”. For numbers which are multiples of both three and five print “FizzBuzz”.
"""


@patch("builtins.print")
def test_main(mocked_print):
    fizzbuzz.main()
    assert len(mocked_print.mock_calls) == 100
    assert mocked_print.mock_calls[0] == call("1")
    assert mocked_print.mock_calls[1] == call("2")
    assert mocked_print.mock_calls[2] == call("Fizz")
    assert mocked_print.mock_calls[4] == call("Buzz")
    assert mocked_print.mock_calls[14] == call("FizzBuzz")
    assert mocked_print.mock_calls[97] == call("98")
    assert mocked_print.mock_calls[98] == call("Fizz")
    assert mocked_print.mock_calls[99] == call("Buzz")
