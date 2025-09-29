#! .venv/bin/python3
import numpy as np
from scipy import signal, io
import matplotlib.pyplot as plt
import json

# 96 kHz sample rate, 10.42 us sample period
audio_sample_rate = 96_000  # samples per s
output_data_rate = 120 * 1  # 120 symbols per byte per sec
symbol_samples = audio_sample_rate // output_data_rate  # samples per bit
symbol_duration = 1 / audio_sample_rate * symbol_samples
frame = np.arange(0, symbol_duration, 1 / audio_sample_rate)
freq_max = 13_000
freq_min = 8_000
zero_start_freq = freq_max  # hz
zero_end_freq = freq_min
one_start_freq = freq_min
one_end_freq = freq_max
bit_depth = np.int16


def slope_shift_key_modulation(seq: list):
    zero_chirp = signal.chirp(
        t=frame,
        f0=zero_start_freq,
        t1=symbol_duration,
        f1=zero_end_freq,
        method="log",
    )
    one_chirp = signal.chirp(
        t=frame, f0=one_start_freq, t1=symbol_duration, f1=one_end_freq, method="log"
    )
    out = np.zeros(symbol_samples * len(seq))
    outstr = ""

    for i, bit in enumerate(seq):
        if bit:
            chirp = one_chirp
            bit = "1"
        else:
            chirp = zero_chirp
            bit = "0"

        start = (i) * symbol_samples
        end = (i + 1) * symbol_samples
        out[start:end] = chirp
        outstr += bit

    return out, outstr


def modulate(data: list, type: str):
    symbols = []
    if type == "FSK":
        symbols.append(sine_wave(freq_max))
        symbols.append(sine_wave(freq_min))
    elif type == "SSK":
        symbols.append(
            signal.chirp(
                t=frame,
                f0=zero_start_freq,
                t1=symbol_duration,
                f1=zero_end_freq,
                method="log",
            )
        )
        symbols.append(
            signal.chirp(
                t=frame,
                f0=one_start_freq,
                t1=symbol_duration,
                f1=one_end_freq,
                method="log",
            )
        )
    else:
        raise ValueError(f"Unrecognized modulation type: {type}")

    out = np.zeros(symbol_samples * len(seq))
    outstr = ""

    for i, bit in enumerate(seq):
        start = (i) * symbol_samples
        end = (i + 1) * symbol_samples
        out[start:end] = symbols[bit]
        outstr += str(bit)

    return out, outstr


def sine_wave(f, n=symbol_samples, rate=audio_sample_rate, phase_shift=0):
    t = np.arange(n) / rate  # time vector
    return np.sin(2 * np.pi * f * t + phase_shift)


def bytes2bitlist(bytes: int):
    bitlist = []
    for i, byte in enumerate(bytes):
        for j in range(8):
            bit = (byte >> j) & 1
            bitlist.append(bit)
    return bitlist


def goldify(data_bitlist, gold_code_bitlist):
    golded = []
    for d_bit in data_bitlist:
        for g_bit in gold_code_bitlist:
            golded.append(int((bool(d_bit) ^ bool(g_bit))))
    return golded


def plot_spectrum(sig: np.ndarray):
    # Compute the spectrogram
    nperseg = symbol_samples // 8
    noverlap = nperseg // 2
    frequencies, times, Sxx = signal.spectrogram(
        sig, fs=audio_sample_rate, nperseg=nperseg, noverlap=noverlap
    )

    # Convert power spectrogram (Sxx) to dB scale for better visualization
    Sxx_dB = 10 * np.log10(Sxx + 1e-10)  # add a small value to avoid log(0)

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, Sxx_dB, cmap="magma", shading="gouraud")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.title("Spectrogram of the Signal")
    plt.colorbar(label="Intensity [dB]")
    plt.ylim(freq_min * 0.85, freq_max * 1.1)  # limit frequency axis for clarity
    plt.show()


def plot_signal(signal: np.ndarray):
    ylabel = "Amplitude"
    xlabel = "Time"
    plt.figure(figsize=(8, 4))
    plt.plot(signal)
    plt.title("Time-Domain Signal")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def export_wav(sig: np.ndarray):
    io.wavfile.write("signal.wav", audio_sample_rate, sig)


if __name__ == "__main__":
    # goldcodes = None
    with open("goldcodes") as f:
        goldcodes = json.load(f)

    seq = "!".encode("utf-8")
    # seq = "1".encode()
    print(format(int.from_bytes(seq), "b"))
    seq = bytes2bitlist(seq)
    # print(seq)
    seq = goldify(seq, goldcodes[0])
    # print(seq)
    out: np.ndarray
    out, outstr = modulate(seq, "FSK")
    print(f"Data ({len(outstr)}: {outstr}")
    # convert to 16-bit int
    out = out * (2**15 - 1)
    out = out.astype(np.int16)
    print(out[0:20])
    plot_spectrum(out)
    export_wav(out)
