import numpy as np
from rtlsdr import RtlSdr
import pyqtgraph

class RTLSDRInterface:
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

def calculate_plot_psd(self, num_samples=4*1024, nfft=None, window='hamming', graphWindow=None):
    # Capture the samples from RTL-SDR
    samples = self.capture_samples(num_samples)
    
    # Calculate the PSD
    freq_bins, psd = self.calculate_psd(samples, nfft=nfft, window=window)

    # Plot the PSD
    graphWindow.plot_graph(freq_bins, 10 * np.log10(psd), pen='g')  # Convert PSD to dB for visualization
    return freq_bins, psd

def close(self):
    self.sdr.close()
    return "RTL-SDR device closed."
