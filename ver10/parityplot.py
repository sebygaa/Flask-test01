import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Generate random data for Given Data and Model Predictions
np.random.seed(42)  # For reproducibility
n_points = 100
given_data = np.linspace(0, 100, n_points)

# Model predictions with specified R^2 values
noise_dnn = np.random.normal(0, 5, n_points)
dnn_predictions = given_data * 0.93 + noise_dnn  # R^2 ~ 0.93

noise_rf = np.random.normal(0, 10, n_points)
rf_predictions = given_data * 0.88 + noise_rf  # R^2 ~ 0.88

noise_gbm = np.random.normal(0, 4, n_points)
gbm_predictions = given_data * 0.94 + noise_gbm  # R^2 ~ 0.94

noise_transformer = np.random.normal(0, 2, n_points)
transformer_predictions = given_data * 0.98 + noise_transformer  # R^2 ~ 0.98

# Calculate R^2 values
r2_dnn = r2_score(given_data, dnn_predictions)
r2_rf = r2_score(given_data, rf_predictions)
r2_gbm = r2_score(given_data, gbm_predictions)
r2_transformer = r2_score(given_data, transformer_predictions)

# Create a 2x2 subplot for parity plots
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# DNN Plot
axes[0, 0].scatter(given_data, dnn_predictions, alpha=0.7, label=f"R² = {r2_dnn:.3f}")
axes[0, 0].plot(given_data, given_data, color='red', linestyle='--')
axes[0, 0].set_title("DNN")
axes[0, 0].set_xlabel("Given Data")
axes[0, 0].set_ylabel("Model Prediction")
axes[0, 0].grid(True)
axes[0, 0].legend()

# RF Plot
axes[0, 1].scatter(given_data, rf_predictions, alpha=0.7, label=f"R² = {r2_rf:.3f}")
axes[0, 1].plot(given_data, given_data, color='red', linestyle='--')
axes[0, 1].set_title("RF")
axes[0, 1].set_xlabel("Given Data")
axes[0, 1].set_ylabel("Model Prediction")
axes[0, 1].grid(True)
axes[0, 1].legend()

# GBM Plot
axes[1, 0].scatter(given_data, gbm_predictions, alpha=0.7, label=f"R² = {r2_gbm:.3f}")
axes[1, 0].plot(given_data, given_data, color='red', linestyle='--')
axes[1, 0].set_title("GBM")
axes[1, 0].set_xlabel("Given Data")
axes[1, 0].set_ylabel("Model Prediction")
axes[1, 0].grid(True)
axes[1, 0].legend()

# Transformer Plot
axes[1, 1].scatter(given_data, transformer_predictions, alpha=0.7, label=f"R² = {r2_transformer:.3f}")
axes[1, 1].plot(given_data, given_data, color='red', linestyle='--')
axes[1, 1].set_title("Transformer")
axes[1, 1].set_xlabel("Given Data")
axes[1, 1].set_ylabel("Model Prediction")
axes[1, 1].grid(True)
axes[1, 1].legend()

plt.tight_layout()
plt.show()
