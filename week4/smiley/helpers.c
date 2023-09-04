#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through each row of the image
    for (int i = 0; i < height; i++)
    {
        // Loop through each column of the image
        for (int j = 0; j < width; j++)
        {
            // Check if current pixel is black
            if (image[i][j].rgbtRed == 0x00 && image[i][j].rgbtGreen == 0x00 && image[i][j].rgbtBlue == 0x00)
            {
                // If pixel is black, change to green
                image[i][j].rgbtGreen = 0xff;
            }
        }
    }
}
