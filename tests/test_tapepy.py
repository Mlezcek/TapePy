import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tapepy import core, export, stats, tape


@tape
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
