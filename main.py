import numpy as np
import matplotlib.pyplot as plt

def main():
    x: np.ndarray = np.arange(0, 5*np.pi, 0.1)
    y: np.ndarray = np.sin(x)

    plt.plot(x, y)
    plt.show()

if __name__ == '__main__':
    main()