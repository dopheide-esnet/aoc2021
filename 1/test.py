
import pytest
from aoc1 import Count_Increased, Count_Increased_Sliding

def test_increased():
    lines = ['199', '200', '208', '210', '200', '207', '240', '269', '260', '263']
    res = Count_Increased(lines)
    assert res == 7

def test_sliding():
    lines = ['199', '200', '208', '210', '200', '207', '240', '269', '260', '263']
    res = Count_Increased_Sliding(lines)
    assert res == 5

