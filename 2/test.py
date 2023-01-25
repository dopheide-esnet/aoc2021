
import pytest
from aoc2 import Dive, Aim

def test_dive():
    lines = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']
    res = Dive(lines)
    assert res == 150

def test_aim():
    lines = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']
    res = Aim(lines)
    assert res == 900