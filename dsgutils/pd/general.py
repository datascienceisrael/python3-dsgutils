from collections import Counter
import math


def cosine_list_similarity(list_a, list_b):
    '''
    Get cosine similarity between two lists
     :param list_a: first list to compare
     :param list_b: second list to compare
     :return: cosine similarity between the lists [0, 1]
    '''

    if not isinstance(list_a, list) or not isinstance(list_b, list):
        raise ValueError('Both passed arguments must be of type list')

    counter_a = Counter(list_a)
    counter_b = Counter(list_b)

    terms = set(counter_a).union(counter_b)
    dotprod = sum(counter_a.get(k, 0) * counter_b.get(k, 0) for k in terms)
    mag_a = math.sqrt(sum(counter_a.get(k, 0)**2 for k in terms))
    mag_b = math.sqrt(sum(counter_b.get(k, 0)**2 for k in terms))
    return round(dotprod / (mag_a * mag_b), 2)