#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Function prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculateIndex(string text, int letterCount, int wordCount, int sentenceCount);

int main(void)
{
    string text = get_string("Text: "); // Get input text
    int letterCount = count_letters(text);
    int wordCount = count_words(text);
    int sentenceCount = count_sentences(text);
    int index = calculateIndex(text, letterCount, wordCount, sentenceCount);

    // Print readability grade
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index < 16)
    {
        printf("Grade %i\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

// Counts the number of letters in the given text
int count_letters(string text)
{
    int letterCount = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]) != 0) // Check if the character is alphabetic
        {
            letterCount++;
        }
    }
    return letterCount;
}

// Counts the number of words in the given text
int count_words(string text)
{
    int wordCount = 1; // Start with 1 because the first word doesn't have a space before it
    for (int i = 0; i < strlen(text); i++)
    {
        if (isblank(text[i]) != 0) // Check if the character is a space
        {
            wordCount++;
        }
    }
    return wordCount;
}

// Counts the number of sentences in the given text
int count_sentences(string text)
{
    int sentenceCount = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?') // Check for sentence-ending punctuation
        {
            sentenceCount++;
        }
    }
    return sentenceCount;
}

// Calculate the Coleman-Liau index for the given text
int calculateIndex(string text, int letterCount, int wordCount, int sentenceCount)
{
    float L = (float)letterCount / wordCount * 100;
    float S = (float)sentenceCount / wordCount * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    return round(index);
}
