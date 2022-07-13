import random


def sample_from_dict(d, sample=10):
    keys = random.sample(list(d), sample)
    values = [d[k] for k in keys]
    return dict(zip(keys, values))


def shuffle_from_dict(d):
    dict_list = list(d.items())
    random.shuffle(dict_list)
    return dict(dict_list)
