from random import shuffle


def partition_offsets(list_size,partition_count):
    """ Return list of offset indices to obtain partition_count
        many subsets of approx same size """

    modulo = list_size % partition_count
    min_size = list_size // partition_count

    offset = 0
    offsets = [0]
    for i in range(1, partition_count):
        offset += min_size + (i <= modulo)
        offsets.append(offset)

    return offsets


def solution(indices, K):
    # random permutation of indices
    # afford copy to not mutate reference
    indices_random = shuffle(indices.copy())

    offsets = partition_offsets(len(indices), K)
    offsets.append(len(indices))

    #print(offsets)

    folds = []

    for fold_id in range(K):
        train = []
        test = []
        for i,index in enumerate(indices): # i is the index of the index in indices
            if offsets[fold_id] <= i < offsets[fold_id+1]:
                test.append(index)
            else:
                train.append(index)
        folds.append(train)
        folds.append(test)
    return folds

#print(solution(list(range(13)),4))
