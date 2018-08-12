from string import ascii_letters as letters
lower_case_letters = letters[:26]

def is_only_letters(word):

    for letter in word:
        if letter not in letters:
            return False
    return True


def has_no_duplicate_letter(word):
    word = list(word)
    bool = len(word) == len(set(word))
    return bool


def does_not_end_with_s(word):
    bool = word[-1] != 's'
    return bool


def word_to_list_of_bools(word):
    letter_list = list(word)
    bool_list = [1 if letter in letter_list else 0 for letter in lower_case_letters]
    return bool_list
