"""
Tests for the calculator module using the pytest framework.

This file demonstrates basic pytest conventions:
- Test files are typically named `test_*.py` or `*_test.py`.
- Test functions are prefixed with `test_`.
- Assertions (`assert`) are used to check expected outcomes.
"""

# Import the function to be tested from the source module
from src.calculator import add, subtract


# Define a test function for the 'add' functionality.
# Pytest discovers functions prefixed with 'test_'.
def test_add():
    """Tests the add function with various inputs."""
    # Use 'assert' statements to verify the function's behavior.
    # If an assertion fails, pytest will report the test as failed.
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-5, -5) == -10


def test_subtract():
    """Tests the subtract function."""
    assert subtract(5, 2) == 3
