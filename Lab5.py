# Importing the required library for visualizations
import matplotlib.pyplot as plt

# Function to get a list of keys sorted by values from a dictionary
def get_sorted_array(d):
    list_d = list(d.items())
    list_d.sort(key=lambda i: i[1])
    return [i[0] for i in list_d]

# Function to count bigrams in a given text and return the most common ones
def count_bigrams(text):
    bigram_count = {}
    for i in range(len(text) - 1):
        if text[i].isalpha() and text[i + 1].isalpha():
            bigram = text[i] + text[i + 1]
            bigram_count[bigram] = bigram_count.get(bigram, 0) + 1

    sorted_bigrams = list(reversed(get_sorted_array(bigram_count)))
    return sorted_bigrams[:11]  # Return the top 11 bigrams

# Function to count trigrams in a given text and return the most common ones
def count_trigrams(text):
    trigram_count = {}
    for i in range(len(text) - 2):
        if text[i].isalpha() and text[i + 1].isalpha() and text[i + 2].isalpha():
            trigram = text[i] + text[i + 1] + text[i + 2]
            trigram_count[trigram] = trigram_count.get(trigram, 0) + 1

    sorted_trigrams = list(reversed(get_sorted_array(trigram_count)))
    return sorted_trigrams[:6]  # Return the top 6 trigrams

# Function to decrypt a text based on letter frequency and manual mappings
def decrypt(text, expected_letter_freq):
    current_letter_freq = {}
    result_text = ''

    # Count the frequency of letters in the given text
    for char in text:
        if char.isalpha():
            current_letter_freq[char] = current_letter_freq.get(char, 0) + 1

    # Convert counts to percentages
    total_letters = sum(current_letter_freq.values())
    for char in current_letter_freq:
        current_letter_freq[char] = (current_letter_freq[char] * 100) / total_letters

    # Get sorted arrays for expected and actual frequencies
    expected_order = list(reversed(get_sorted_array(expected_letter_freq)))
    actual_order = list(reversed(get_sorted_array(current_letter_freq)))

    # Create a mapping of characters from the actual text to the expected order
    char_mapping = {actual_order[i]: expected_order[i] for i in range(len(actual_order))}

    # Decrypt the text using the mapping
    for char in text:
        if char.isalpha():
            result_text += char_mapping.get(char, char)  # Use the mapping or retain the original character
        else:
            result_text += char  # Non-alphabetic characters remain unchanged

    return result_text, char_mapping, current_letter_freq  # Return the decrypted text, mapping, and letter frequency

# Function to visualize results and show key decryption mappings
def show_result(decrypted_text, expected_letter_freq, current_letter_freq, char_mapping):
    print('Decrypted Text:')
    print(decrypted_text)

    # Visualize expected letter frequencies
    plt.bar(expected_letter_freq.keys(), expected_letter_freq.values(), width=0.5, color='g')
    plt.show()

    # Visualize actual letter frequencies after decryption
    current_sorted = get_sorted_array(current_letter_freq)
    plt.bar(current_sorted, [current_letter_freq[c] for c in current_sorted], width=0.5, color='b')
    plt.show()

    # Print the mapping used for decryption
    print('Character Mapping:')
    for key, value in char_mapping.items():
        print(f"{key} -> {value}")

# Test case with simple text and predefined frequencies
english_letter_freq = {
    'E': 12.70,
    'T': 9.06,
    'A': 8.17,
    'O': 7.51,
    'I': 6.97,
    'N': 6.75,
    'S': 6.33,
    'H': 6.09,
    'R': 5.99,
    'D': 4.25,
    'L': 4.03,
    'C': 2.78,
    'U': 2.76,
    'M': 2.41,
    'W': 2.36,
    'F': 2.23,
    'G': 2.02,
    'Y': 1.97,
    'P': 1.93,
    'B': 1.29,
    'V': 0.98,
    'K': 0.77,
    'J': 0.15,
    'X': 0.15,
    'Q': 0.10,
    'Z': 0.07
}

# Read text data from files
rus_text = "example text for decryption"
eng_text = "example english text to lower case"

# Decrypt the Russian text with a given letter frequency
decrypted_text, char_mapping, current_letter_freq = decrypt(rus_text, english_letter_freq)

# Show the result
show_result(decrypted_text, english_letter_freq, current_letter_freq, char_mapping)
