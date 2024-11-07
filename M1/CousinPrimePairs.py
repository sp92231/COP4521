"""

Name: Shanie Portal
Date: 08/31/2024
Assignment: Module 1: Cousin Prime Pairs
Due Date: 09/01/2024
About this project: Finds, displays, and counts the cousin prime pairs less than the user input.
Assumptions: Assumes the user enters only a numeric value for their input.
All work below was performed by (Your Name)

"""


# Function to check if a value is prime.
def is_prime(num):
    # 1 is not prime.
    if num <= 1:
        return False
    # 2 is only even prime number.
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    i = 3
    # Loops to check if there is another divisor.
    while i * i <= num:
        if num % i == 0:
            return False
        # Only checks odd numbers.
        i += 2
    return True


# Function to find cousin primes.
def is_cousin_pair(prime_list, cousin_primes):
    # Loops through prime_list to check for cousin prime pairs.
    for element in prime_list:
        # Cousin primes differ by 4.
        check = element + 4
        # Checks if check is also prime.
        if is_prime(check):
            # If true, creates pair and adds to cousin_primes list.
            if check in prime_list:
                pair = (element, check)
                cousin_primes.append(pair)


# Main function.
def main():
    # Prompt the user for input.
    user_input = int(input("Please enter in a number > 0. "))

    # Validate if user_input is greater than 0.
    while user_input < 1:
        user_input = int(input("Please enter in a number > 0. "))

    # Declaration of lists.
    prime_list = []
    cousin_primes = []

    # Loop to find prime numbers.
    for num in range(2, user_input + 4):
        if is_prime(num):
            prime_list.append(num)

    # Find cousin primes and print.
    is_cousin_pair(prime_list, cousin_primes)
    for element in cousin_primes:
        print(element)

    # Print the number of cousin prime pairs.
    length = len(cousin_primes)
    print("There are " + str(length) + " Cousin Prime Pairs.")


# Run the main function.
if __name__ == "__main__":
    main()
