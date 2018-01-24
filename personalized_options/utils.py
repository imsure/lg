from random import random
import json


def unique_place_id():
    place_id = 1
    while True:
        yield place_id
        place_id += 1


def probability_list(ret_format=None):
    rand_data = []
    for i in range(0, 96):
        rand_data.append(random() * 100)
    total = sum(rand_data)

    probabilities = [100 * p / total for p in rand_data]
    if ret_format == 'str':
        probabilities = ['{:.2f}'.format(p) for p in probabilities]
        return ','.join(probabilities)
    return probabilities


if __name__ == '__main__':
    place_id_seq = unique_place_id()
    print(next(place_id_seq))
    print(next(place_id_seq))
    print(next(place_id_seq))
    print(next(place_id_seq))

    prob_list = probability_list(ret_format='str')
    print(prob_list)
    prob_list = [float(p) for p in prob_list.split(',')]
    print(sum(prob_list))
    print(len(prob_list))

    prob_list = probability_list()
    print(prob_list)
