# Cancer Detection System

## Project Overview
This project is an AI-based computational pathology framework designed to predict the primary origin of Cancers of Unknown Primary (CUP) directly from Hematoxylin and Eosin (H&E) stained whole slide images. It utilizes deep learning (a multi-task ResNet-50 based architecture) to classify tumors into 18 primary origins and predict whether a lesion is Primary or Metastatic.

## Features
- **Origin Classification**: Classifies tumors into 18 different primary origins (e.g., Lung, Breast, Colorectal).
- **Metastatic Prediction**: Identifies whether the tumor is primary or metastatic.
- **Automated Pipeline**: A single master script installs dependencies, generates mock feature tensors for testing, trains the model, and evaluates it.
- **Custom Dataset Support**: Easily train on your own whole slide images (WSI) and patch features.

## Getting Started

### 1. Clone the Repository
To get started, clone the repository to your local machine:
```bash
git clone https://github.com/yashdiwan12/cancer_detection
cd cancer_detection
```

### 2. Installation & Quick Start
The simplest way to run the project is using the automated master script. It will automatically check for dependencies, install PyTorch and other required libraries, and run a complete training and evaluation pipeline on a dummy dataset.

```bash
python run_project.py
```

### 3. Manual Installation (Optional)
If you prefer to install dependencies manually:
```bash
pip install torch torchvision
pip install tensorboardX h5py torchsummary pandas numpy scikit-learn scipy tqdm
```

## Dataset Preparation
To run the model on your own dataset, you need:
1. A `.csv` file containing the labels (e.g., `slide_id`, `case_id`, `label`, `site`, `sex`).
2. Pre-extracted patch features saved as PyTorch `.pt` tensors (`N × 1024` shape) in your dataset directory.

*(Note: If you just run `run_project.py`, the system will automatically generate a dummy dataset of features for you to test the pipeline.)*

## Output & Monitoring
- **Logs & TensorBoard**: Training progress and metrics are saved in the `results/` folder. You can monitor them using TensorBoard.
- **Evaluation**: The script will output AUC (Area Under the Curve) and accuracy metrics upon completion.
