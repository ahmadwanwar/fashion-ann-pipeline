"""Build and train the ANN using hyperparameters from params.yaml."""
import csv
from pathlib import Path

import numpy as np
import tensorflow as tf
import yaml
from tensorflow import keras


def main():
    p = yaml.safe_load(open("params.yaml"))["train"]
    tf.keras.utils.set_random_seed(p["seed"])

    d = np.load("data/processed/dataset.npz")

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(p["dense_units"], activation="relu"),
        keras.layers.Dropout(p["dropout_rate"]),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=p["learning_rate"]),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    history = model.fit(
        d["x_train"], d["y_train"],
        validation_data=(d["x_val"], d["y_val"]),
        epochs=p["epochs"],
        batch_size=p["batch_size"],
        verbose=2,
    )

    Path("models").mkdir(exist_ok=True)
    model.save("models/model.h5")

    keys = list(history.history)
    with open("models/history.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["epoch"] + keys)
        for i in range(len(history.history[keys[0]])):
            w.writerow([i + 1] + [history.history[k][i] for k in keys])


if __name__ == "__main__":
    main()
