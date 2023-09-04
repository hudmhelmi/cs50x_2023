#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Define the constant representing the number of bits in a byte
const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // Ask the user for a message and store it in the variable 'message'
    string message = get_string("Input your message: ");

    // Loop over each character of the message
    for (int i = 0, n = strlen(message); i < n; i++)
    {
        // Convert each character to its ASCII value and store it in 'ascii_val'
        int ascii_val = (int) message[i];

        // Array to store the binary representation
        int binary[BITS_IN_BYTE] = {0};

        // Convert the ASCII value to binary and store it in the 'binary' array
        // We start from the rightmost bit
        for (int j = BITS_IN_BYTE - 1; j >= 0; j--)
        {
            // Find the remainder when divided by 2 using the modulo operator
            // This gives us the rightmost bit in the binary representation
            binary[j] = ascii_val % 2;

            // Divide the ASCII value by 2 for the next iteration
            ascii_val = ascii_val / 2;
        }

        // Loop over the binary array and print each bit as a bulb
        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            print_bulb(binary[j]);
        }

        // Print a newline after each character to separate bytes
        printf("\n");
    }
}

// Function to print a bulb emoji depending on whether the bit is 0 or 1
void print_bulb(int bit)
{
    // If the bit is 0, print a dark bulb emoji
    if (bit == 0)
    {
        printf("\U000026AB");
    }
    // If the bit is 1, print a light bulb emoji
    else if (bit == 1)
    {
        printf("\U0001F7E1");
    }
}
