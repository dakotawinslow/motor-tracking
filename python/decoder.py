import numpy as np
from scipy import signal, io, fft
import json
import matplotlib.pyplot as plt
import tone_generator as tg


offset = 0  # number of samples off from perfectly in-phase, for simulating issues


def plot_ft(bins, sig):
    ylabel = "Amplitude"
    xlabel = "Frequency"
    plt.figure(figsize=(8, 4))
    plt.plot(bins, sig)
    plt.title("FFT of Signal")
    plt.xlim(0, 20000)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    pass


def demodulate_FSK(sig: np.ndarray):
    # TODO: Use filtering and a narrower window
    # First, we window the signal by the known transmission key length
    low_peak = None
    high_peak = None
    symbols = []
    for i in range(0, sig.shape[0], tg.symbol_samples):
        # next, we do an fft on the chunk
        window = sig[i : i + tg.symbol_samples]
        sig_ft = fft.fft(window)
        sig_ft = np.abs(sig_ft)[
            : sig_ft.shape[0] // 2
        ]  # take mag and throw out negatives to give us [0,pi]
        top_freq = tg.audio_sample_rate // 2  # Nyquist limit
        if not low_peak:
            low_peak = int((tg.freq_min / top_freq) * sig_ft.shape[0])
            high_peak = int((tg.freq_max / top_freq) * sig_ft.shape[0])
        if sig_ft[low_peak] > sig_ft[high_peak]:
            symbols.append(False)
        else:
            symbols.append(True)
        print(f"Low peak value ({tg.freq_min}hz): {sig_ft[low_peak]}")
        print(f"High peak value ({tg.freq_max}hz): {sig_ft[high_peak]}")
        # amp_low = np.mean(amp_low)
        # print(amp_low)
    symbols = np.array(symbols, np.uint8)
    print(symbols)
    return symbols


def despread(symbols, goldcode):
    PRN = np.array(goldcode, np.uint8)
    # section signal into code-length chunks
    codelen = PRN.shape[0]
    numcodes = symbols.shape[0] // codelen
    for i in range(numcodes):
        section = symbols[i : i + codelen]
        print(f"section: {section}")
        print(f"PRN: {PRN}")
        print(f"PRN ^ section: {PRN ^ section}")


if __name__ == "__main__":
    rate, sig = io.wavfile.read("signal.wav")
    with open("goldcodes") as f:
        goldcodes = json.load(f)
    symbols = demodulate_FSK(sig)
    despread(symbols, goldcodes[0])
