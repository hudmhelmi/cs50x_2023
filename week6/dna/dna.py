import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # Read database file into a variable
    database = []
    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)
        for person in reader:
            for key in person.keys():
                if key != "name":
                    person[key] = int(person[key])
            database.append(person)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as f:
        sequence = f.read()

    # Find longest match of each STR in DNA sequence
    str_profile = {}
    subsequences = list(database[0])[1:]
    for subsequence in subsequences:
        str_profile[subsequence] = longest_match(sequence, subsequence)

    # Check database for matching profiles
    for person in database:
        person_profile = {k: person[k] for k in subsequences}
        if person_profile == str_profile:
            print(person["name"])
            return
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
