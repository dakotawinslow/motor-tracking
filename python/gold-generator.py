import json
import polars as pl

# Step 1: Generate some m-sequences
primative_polys = {2: [2, 1], 3: [3, 1], 4: [4, 1], 5: [5, 3], 6: [6, 2]}


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
    num_sequences = 64
    m = 6
    m_seqs = []
    for i in range(num_sequences):
        seed = []
        for j in range(m):
            bits = i + 1
            bits = bits >> j
            seed.append(bits & 1)
        # print(seed)
        m_seqs.append(generate_m_seq(seed))

    golds = []
    for d in range(len(m_seqs[0])):
        A = m_seqs[0]
        B = cyclic_shift(m_seqs[1], d)
        gold = [a ^ b for a, b in zip(A, B)]
        golds.append(gold)
    max_corrs = []
    complete = []
    for i, A in enumerate(golds):
        # complete.append(i)
        for j, B in enumerate(golds):
            if j == i:
                continue
            max_corr = 0
            for k in range(len(A)):
                cross = [(a - 0.5) * (b - 0.5) for a, b in zip(A, cyclic_shift(B, k))]
                corr = sum(cross)
                if corr > max_corr:
                    max_corr = corr
            max_corrs.append((max_corr, i, j))
    max_corrs = pl.DataFrame(max_corrs, schema=["score", "i", "j"])
    max_corrs = max_corrs.group_by("i").agg(pl.col("score").sum())
    best = max_corrs.sort("score").head(16)
    for i in best["i"]:
        print(i)
        print(golds[int(i)])
        print("")

    with open("goldcodes63", "w") as f:
        json.dump(golds, f)
