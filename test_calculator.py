#!/usr/bin/env python3
"""
Test/Demo script for the calculator functions
"""

from calculator import add, subtract, multiply, divide

print("Calculator Function Tests")
print("=" * 40)

# Test addition
print(f"10 + 5 = {add(10, 5)}")

# Test subtraction
print(f"10 - 5 = {subtract(10, 5)}")

# Test multiplication
print(f"10 * 5 = {multiply(10, 5)}")

# Test division
print(f"10 / 5 = {divide(10, 5)}")

# Test division by zero
print(f"10 / 0 = {divide(10, 0)}")

# Test with decimals
print(f"7.5 + 2.3 = {add(7.5, 2.3)}")
print(f"15.8 - 3.2 = {subtract(15.8, 3.2)}")
print(f"4.5 * 2 = {multiply(4.5, 2)}")
print(f"9.6 / 3 = {divide(9.6, 3)}")
