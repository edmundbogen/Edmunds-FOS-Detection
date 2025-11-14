#!/usr/bin/env python3
"""
Simple Calculator
Supports basic arithmetic operations: +, -, *, /
"""

def add(x, y):
    """Add two numbers"""
    return x + y

def subtract(x, y):
    """Subtract two numbers"""
    return x - y

def multiply(x, y):
    """Multiply two numbers"""
    return x * y

def divide(x, y):
    """Divide two numbers"""
    if y == 0:
        return "Error: Division by zero!"
    return x / y

def calculator():
    """Main calculator function"""
    print("Simple Calculator")
    print("-" * 40)
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")
    print("-" * 40)

    while True:
        choice = input("\nEnter operation (1-5 or +, -, *, /, q to quit): ").strip()

        if choice in ['5', 'q', 'quit', 'exit']:
            print("Goodbye!")
            break

        if choice not in ['1', '2', '3', '4', '+', '-', '*', '/']:
            print("Invalid operation! Please try again.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
            continue

        if choice in ['1', '+']:
            result = add(num1, num2)
            operation = "+"
        elif choice in ['2', '-']:
            result = subtract(num1, num2)
            operation = "-"
        elif choice in ['3', '*']:
            result = multiply(num1, num2)
            operation = "*"
        elif choice in ['4', '/']:
            result = divide(num1, num2)
            operation = "/"

        print(f"\n{num1} {operation} {num2} = {result}")

if __name__ == "__main__":
    calculator()
