# CropWise — Smart Crop Recommendation System

A Python and Streamlit web application that demonstrates crop recommendation based on soil nutrient levels and environmental conditions.

## Overview

Crop selection depends on factors such as soil nutrients, temperature, humidity, pH, and rainfall. CropWise provides an interactive dashboard where users can enter these parameters and view a crop recommendation.

The project is designed around Multinomial Logistic Regression for multi-class classification. The current implementation uses a rule-based prediction function to demonstrate the workflow. Integration of a trained machine-learning model is planned for a future version.

## Features

- Interactive dashboard with five navigation pages.
- Input fields for seven soil and environmental parameters.
- Rule-based crop recommendation.
- Visualization of the recommended crop and demonstration probability values.
- Tabular summary of user inputs.
- Explanation of Multinomial Logistic Regression and the Softmax function.
- Performance dashboard with sections for classification metrics.
- Modular structure for future machine-learning integration.

## Supported Crops

The application includes ten crop categories:

Rice, Maize, Chickpea, Cotton, Coffee, Banana, Mango, Watermelon, Lentil, and Jute.

## Input Parameters

| Parameter | Description |
|---|---|
| Nitrogen (N) | Soil nitrogen content |
| Phosphorus (P) | Soil phosphorus content |
| Potassium (K) | Soil potassium content |
| Temperature | Environmental temperature in °C |
| Humidity | Relative humidity in % |
| Soil pH | Soil acidity or alkalinity |
| Rainfall | Rainfall measurement in mm |

## Technology Stack

- **Python** — Application logic
- **Streamlit** — Web interface
- **Pandas** — Data processing and tabular display
- **NumPy** — Numerical computing
- **Scikit-learn** — Planned model training and evaluation

## Project Structure

```text
cropwise_streamlit/
├── app.py
├── README.md
├── requirements.txt
└── venv/                 # Local virtual environment; not committed
```

## Installation and Setup

### Prerequisites

- Python 3.11 or a compatible version
- Git
- Visual Studio Code (recommended)
- PowerShell on Windows

### 1. Clone the repository

Replace the placeholder with your GitHub repository URL.

```powershell
git clone <repository-url>
cd cropwise_streamlit
```

Alternatively, download the repository and open its folder in VS Code.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the application

```powershell
streamlit run app.py
```

Open the local URL displayed in the terminal, usually [http://localhost:8501](http://localhost:8501).

### Running the Application Again

After the initial setup, activate the existing virtual environment and start the application:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

Dependencies do not need to be reinstalled unless the environment is recreated or the required packages change.

## How It Works

The current application follows these steps:

1. The user enters the seven soil and environmental parameters.
2. The application passes the inputs to a prediction function.
3. Predefined rules determine the recommended crop.
4. The dashboard displays the recommendation, demonstration probability values, and input summary.

### Intended Machine-Learning Approach

The planned model uses Multinomial Logistic Regression to classify agricultural conditions into one of the supported crop categories.

For each class \(k\), the model calculates a score:

\[
Z_k=b_k+\sum_i w_{ik}x_i
\]

The Softmax function converts these scores into class probabilities:

\[
P(y=k\mid X)=\frac{e^{Z_k}}{\sum_j e^{Z_j}}
\]

The class with the highest predicted probability is selected as the recommendation.

These equations describe the intended machine-learning approach. The current rule-based implementation does not perform this calculation.

## Model Evaluation

The Performance page includes sections for:

- Accuracy
- Precision
- Recall
- F1 score
- Confusion matrix
- Dataset overview

**Note:** The current metric values are illustrative, not verified results from a trained model. Actual evaluation requires a labelled dataset, a suitable train-test split, and metrics calculated from model predictions.

## Future Enhancements

- Train and integrate a Multinomial Logistic Regression model.
- Evaluate model performance using a held-out test dataset.
- Generate a confusion matrix and classification report from actual predictions.
- Integrate weather APIs for updated environmental data.
- Add fertilizer recommendations based on soil conditions.
- Incorporate IoT sensors for real-time soil measurements.
- Explore location-based recommendations and relevant weather or air-quality data.

## Objective

To develop an interactive crop recommendation application that demonstrates how agricultural data, classification techniques, and web-based visualization can support crop selection.

## Conclusion

CropWise provides a foundation for exploring crop recommendation through a Streamlit dashboard. The current version demonstrates the prediction workflow using predefined rules, with scope for integrating a trained machine-learning model and evaluating its performance in future development.

---

**CropWise — Smart Decisions. Better Farming.**
