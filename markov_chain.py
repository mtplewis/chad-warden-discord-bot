import pandas as pd
import responses
import random
from numpy.random import choice


def letters(input):

    valids = []
    for character in input:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)


def make_a_sentence(start, input, strip_emojis=False):
    words = responses.get_words(input, strip_emojis)

    dict_df = pd.DataFrame(columns=['lead', 'follow', 'freq'])
    dict_df['lead'] = words
    follow = words[1:]
    follow.append('EndWord')
    dict_df['follow'] = follow

    end_words = responses.get_end_words(input, strip_emojis)

    dict_df['freq'] = dict_df.groupby(by=['lead', 'follow'])['lead', 'follow'].transform('count').copy()

    dict_df = dict_df.drop_duplicates()
    pivot_df = dict_df.pivot(index='lead', columns='follow', values='freq')

    sum_words = pivot_df.sum(axis=1)
    pivot_df = pivot_df.apply(lambda x: x / sum_words)
    desired_length = random.choice(range(3, 8))

    word = start
    sentence = [word]
    while len(sentence) < desired_length:
        next_word = choice(a=list(pivot_df.columns), p=pivot_df.iloc[pivot_df.index == word].fillna(0).values[0])
        if next_word in end_words and next_word != 'EndWord':
            try_word = choice(a=list(pivot_df.columns), p=pivot_df.iloc[pivot_df.index == word].fillna(0).values[0])
            next_word = choice(a=list(pivot_df.columns), p=pivot_df.iloc[pivot_df.index == word].fillna(0).values[0])
            if try_word == next_word:
                sentence.append(next_word)
                break
            if len(sentence) == desired_length:
                sentence.append(next_word)
                break
            else:
                continue
        else:
            sentence.append(next_word)
        word = next_word
    check = all(item in sentence for item in end_words)
    if not check:
        sentence.append(random.choice(end_words))
    sentence = ' '.join(sentence)

    return sentence
