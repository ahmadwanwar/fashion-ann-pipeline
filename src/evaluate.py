"""Evaluate the trained model on the test set; write metrics.json and a confusion matrix."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from tensorflow import keras

CLASSES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
           "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def main():
    d = np.load("data/processed/dataset.npz")
    model = keras.models.load_model("models/model.h5")

    loss, acc = model.evaluate(d["x_test"], d["y_test"], verbose=0)
    pred = model.predict(d["x_test"], verbose=0).argmax(axis=1)

    Path("reports").mkdir(exist_ok=True)
    cm = confusion_matrix(d["y_test"], pred)
    fig, ax = plt.subplots(figsize=(8, 8))
    ConfusionMatrixDisplay(cm, display_labels=CLASSES).plot(ax=ax, xticks_rotation=45, colorbar=False)
    fig.tight_layout()
    fig.savefig("reports/confusion_matrix.png", dpi=120)

    with open("metrics.json", "w") as f:
        json.dump({"test_loss": float(loss), "test_accuracy": float(acc)}, f, indent=2)
    print(f"test_loss={loss:.4f} test_accuracy={acc:.4f}")


if __name__ == "__main__":
    main()
