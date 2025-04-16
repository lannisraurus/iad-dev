"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with the RTL-SDR
module.

"""
import numpy as np
from rtlsdr import RtlSdr

# Class
class RTLSDRInterface:
    # Constructor
    def __init__(self, sample_rate=3.2e6, center_freq=1.7e9, gain='auto'):
        # Initialize the RTL-SDR device
        self.sdr = RtlSdr()
        
        # Configure the RTL-SDR device
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.gain = gain

        # Set up the RTL-SDR device with the provided parameters
        self.sdr.sample_rate = self.sample_rate #max 3.2e6
        self.sdr.center_freq = self.center_freq
        self.sdr.gain = self.gain

        return f"RTL-SDR initialized with sample rate {self.sample_rate / 1e6} MHz and frequency {self.center_freq / 1e6} MHz."

    # Capture
    def capture_samples(self, num_samples=4*1024):
        return self.sdr.read_samples(num_samples)

    def calculate_psd(self, samples, nfft=None, fs=None, window='hamming'):
        if nfft is None:
            nfft = len(samples)  # Default to the sample size if nfft is not provided
        if fs is None:
            fs = self.sample_rate  # Default to the sample rate of the RTL-SDR

        # Apply windowing function if specified (e.g., 'hamming', 'hann', etc.)
        if window:
            if window == 'hamming':
                window_func = np.hamming(len(samples))
            elif window == 'hann':
                window_func = np.hanning(len(samples))
            else:
                window_func = np.ones(len(samples))  # No window (no change to samples)
        
            samples = samples * window_func

        # Perform FFT on the samples
        fft_samples = np.fft.fft(samples, n=nfft)

        # Calculate the Power Spectral Density (PSD)
        psd = np.abs(fft_samples) ** 2 / nfft / fs 

        # Get the frequency bin
        freq_bins = np.fft.fftfreq(nfft, d=1/fs)

        # Shift the frequencies by the central frequency
        freq_bins += self.central_freq

        return freq_bins, psd

    def save_samples(fileName):
        numbers = [1, 2, 3.5, 4.75, 100]

        with open(fileName, "w") as f:
            f.write(",".join(str(n) for n in numbers))

    def close(self):
        self.sdr.close()
        return "RTL-SDR device closed."
