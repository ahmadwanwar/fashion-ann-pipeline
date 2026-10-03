"""Normalize pixels to [0, 1], split a validation set, save to data/processed/."""
from pathlib import Path

import numpy as np
import yaml
from sklearn.model_selection import train_test_split


def normalize(x):
    return x.astype("float32") / 255.0


def main():
    params = yaml.safe_load(open("params.yaml"))["preprocess"]
    raw = np.load("data/raw/fashion_mnist.npz")

    x_train = normalize(raw["x_train"])
    x_test = normalize(raw["x_test"])
    x_tr, x_val, y_tr, y_val = train_test_split(
        x_train, raw["y_train"],
        test_size=params["val_size"],
        random_state=params["seed"],
        stratify=raw["y_train"],
    )

    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out / "dataset.npz",
        x_train=x_tr, y_train=y_tr,
        x_val=x_val, y_val=y_val,
        x_test=x_test, y_test=raw["y_test"],
    )
    print(f"train={x_tr.shape}, val={x_val.shape}, test={x_test.shape}")


if __name__ == "__main__":
    main()
