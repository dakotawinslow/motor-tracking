# the goal of this script is to identify a set of codes that have low correlation with eachother at any cyclic rotation
import json
import numpy as np
import tqdm
import itertools

with open("goldcodes6") as f:
    codes = json.load(f)


def corr_sequences(a, b):
    a = np.array(a)
    b = np.array(b)
    a = 2 * a - 1
    b = 2 * b - 1
    c = a * b
    return int(np.absolute(c.sum()))


# First, we pick a single code
correlations = np.empty((len(codes), len(codes), 2), np.uint)
for i, code in tqdm.tqdm(enumerate(codes)):
    # and we go through all the other codes in the set
    for j, challenge in enumerate(codes):
        rot_corrs = np.empty(63)
        for k in range(63):
            rotated = challenge[k:] + challenge[:k]
            cor = corr_sequences(code, rotated)
            rot_corrs[k] = cor
        correlations[i][j][0] = rot_corrs.sum() ** 2
        if i == j:
            correlations[i][j][1] = 0
        else:
            correlations[i][j][1] = rot_corrs.max()


def search_for_sets(set_size):
    sets = []
    for subset in itertools.combinations(range(len(codes)), set_size):
        sets.append(subset)
    sets = np.array(sets)
    total_corrs = np.zeros(len(sets))
    max_corrs = np.zeros(len(sets))
    for i in tqdm.tqdm(range(len(sets))):
        for a, b in itertools.combinations(sets[i], 2):
            total_corrs[i] += correlations[a][b][0]
            if correlations[a][b][1] > max_corrs[i]:
                max_corrs[i] = correlations[a][b][1]

    mindex_corrs = np.argmin(total_corrs)
    mindex_maxes = np.argmin(max_corrs)
    print(f"Mean total correlation: {total_corrs.mean()}")
    print(
        f"Best set by lowest totals: {sets[mindex_corrs]}, with total correlation {total_corrs[mindex_corrs]}"
    )
    print(f"Mean max fluke correlation: {max_corrs.mean()}")
    print(
        f"Best set by max fluke correlation: {sets[mindex_corrs]}, with max fluke correlation {max_corrs[mindex_maxes]}"
    )
    print("\nCodes:")
    codeset = sets[mindex_corrs]
    count = 1
    for i in codeset:
        print(f"PRN{count} = {codes[i].__str__().replace(",", "")};")
        count += 1


print("*** BEST SET OF 4 ***")
search_for_sets(4)
# print("*** BEST SET OF 8 ***")
# search_for_sets(8)
# print("*** BEST SET OF 12 ***")
# search_for_sets(12)
# print("*** BEST SET OF 16 ***")
# search_for_sets(16)
