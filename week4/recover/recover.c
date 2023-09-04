#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Define a block size of 512 bytes for the purpose of reading the memory card
#define BLOCK_SIZE 512

// Define a BYTE as an 8-bit unsigned integer to represent a single byte of data
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check if the program is being called with exactly one command line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        // If not, print usage information and return 1 (indicating error)
        return 1;
    }

    // Attempt to open the memory card file specified by the command line argument
    FILE *card = fopen(argv[1], "r");

    // If the memory card file couldn't be opened, print an error message and return 1
    if (card == NULL)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 1;
    }

    // Define a buffer of size BLOCK_SIZE to hold data read from the memory card
    BYTE buffer[BLOCK_SIZE];

    // Initialize a counter to keep track of the number of JPEG files found
    int fileCounter = 0;

    // Declare a pointer to hold the current output JPEG file
    FILE *img = NULL;

    // Array to hold the filename of the current JPEG
    char filename[8];

    // Loop over the memory card, reading in blocks of size BLOCK_SIZE until the end of the card is reached
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Check if the start of a new JPEG file has been found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If this is not the first JPEG found
            if (fileCounter != 0)
            {
                // Close the current JPEG file
                fclose(img);
            }

            // Open a new JPEG file for writing
            sprintf(filename, "%03i.jpg", fileCounter);
            img = fopen(filename, "w");
            // Write the first block of the new JPEG file
            fwrite(buffer, BLOCK_SIZE, 1, img);
            // Increment the JPEG file counter
            fileCounter++;
        }
        // If this block doesn't start a new JPEG
        else
        {
            // If a JPEG file is already being written
            if (img != NULL)
            {
                // Write the block to the current JPEG file
                fwrite(buffer, BLOCK_SIZE, 1, img);
            }
        }
    }
    // After reading through the entire memory card, close any open files
    if (img != NULL)
    {
        fclose(img);
    }
    // Close the memory card file
    fclose(card);
}
