import string
import re
import unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

def clean_punctuation(s, punc_to_keep=[]):
    """
   Strip string of punctuation
    :param s: a string to strip of punctuation
    :param punc_to_keep: a set with all the punctuation marks to keep as a string, with no spaces e.g. {$#}
    :return: a string stripped of punctuation
    """

    if not isinstance(s, str):
        raise ValueError('The value passed is not a string')

    PUNCT = re.compile('[%s]' % re.escape("".join(set(string.punctuation) - set(punc_to_keep))))
    return re.sub('\s+', ' ', PUNCT.sub('', s)).strip()

def remove_non_ascii(word):
    """
    Remove non-ASCII characters from list of tokenized words
    :param word: a word to clean
    :return: the original word with only ascii characters
    """
    if not isinstance(word, str):
        raise ValueError('The value passed is not a string')

    return unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')


def unite_standalone_uppercase(str_to_fix):
    """
    Unite single capital letters on a row, to one word. e.g.: U S A -> USA
    :param str_to_fix: word to examine and fix
    :return: new string with united single capital letters
    """

    if not isinstance(str_to_fix, str):
        raise ValueError('The value passed is not a string')

    str_split = str_to_fix.split()
    new_str = ""
    for i, word in enumerate(str_split):
        if (len(word) == 1) and (i+1 < len(str_split)) and (len(str_split[i+1]) == 1) and (word.isupper()) \
                                                                                        and (str_split[i+1].isupper()):
            new_str += word

        else:
            new_str = new_str + word + " "

    return new_str.strip()


def camel_case_split(str_to_split):
    """
    Seperate camel case words to two single words
    :param str_to_split: word to seperate
    :return: new string with split camel case words
    """
    if not isinstance(str_to_split, str):
        raise ValueError('The value passed is not a string')

    str_to_split = str_to_split.replace('-', ' ')
    remove_digits = str.maketrans('', '', string.digits)

    str_to_split = str_to_split.translate(remove_digits)

    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', str_to_split)

    return " ".join([m.group(0) for m in matches])


def lemmatize_word(word, pos):
    """
    Lemmatize word according to the given POS tag
    :param word: a word to lemmatize
    :param pos: part of speech tag: 's' / 'a' / 'r' / 'v' / 'n' / 'adverb'
    :return: the lemmatized word
    """

    if not isinstance(word, str):
        raise ValueError('The value passed is not a string')

    if not isinstance(pos, str) or pos not in ['s', 'a', 'r', 'v', 'n', 'adverb']:
        raise ValueError('Please enter a valid part of speach out of the following options: s, a, r, v, n, adverb')

    if pos == "adverb":
        return wn.synset(word + ".r.1").lemmas()[0].pertainyms()[0].name()

    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word, pos = pos)


def normalize_word(word, from_pos, to_pos):
    """
    Transform the given word from/to POS tags
    :param word: word to normalize
    :param from_pos: Part of speach the word is in
    :param to_pos: part of speech to convert to
    :return: normalized word
    """

    if not isinstance(word, str):
        raise ValueError('The value passed is not a string')

    if not isinstance(from_pos, str) or from_pos not in ['s', 'a', 'r', 'v', 'n', 'adverb']:
        raise ValueError('Please enter a valid from_pos part of speach out of the following options: s, a, r, v, n, adverb')

    if not isinstance(to_pos, str) or to_pos not in ['s', 'a', 'r', 'v', 'n', 'adverb']:
        raise ValueError('Please enter a valid to_pos part of speach out of the following options: s, a, r, v, n, adverb')

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in ('a', 's') and \
                    s.name().split('.')[1] in ('a', 's'):
                lemmas += [l]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in ('a', 's') and \
                    l.synset().name().split('.')[1] in ('a', 's'):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])

    # return all the possibilities sorted by probability
    return result[0][0]
