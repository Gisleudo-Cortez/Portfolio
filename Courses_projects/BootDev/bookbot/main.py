def count_chars(text):
    chars_set = set(list(text.lower()))
    char_counts = {item: 0 for item in chars_set}
    # print(char_counts)
    text = list(text.lower())
    for i in text:
        char_counts[i] += 1
    return char_counts


def number_of_words(text):
    return len(text.split())


def sort_dict(char_dict, reverse=True):
    sorted_dict = {
        k: v
        for k, v in sorted(char_dict.items(), key=lambda item: item[1], reverse=reverse)
    }
    return sorted_dict


def print_report(n_words, char_dict):
    print("--- Begin report of books/frankenstein.txt ---")
    print(f"{n_words} words found in the document", end="\n" * 2)

    # loop for alpha character in dictionary
    for k, v in char_dict.items():
        if k.isalpha():
            print(f"The '{k}' character was found {v} times")
        else:
            continue
    print("--- End report ---")


def main():
    with open("books/frankenstein.txt", "r") as f:
        file_contents = f.read()
        # print(file_contents)
        n_words = number_of_words(file_contents)
        # print(n_words)
        # count the frequency of chars
        chars = count_chars(file_contents)
        # print sorted dict
        sorted_dict = sort_dict(chars)
        # print(sorted_dict)
        print_report(n_words, sorted_dict)
        f.close()


main()

