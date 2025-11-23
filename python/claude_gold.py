import numpy as np
from scipy import signal
import json


def gen_gold(seq1, seq2, only_balanced=False):
    """Function to produce a gold sequence based on two input preferred pair Maximal Length Sequences."""
    gold = [
        seq1,
        seq2,
    ]  # Initial gold code with seq1 and seq2
    for shift in range(0, len(seq1)):
        gold.append(np.logical_xor(seq1, np.roll(seq2, shift)))
    if only_balanced:
        bal = []
        for code in gold:
            ones = np.count_nonzero(code)
            if ones * 2 + 1 == len(code) or ones * 2 - 1 == len(code):
                bal.append(code)
        gold = bal
    return np.where(gold, 1, 0)


# seq1 = np.random.choice([0, 1], size=6)  # Random binary sequence
# seq2 = np.random.choice([0, 1], size=6)
seq1 = [0, 0, 0, 0, 0, 1]
seq2 = [0, 0, 0, 0, 0, 1]

poly1 = [6, 5, 2, 1]
poly2 = [6, 1]

mseq1 = np.array(signal.max_len_seq(6, state=seq1, taps=[poly1])[0])
mseq2 = np.array(signal.max_len_seq(6, state=seq2, taps=[poly2])[0])

golds = gen_gold(mseq1, mseq2, only_balanced=True)
print(len(golds))
golds = golds.tolist()
with open("goldcodes6", "w") as f:
    json.dump(golds, f)
    # s = json.dumps(golds).replace(",", "").replace("] [", "]\n[")
    # f.write(s)
