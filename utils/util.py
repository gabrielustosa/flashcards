import string
import difflib
from random import choice, shuffle


def shuffle_from_dict(d):
    dict_list = list(d.items())
    shuffle(dict_list)
    return dict(dict_list)


def escape(word, sentence):
    sentence_lower = sentence.lower()
    word = word.lower().split(' ')

    new_sentence = ''
    for index, word_sentence in enumerate(sentence_lower.split(' ')):
        new_word = sentence.split(' ')[index]
        word_sentence = word_sentence.translate(str.maketrans('', '', string.punctuation))
        for word_part in word:
            if word_part == word_sentence:
                replaced_string = ''.join(['_' for _ in range(len(word_part))])
                new_word = replaced_string
        new_sentence += new_word
        new_sentence += ' '

    close_matches = []
    for word_part in word:
        matches = difflib.get_close_matches(word_part, new_sentence.split(' '), cutoff=0.5)
        close_matches.extend(matches)
    if close_matches:
        for match in close_matches:
            match_str = str(match).lower()
            for word_part in word:
                if match_str.startswith(word_part):
                    replaced_string = ''.join(['_' for _ in range(len(match_str))])
                    new_sentence = new_sentence.replace(str(match), replaced_string)

    return new_sentence


def get_random_objects(query, not_equal, quantity=1):
    pks = query.values_list('pk', flat=True)

    list_ids = []
    for _ in range(quantity):
        random_id = choice(pks)
        while random_id in list_ids or random_id == not_equal:
            random_id = choice(pks)
        list_ids.append(random_id)

    return query.filter(id__in=list_ids)
