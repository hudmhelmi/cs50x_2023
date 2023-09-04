from cs50 import get_string


def main():
    # Get user's input
    text = get_string("Text: ")

    # Calculate index
    letter_count = count_letters(text)
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    index = calculate_index(letter_count, word_count, sentence_count)
    # Print grade
    if index < 1:
        print("Before Grade 1")

    elif index >= 1 and index < 16:
        print(f"Grade {index}")

    else:
        print("Grade 16+")


# Returns number of letters in text
def count_letters(text):
    letter_count = 0
    for letter in text:
        if letter.islower() or letter.isupper():
            letter_count += 1
    return letter_count


# Returns number of words in text
def count_words(text):
    word_count = len(text.split())
    return word_count


# Returns number of sentences in text
def count_sentences(text):
    sentence_count = 0
    for char in text:
        if char in ".!?":
            sentence_count += 1
    return sentence_count


# Calculate the Coleman-Liau index
def calculate_index(letter_count, word_count, sentence_count):
    L = letter_count / word_count * 100
    S = sentence_count / word_count * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


if __name__ == "__main__":
    main()
