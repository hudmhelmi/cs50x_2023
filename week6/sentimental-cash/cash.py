from cs50 import get_float

# Init variable for coin count
coins = 0

# Get user's cents in x.xx format
while True:
    cents = int(100 * get_float("Change owed: "))
    if cents > 0:
        break

# Get number of quarters
coins += cents // 25
cents = cents % 25

# Get number of dimes
coins += cents // 10
cents = cents % 10

# Get number of nickels
coins += cents // 5
cents = cents % 5

# Get number of pennies
coins += cents // 1
cents = cents % 1

# Print number of coins
print(coins)