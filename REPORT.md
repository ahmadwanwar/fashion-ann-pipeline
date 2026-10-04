# Assignment 2: End-to-End ML Versioning with Git, DVC & Google Drive

- **Repository**: [https://github.com/ahmadwanwar/fashion-ann-pipeline](https://github.com/ahmadwanwar/fashion-ann-pipeline)
- **Google Drive DVC Remote**: [https://drive.google.com/drive/u/0/folders/17EtYjREVF_82cgP-8tMB-9mM2WSYK_aP](https://drive.google.com/drive/u/0/folders/17EtYjREVF_82cgP-8tMB-9mM2WSYK_aP)
- **Author**: Muhammad Ahmad Waqar (`ahmadwaqaranwar@gmail.com`)

---

## Part A: Git Fundamentals & Advanced Commands

### A1. Initialization and Initial Commit
- **Branch**: `main`
- Initial commit created with `README.md` and `.gitignore` (ignoring `.venv/`, `__pycache__/`, `.dvc/cache`, `.dvc/tmp`, `.dvc/config.local`, `*.h5`, and data/model payloads).

### A2. Feature Development on `dev` Branch
- Switched to `dev` branch with `git checkout -b dev`.
- 6+ incremental commits covering pipeline scripts, configs, requirements, and scratch notes.

### A3. Log Variants & Analysis
| Command | Output / Screenshot Evidence | Explanation / What it reveals |
|---|---|---|
| `git log --oneline --graph --all` | Displays complete ASCII branch topology and merge graph across all branches | Shows branch branching/merging points, diverging commit paths, and current branch pointers in a compact single-line view. |
| `git log --stat -3` | Lists modified files with insertion/deletion counts for the last 3 commits | Shows file-level impact and volume of changes for recent commits without displaying full diff patches. |
| `git log -p -1` | Displays full unified diff patch of the most recent commit | Shows the exact line-by-line additions and deletions made in the latest commit. |
| `git log main..dev` | Lists commits present on `dev` that have not yet been merged into `main` | Useful for reviewing pending feature branch commits prior to creating pull requests or merging into production. |

```text
$ git log --oneline --graph --all
* e4cb8fc Update dvc.lock after merge
*   948ec7d Merge teammate-sim into main (keep per-image min-max)
|\  
| * 8ea097c teammate: standardize pixels with mean/std
* | 1723835 main: per-image min-max normalization
|/  
* ecee5ca v2: dense_units 256
* e2033fc v1: first pipeline run (dvc.lock, metrics)
* 07254c9 Add dvc.yaml pipeline
* 6b5226a Hand artifact tracking over to dvc.yaml pipeline
* 67f112c Track data and model with DVC (v0 artifacts)
* 52dfb5d Configure Google Drive DVC remote
* be6ac21 Initialize DVC
* da623bd Remove obsolete scratch notes
* bd7dab6 Move prepare.py into src/
* d1d3224 Expand README description
* 1e7f964 Add scratch notes (to be removed later)
* 3f93ea3 Add requirements
* 623aaa7 Add evaluate script
* 66a7031 Add train script
* e7d4bd8 Add params.yaml
* a684888 Add preprocess script
* bfc727a Add prepare script (Fashion-MNIST download)
* c94c2e1 Fix README typo
* 8f4e35c Initial commit: add README and gitignore
```

### A4. Diff Variants
- `git diff`: Unstaged working directory modifications.
- `git diff --staged`: Changes staged in the index ready for the next commit.
- **Two-dot vs Three-dot**:
  - `git diff main..dev`: Compares the direct tips of `main` and `dev`. Any new changes on `main` show up inverted.
  - `git diff main...dev`: Compares `dev`'s tip to the merge-base (common ancestor) between `main` and `dev`, showing strictly what `dev` introduced.

### A5. Git Stash Workflow
- Stashed mid-edit changes on `src/preprocess.py` using `git stash`.
- Checked status and inspected `git stash list`.
- Switched to `main`, returned to `dev`, and restored working state with `git stash pop`.

### A6. Rebase Scenario
- Created `hotfix` branch off `main`, fixed README typo (`c94c2e1`), and fast-forward merged to `main`.
- Rebased `dev` on `main` with `git rebase main`. Resolved README conflict by preserving the updated description, ensuring clean linear history.

### A7. Soft vs Hard Reset
- Made 2 scratch commits on `scratch` branch.
- `git reset --soft HEAD~1`: HEAD moved backwards, but modifications remained staged in index and working tree.
- `git reset --hard HEAD~1`: HEAD moved backwards, and modifications were completely discarded from both index and disk.

### A8. History-Preserving Reorganization
- Relocated root script with `git mv prepare.py src/prepare.py`.
- Deleted temporary notes with `git rm scratch_notes.txt`.
- Tracked both operations as distinct Git history events.

---

## Part B: Modular TensorFlow ANN Pipeline

1. **`src/prepare.py`**:
   Loads the Fashion-MNIST dataset directly from `tf.keras.datasets.fashion_mnist.load_data()` (60,000 train, 10,000 test images at 28x28 grayscale) and compresses them into `data/raw/fashion_mnist.npz`.
2. **`src/preprocess.py`**:
   Loads raw arrays, applies per-image min-max scaling into $[0, 1]$, and uses `sklearn.model_selection.train_test_split` (stratified by label) to split training data into 54,000 train samples and 6,000 validation samples. Saves output to `data/processed/dataset.npz`.
3. **`src/train.py`**:
   Reads hyperparameters (`dense_units`, `dropout_rate`, `learning_rate`, `epochs`, `batch_size`, `seed`) from `params.yaml`. Constructs a Sequential ANN (`Flatten -> Dense(ReLU) -> Dropout -> Dense(10, Softmax)`), compiles with Adam and `sparse_categorical_crossentropy`, trains on processed data, and saves `models/model.h5` and `models/history.csv`.
4. **`src/evaluate.py`**:
   Evaluates the saved model on the unseen test set, generates a confusion matrix saved as `reports/confusion_matrix.png`, and outputs test accuracy and loss into `metrics.json`.

---

## Part C: DVC Setup with Google Drive Remote

- **Remote URL**: `gdrive://17EtYjREVF_82cgP-8tMB-9mM2WSYK_aP`
- **Remote Name**: `gdrive_storage` (default remote)
- **OAuth Authentication**: Completed using Google Cloud Desktop Client credentials.
- **Security & Credential Exclusion Verification**:
  ```text
  $ git check-ignore -v .dvc/config.local .dvc/tmp/gdrive-user-credentials.json
  .gitignore:7:.dvc/config.local    .dvc/config.local
  .gitignore:6:.dvc/tmp             .dvc/tmp/gdrive-user-credentials.json

  $ git ls-files | Select-String -Pattern "credential|config.local"
  (No output - credentials and tokens are strictly excluded)
  ```
- **Real Artifact Push**: Hashed payload files physically pushed to Google Drive remote.

---

## Part D: DVC Pipeline (`dvc.yaml` + `params.yaml`)

### Final `params.yaml`
```yaml
preprocess:
  val_size: 0.1
  seed: 42

train:
  dense_units: 256
  dropout_rate: 0.2
  learning_rate: 0.001
  epochs: 10
  batch_size: 64
  seed: 42
```

### Final `dvc.yaml`
```yaml
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
      - src/prepare.py
    outs:
      - data/raw

  preprocess:
    cmd: python src/preprocess.py
    deps:
      - src/preprocess.py
      - data/raw
    params:
      - preprocess.val_size
      - preprocess.seed
    outs:
      - data/processed

  train:
    cmd: python src/train.py
    deps:
      - src/train.py
      - data/processed
    params:
      - train.dense_units
      - train.dropout_rate
      - train.learning_rate
      - train.epochs
      - train.batch_size
      - train.seed
    outs:
      - models/model.h5
      - models/history.csv

  evaluate:
    cmd: python src/evaluate.py
    deps:
      - src/evaluate.py
      - models/model.h5
      - data/processed
    outs:
      - reports/confusion_matrix.png
    metrics:
      - metrics.json:
          cache: false
```

### D3 vs D4 Execution Analysis
- **D3 (`v1`, dense_units=128)**:
  All four stages executed sequentially (`prepare` -> `preprocess` -> `train` -> `evaluate`). Initial `dvc.lock` generated.
- **D4 (`v2`, dense_units=256)**:
  `prepare` and `preprocess` were **skipped** (`didn't change, skipping`).
  Only `train` and `evaluate` re-ran.
- **Explanation**:
  DVC calculates cryptographic hashes for each stage based on its code dependencies, inputs, and declared `params.yaml` keys. Because `train.dense_units` only belongs to the `train` stage, the hashes for `prepare` and `preprocess` matched `dvc.lock` and were reused from cache. When `train` detected the altered hyperparameter, it re-executed, producing a new `models/model.h5` which invalidated `evaluate`'s dependency, triggering `evaluate` to update `metrics.json`.

### Metrics Comparison Table (v1 vs v2)
| Metric | v1 (`dense_units=128`) | v2 (`dense_units=256`) | Delta | Target Met? |
|---|---|---|---|---|
| **Test Accuracy** | `87.42%` (0.8742) | `87.36%` (0.8736) | -0.06% | **Yes** ($\ge 85\%$) |
| **Test Loss** | 0.3443 | 0.3555 | +0.0112 | N/A |

---

## Part E: Simulated Collaboration & Conflict Resolution

### Conflict Generation (E1–E3)
- In branch `teammate-sim`: modified `src/preprocess.py` to standardize pixels with mean/std `(x / 255.0 - 0.2860) / 0.3530`, ran `dvc repro preprocess`, pushed data to Google Drive, and committed.
- In branch `main`: modified `src/preprocess.py` to per-image min-max scaling `(a - a.min()) / (a.ptp() + 1e-7)`, ran `dvc repro preprocess`, pushed data to Google Drive, and committed.
- On `git merge teammate-sim`:
  ```text
  Auto-merging dvc.lock
  CONFLICT (content): Merge conflict in dvc.lock
  Auto-merging src/preprocess.py
  CONFLICT (content): Merge conflict in src/preprocess.py
  Automatic merge failed; fix conflicts and then commit the result.
  ```

### Dual Conflict Diagnosis
1. **Git Code Conflict (`src/preprocess.py`)**:
   Standardization formula in `teammate-sim` collided with per-image min-max formula on `main`.
2. **DVC Data Conflict (`dvc.lock`)**:
   Because `data/processed` is versioned through the pipeline, its content md5 hash is tracked in `dvc.lock`. Each normalization formula generated distinct numpy array hashes (`8f047b810c46b3f8e76b9b760b8cbb12.dir` vs `10645f906e4808544f4a5ccc579ced67.dir`), creating a simultaneous hash conflict in Git.

### Resolution (E4–E5)
1. **Code Conflict**: Selected `main`'s per-image min-max scaling (ensuring pixel values remain in $[0, 1]$ as specified in assignment requirements) and staged `src/preprocess.py`.
2. **Data Conflict**: Marked `main`'s pointer authoritative with `git checkout --ours dvc.lock` and staged it.
3. **Workspace Sync**: Ran `dvc checkout` to synchronize `data/processed` on disk with the resolved pointer hash.
4. **Merge Commit**: Committed resolution with `git commit -m "Merge teammate-sim into main (keep per-image min-max)"`.
5. **Verification**: Executed `dvc repro` to retrain and re-evaluate on the resolved state (`test_accuracy=0.8764`). Confirmed `dvc status` reports `Data and pipelines are up to date.`. Pushed final code to GitHub and all data artifacts to Google Drive remote.
