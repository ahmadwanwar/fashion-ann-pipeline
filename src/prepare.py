"""Download Fashion-MNIST and save the raw arrays to data/raw/."""
from pathlib import Path

import numpy as np
from tensorflow import keras


def main():
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    out = Path("data/raw")
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out / "fashion_mnist.npz",
        x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test,
    )
    print(f"saved raw data: train={x_train.shape}, test={x_test.shape}")


if __name__ == "__main__":
    main()
