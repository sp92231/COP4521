"""

Name: Shanie Portal
Date: 09/22/2024
Assignment: Module 4: Using Threads with Locks
Due Date: 09/22/2024
About this project: The program uses multiple threads to simulate random payments and track a player's loan balance
until it reaches zero or higher.
All work below was performed by Shanie Portal

"""

import random
import threading
from concurrent.futures import ThreadPoolExecutor
import time

# Filename to store payment amounts.
filename = "temp.txt"
# Initial loan account balance.
loanAcc = -25000
# Create a lock to manage access to shared resources.
lock = threading.Lock()

def clear_file():
    # Clears the contents of the file.
    with open(filename, "w") as f:
        # Clear the file.
        f.write("")
    return

def append_file(num):
    # Appends payment to file with a lock.
    with lock:
        with open(filename, "a") as f:
            # Writes payment amount to file.
            f.write(str(num) + "\n")
    return

def pay():
    #Simulates random payments.
    for _ in range(5):
        # Generates a random payment amount.
        amount = random.randint(1, 1500)
        # Appends the amount to the file.
        append_file(amount)
    return None

def accountant():
    # Reads payment amount from file and updates balance.
    global loanAcc
    with lock:
        with open(filename, "r") as f:
            for line in f:
                # Removes trailing newline.
                line = line.strip()
                # Checks if line has valid number.
                if line.isnumeric():
                    # Updates balance.
                    loanAcc += int(line)
                    # Displays balance.
                    print(f"Current loan account: {loanAcc}")
        # Clears file.
        clear_file()
    return None

def main():
    while loanAcc < 0:
        with ThreadPoolExecutor(max_workers=1) as accountants:
            # Starts accountant thread.
            accountants.submit(accountant)

        with ThreadPoolExecutor(max_workers=25) as payments:
            for _ in range(25):
                # Starts payment threads.
                payments.submit(pay)

        time.sleep(1) 

if __name__ == '__main__':
    main()
