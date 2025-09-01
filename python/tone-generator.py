#! .venv/bin/python3
import numpy as np
from scipy import signal, io
import matplotlib.pyplot as plt

# 96 kHz sample rate, 10.42 us sample period
audio_sample_rate = 96_000  # samples per s
output_data_rate = 100  # bits per s
chirp_samples = audio_sample_rate // output_data_rate  # samples per bit
chirp_duration = 1 / audio_sample_rate * chirp_samples
frame = np.arange(0, chirp_duration, 1 / audio_sample_rate)
freq_max = 13_000
freq_min = 8_000
zero_start_freq = freq_max  # hz
zero_end_freq = freq_min
one_start_freq = freq_min
one_end_freq = freq_max


def chirpify(seq: int):
    zero_chirp = signal.chirp(
        t=frame,
        f0=zero_start_freq,
        t1=chirp_duration,
        f1=zero_end_freq,
        method="log",
    )
    one_chirp = signal.chirp(
        t=frame, f0=one_start_freq, t1=chirp_duration, f1=one_end_freq, method="log"
    )
    out = np.zeros(chirp_samples * len(seq) * 8)
    outstr = ""

    for i, byte in enumerate(seq):
        for j in range(8):
            if (byte >> j) & 1 == 0:
                chirp = zero_chirp
                bit = "0"
            else:
                chirp = one_chirp
                bit = "1"
            start = ((i * 8) + j) * chirp_samples
            end = ((i * 8) + j + 1) * chirp_samples
            out[start:end] = chirp
            outstr += bit
            # if j > 0:
            #     break

    return out, outstr


def plot_signal(sig: np.ndarray):
    # Compute the spectrogram
    nperseg = chirp_samples // 8
    noverlap = nperseg // 2
    frequencies, times, Sxx = signal.spectrogram(
        sig, fs=audio_sample_rate, nperseg=nperseg, noverlap=noverlap
    )

    # Convert power spectrogram (Sxx) to dB scale for better visualization
    Sxx_dB = 10 * np.log10(Sxx + 1e-10)  # add a small value to avoid log(0)

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, Sxx_dB, shading="gouraud")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.title("Spectrogram of the Signal")
    plt.colorbar(label="Intensity [dB]")
    plt.ylim(freq_min * 0.85, freq_max * 1.1)  # limit frequency axis for clarity
    plt.show()


def export_wav(sig: np.ndarray):
    io.wavfile.write("signal.wav", audio_sample_rate, sig)


if __name__ == "__main__":
    seq = "Hello World!".encode("utf-8")
    # seq = "1".encode()
    print(len(seq))
    out, outstr = chirpify(seq)
    print(outstr)
    # plot_signal(out)
    export_wav(out)
