import random
import string


def shuffle_from_dict(d):
    dict_list = list(d.items())
    random.shuffle(dict_list)
    return dict(dict_list)


def escape(word, sentence):
    sentence_lower = sentence.lower()
    word = word.lower()
    if ' ' in word:
        word = word.split(' ')

    new_sentence = ''
    for index, word_sentence in enumerate(sentence_lower.split(' ')):
        new_word = sentence.split(' ')[index]
        word_sentence = word_sentence.translate(str.maketrans('', '', string.punctuation))
        if isinstance(word, list):
            for word_part in word:
                if word_part == word_sentence:
                    replaced_string = ''.join(['_' for n in range(len(word_part))])
                    new_word = replaced_string
        else:
            replaced_string = ''.join(['_' for n in range(len(word))])
            if word == word_sentence:
                new_word = replaced_string
        new_sentence += new_word
        new_sentence += ' '
    return new_sentence
