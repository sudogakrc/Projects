#Question 1

def word_frequencies(given_string):
    new_string = given_string.lower().strip().replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace("'", "").split(" ")
    WordCount = {}
    for word in new_string:
        if WordCount.get(word) == None:
            WordCount[word] = 0
        WordCount[word] = WordCount.get(word) + 1
    print(WordCount)
    
#Question 2

def print_top_freqs(name_dict, k):
    sorted_dict = sorted(name_dict, key=name_dict.get, reverse=True)
    keys = list(sorted_dict.keys())[:k]
    values = list(sorted_dict.values())[:k]
    for i in range(len(values)):
        if values[i] > 1:
            print("There are " + str(values[i]) + "copies of \"" + str(keys[i]) + "\"")
        else:
            print("There is " + str(values[i]) + "copy of \"" + str(keys[i]) + "\"")
            
#Question 3

Alphabet = "abcdefghijklmnopqrstuvwxyz"
def is_pangram(given_string):
    given_string = given_string.lower()
    given_string = given_string.replace(" ", "")
    count_letters = 0
    for letter in Alphabet:
        if letter in given_string:
            count_letters += 1
    if count_letters == 26:
        return True
    else:
        return False
        
def missing_letters(given_string):
    given_string = given_string.upper()
    given_string = given_string.replace(" ", "")
    Up_Alphabet = Alphabet.upper()
    missing = set()
    for letter in Up_Alphabet:
        if letter not in given_string:
            missing.add(letter)
    return missing
    
#Question 4

def freq_strings(name_dict):
    list_dict = name_dict.items()
    str_list = [str(element) for element in list_dict]
    return str_list
    
def words_longer_than(given_string, n):
    new_dict = word_frequencies(given_string)
    keys = list(new_dict.keys())
    str_key = [str(x) for x in keys]
    longer_words = [words for words in str_keys if len(words) > n]
    return longer_words
    
#Question 5

def most_common_word(name_dict):
    sorted_dict = sorted(name_dict, key=name_dict.get, reverse=True)
    sorted_list = sorted_dict.items()
    if sorted_list[0][1] == sorted_list[1][1]:
        print("None")
    else:
        print(str(sorted_list[0][0]))


            
    

