# Adult Census Income Analysis

This project involves an end-to-end analysis and classification of the **Adult Census Income Dataset**. The goal is to predict whether an individual's income exceeds $50K/yr based on various census data features.

## 📂 Project Structure

- **`adult.csv`**: The dataset containing census information.
- **`assignment.ipynb`**: The main Jupyter Notebook containing Data Preprocessing, Exploratory Data Analysis (EDA), Feature Engineering, Model Training, and Evaluation.
- **`requirements.txt`**: List of Python dependencies required to run the notebook.
- **`performance_metrics.csv`**: Contains the evaluation metrics (Accuracy, Precision, Recall, F1-Score) of the different models trained.
- **`*.png`**: Visualizations generated during the analysis, including EDA insights, correlation matrices, model comparisons, confusion matrices, and ROC curves.
- **`MPOnlineAssignment.pdf` / `.docx`**: Assignment description and prompt.

## 📊 Visualizations & Insights

The notebook generates several visualizations that are saved as images:
- **`task1_understanding.png`**: Initial data exploration and distribution visualization.
- **`task3_correlation.png`**: Correlation heatmap of the numerical features.
- **`task5_comparison.png`**: A bar chart comparing the performance of different classification models.
- **`task5_confusion_matrices.png`**: Confusion matrices for the evaluated models.
- **`task5_roc_curves.png`**: ROC curves to evaluate the True Positive Rate vs False Positive Rate.

## 🚀 Setup & Installation

To run this project locally, ensure you have Python installed. It is recommended to use a virtual environment.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sharmapragalbh565-lgtm/Adult-Census-Income-Analysis.git
   cd Adult-Census-Income-Analysis
   ```

2. **Create a virtual environment (Optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```
   Open `assignment.ipynb` and run the cells to reproduce the analysis.

## 🛠️ Technologies Used

- **Python** 
- **Pandas & NumPy** (Data Manipulation)
- **Matplotlib & Seaborn** (Data Visualization)
- **Scikit-Learn** (Machine Learning & Modeling)
- **Jupyter Notebook** (Interactive coding environment)
