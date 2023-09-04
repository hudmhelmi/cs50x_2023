// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Count of words in the dictionary
int wordCount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Get hash index for word
    int index = hash(word);

    // Traverse linked list at given hash table index. If word is found, return true. Continue until end of list.
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
    }

    // Word was not found in dictionary
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash function using sum of ASCII values
    int sum = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        sum += toupper(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");

    // If dictionary file could not be opened, return false
    if (dict == NULL)
    {
        return false;
    }

    // Buffer to hold word read from dictionary
    char word[LENGTH + 1];

    // Read each word from dictionary file
    while (fscanf(dict, "%s", word) != EOF)
    {
        // Allocate memory for a new node to store the word
        node *new_node = malloc(sizeof(node));

        // If memory allocation fails, clean up and return false
        if (new_node == NULL)
        {
            fclose(dict);
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, word);

        // Hash word
        int index = hash(word);

        // Add the new node to the beginning of the linked list at the calculated hash table index
        new_node->next = table[index];
        table[index] = new_node;

        // Increase word count
        wordCount++;
    }

    // Close dictionary file
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate through hash table
    for (int i = 0; i < N; i++)
    {
        // Set cursor to first index
        node *cursor = table[i];

        // Free each node in the list
        while (cursor != NULL)
        {
            node *tmp = cursor; // Temporary node to hold current node
            cursor = cursor->next; // Move cursor to the next node before freeing current node
            free(tmp); // Free memory allocated for current node
        }
    }
    return true;
}