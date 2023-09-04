#include <cs50.h>
#include <stdio.h>

#define AMEX_DIGITS 15
#define MASTERCARD_DIGITS 16
#define VISA_DIGITS_ONE 13
#define VISA_DIGITS_TWO 16

// Function to count the number of digits in a number.
int countDigits(long number)
{
    int count = 0;
    while (number != 0)
    {
        number /= 10;
        ++count;
    }
    return count;
}

// Function to retrieve the first two digits of a number.
int getFirstTwoDigits(long number)
{
    while (number >= 100)
    {
        number /= 10;
    }
    return number;
}

// Step 1 of Luhn's algorithm: Function to double every other digit and add the resulting digits together.
int sumDoubledDigits(long number)
{
    int sum = 0;
    while (number > 0)
    {
        int digit = (number % 100 / 10) * 2; // Extracting every other digit and doubling it.
        sum += digit % 10 + digit / 10;      // Adding the resulting digits together.
        number /= 100;                       // Move to the next pair of digits.
    }
    return sum;
}

// Step 2 of Luhn's algorithm: Function to sum up the digits that weren't doubled.
int sumRemainingDigits(long number)
{
    int sum = 0;
    while (number > 0)
    {
        sum += number % 10; // Adding the current digit to the sum.
        number /= 100;      // Move to the next pair of digits.
    }
    return sum;
}

// Function to validate the credit card number and determine the card type.
string validateCardNumber(long cardNumber)
{
    int numDigits = countDigits(cardNumber);
    int digitSum = sumDoubledDigits(cardNumber) + sumRemainingDigits(cardNumber);
    int firstTwoDigits = getFirstTwoDigits(cardNumber);

    if (digitSum % 10 != 0) // Step 3 of Luhn's algorithm: Check if the total modulo 10 is congruent to 0.
    {
        return "INVALID";
    }
    else if ((numDigits == AMEX_DIGITS) && (firstTwoDigits == 34 || firstTwoDigits == 37))
    {
        return "AMEX";
    }
    else if ((numDigits == MASTERCARD_DIGITS) && (firstTwoDigits >= 51 && firstTwoDigits <= 55))
    {
        return "MASTERCARD";
    }
    else if ((numDigits == VISA_DIGITS_ONE || numDigits == VISA_DIGITS_TWO) && (firstTwoDigits / 10 == 4))
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}

int main(void)
{
    long cardNumber = get_long("Number: "); // Prompt user for the credit card number.
    string cardType = validateCardNumber(cardNumber);
    printf("%s\n", cardType);
}
