import numpy as np
from scipy import signal, io, fft
import matplotlib.pyplot as plt
import tone_generator as tg

offset = 0  # number of samples off from perfectly in-phase, for simulating issues


def plot_ft(sig):
    ylabel = "Amplitude"
    xlabel = "Frequency"
    plt.figure(figsize=(8, 4))
    plt.plot(signal)
    plt.title("FFT of Signal")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    pass


def demodulate_FSK(sig: np.ndarray):
    # TODO: Use filtering and a narrower window
    # First, we window the signal by the known transmission key length
    for i in range(0, sig.shape[0], tg.symbol_samples):
        # next, we do an fft on the chunk
        sig_ft = fft.fft(sig[i : i + tg.symbol_samples])
        plot_ft(sig_ft[0:20000])
        break


if __name__ == "__main__":
    rate, sig = io.wavfile.read("signal.wav")
    demodulate_FSK(sig)
