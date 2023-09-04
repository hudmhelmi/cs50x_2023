#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1; // argc - 1 is the total number of arguments passed minus one, typicall the program itself
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1]; // + 1 again to avoid adding the program name itself as a candidate
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name)) // vote() presumably returns false when invalid name given
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner(); // print_winner() presumably calculates who wins
}

// Update vote totals given a new vote
bool vote(string name)
{

    // If no names provided somehow
    if (candidates[0].name == NULL)
    {
        return false;
    }

    // Loop through all candidate names
    for (int i = 0; i < candidate_count; i++)
    {
        // If input matches a candidate name
        if (strcmp(name, candidates[i].name) == 0)
        {
            // ++ votes
            candidates[i].votes++;
            return true;
        }
    }
    return false; // Return false if no match found
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // Variable to keep track of current highest score
    int highscore = -1;

    // Loop through all scores
    for (int i = 0; i < candidate_count; i++)
    {
        // If votes higher or equal
        if (candidates[i].votes >= highscore)
        {
            // Update current_highscore
            highscore = candidates[i].votes;
        }
    }

    // Loop through array of winners
    for (int i = 0; i < candidate_count; i++)
    {
        // If not NULL, print
        if (candidates[i].votes == highscore)
        {
            // Print name
            printf("%s\n", candidates[i].name);
        }
    }
}