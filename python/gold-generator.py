import json

# Step 1: Generate some m-sequences
primative_polys = {2: [2, 1], 3: [3, 1], 4: [4, 1], 5: [5, 3]}


def generate_m_seq(seed):
    reg = seed.copy()
    seq = []
    m = len(seed)
    try:
        taps = primative_polys[m]
    except IndexError:
        raise IndexError(
            f"There is no primitive polynomial set for sequences of length {m}"
        )

    for _ in range(2**m - 1):
        output = reg[-1]
        seq.append(output)
        feedback = 0
        for t in taps:
            feedback ^= reg[m - t]

        reg = [feedback] + reg[:-1]
    return seq


def cyclic_shift(seq, n=1):
    return seq[-n:] + seq[:-n]


if __name__ == "__main__":
    num_sequences = 2
    m = 4
    m_seqs = []
    for i in range(num_sequences):
        seed = []
        for j in range(m):
            bits = i + 1
            bits = bits >> j
            seed.append(bits & 1)
        print(seed)
        m_seqs.append(generate_m_seq(seed))

    golds = []
    for d in range(len(m_seqs[0])):
        A = m_seqs[0]
        B = cyclic_shift(m_seqs[1], d)
        gold = [a ^ b for a, b in zip(A, B)]
        golds.append(gold)
    print(golds)
    with open("goldcodes", "w") as f:
        json.dump(golds, f)
