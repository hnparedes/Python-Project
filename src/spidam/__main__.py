def main():
    # Import necessary libraries
    import numpy as np
    import matplotlib.pyplot as plt

    # Define the parameters for the sine wave
    frequency_modifier = 2  # Frequency modifier for the sine wave
    time_values = np.arange(0, 5 * np.pi, 0.1)  # Time values from 0 to 5π
    sine_wave = np.sin(frequency_modifier * time_values)  # Generate the sine wave

    # Plot the sine wave
    plt.plot(time_values, sine_wave)
    plt.title('Modified Sine Wave')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
