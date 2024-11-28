import math

def sum_of_digits(n):
    # Calculate the factorial
    factorial = math.factorial(n)
    
    # Convert the number to a string and sum its digits
    return sum(int(digit) for digit in str(factorial))

result = sum_of_digits(100)
print(result) 



