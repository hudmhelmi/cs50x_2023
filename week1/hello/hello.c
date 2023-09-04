#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get user's name
    string name = get_string("What's your name? ");
    // Print hello, user
    printf("hello, %s\n", name);
}