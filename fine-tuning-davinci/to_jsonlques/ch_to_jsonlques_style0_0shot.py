import re
import json
import random
import numpy as np


def dict_to_jsonl_0shot(dictionary, file_path):
    '''converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            json_data = {'prompt': "ANSWER KEY:" + str(value[1]) + " Q: " + key + " A: ", 'completion': str(value[0])}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

def dict_to_jsonl_1shot(dictionary, example_lines, file_path, file_text):
    '''converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            formatted_example_line = create_shot_examples(random.choice(example_lines), value[2], file_text)
            json_data = {'prompt': formatted_example_line + " ANSWER KEY:" + str(value[1]) + " Q: " + key + " A: ", 'completion': str(value[0])}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

def create_shot_examples(example_line, whole_or_partial, file_text):
    output_dict = {"NONE":"NONE"}
    if whole_or_partial == "w":
        output_dict = whole_word_replacement(example_line.rstrip("\n"), file_text)
    else:
        output_dict = suffix_replacement(example_line.rstrip("\n"))    
        if not output_dict:
            output_dict = whole_word_replacement(example_line.rstrip("\n"), file_text)
    
    dict_key = str(list(output_dict.keys())[0])

    return "ANSWER KEY:" + str(output_dict[dict_key][1]) + " Q: " + dict_key + " A: " +  str(output_dict[dict_key][0])

def create_word_bank(file_text, num):
    '''creates a list of num random words from file_text'''
    words = re.findall(r'\b\w+\b', file_text)
    random_words = random.sample(words, num)
    return random_words


def whole_word_replacement(input_string, file_text):
    '''takes in one line of the file, outputs a dictionary with the following format for every word in the line:
    key: the line with one word replaced with a tidle
    value: the replaced word'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}
    print(words)

    for word in words:
        word_bank = create_word_bank(file_text, 9)
        word_bank.append(word)
        random.shuffle(word_bank)
        
        replaced_sentence = re.sub(r'\b' + word + r'\b', "~", input_string, count=1)  # Replace only the first occurrence of the current word with a tilde (~)
        word_dictionary[replaced_sentence] = [word, word_bank, "w"]
    
    print(word_dictionary)
    return word_dictionary

def suffix_replacement(input_string):
    '''takes in one line of the file, 
    outputs a dictionary with the following format for every word in the line with a common latin suffix:
    key: the line with the word ending replaced with a tidle
    value: the common suffix'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}

    # suffixes in ch1-3
    latin_suffixes = ['um', 'sunt', 'ae', 'ārum', 'us', 'drum', 'est', 'a', 'ī']
                    
    for word in words:
        for suffix in latin_suffixes:
            if word.endswith(suffix):
                replaced_sentence = re.sub(r'\b' + word + r'\b', word[:-len(suffix)] + '~', input_string, count=1)  # Replace the suffix with a tilde (~) only once
                word_dictionary[replaced_sentence] = [suffix, latin_suffixes, "r"]
                break

    return word_dictionary


output_dict = {}
filename = "ch1-3.txt"

with open(filename, "r") as file:
    file_text = file.read()

with open(filename, "r") as file:
    # split the file randomly in half
    # for line in 1 half, for line in second half, 
    lines = file.readlines()
    #example_lines, eval_lines = np.array_split(lines, 2)
    #example_lines = [item for item in example_lines if re.search('[a-zA-Z]', item)]
    random.shuffle(lines)
    # for eval_line in eval_lines:
    for eval_line in lines:
        if not eval_line.startswith("#"):
            output_dict.update(whole_word_replacement(eval_line.rstrip("\n"), file_text))
            output_dict.update(suffix_replacement(eval_line.rstrip("\n")))


dict_to_jsonl_0shot(output_dict, "ch1-3_lesstoken_0shot.jsonl")