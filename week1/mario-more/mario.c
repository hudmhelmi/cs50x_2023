#include <cs50.h>
#include <stdio.h>

#define MIN_HEIGHT 1
#define MAX_HEIGHT 8

int main(void)
{
    // Get height from user until height is between 1 and 8 inclusive.
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < MIN_HEIGHT || height > MAX_HEIGHT);

    for (int row = 0; row < height; row++)
    {
        // Print pre-gap spaces.
        for (int space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }

        // Print pre-gap hashes.
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }

        // Print gap spaces.
        printf("  ");

        // Print post-gap hashes.
        for (int gap = 0; gap <= row; gap++)
        {
            printf("#");
        }

        // Print newline.
        printf("\n");
    }
}
