#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height from user until height is between 1 and 8.
    int height = 0;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        // Print spaces.
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }

        // Print hashes.
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }

        // Print newline.
        printf("\n");
    }
}
