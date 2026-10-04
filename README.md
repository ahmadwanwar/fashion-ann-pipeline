# Fashion-MNIST ANN Pipeline

Fashion-MNIST classifier with Git + DVC.

Fully-connected ANN (Flatten, Dense ReLU, Dropout, Dense softmax) trained on
Fashion-MNIST. Data and models are versioned with DVC and stored on Google Drive.

## Run

    pip install -r requirements.txt
    dvc pull
    dvc repro
