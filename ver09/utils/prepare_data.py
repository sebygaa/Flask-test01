import pandas as pd
import numpy as np
import joblib

def prepare_data(file_path, scaler_path):
    """
    Prepares data for the model by loading, normalizing, and splitting.

    Args:
        file_path (str): Path to the CSV file containing the data.
        scaler_path (str): Path to the saved scaler information file.

    Returns:
        tuple: (X, y, scaling_info, output_columns)
    """
    dataframe = pd.read_csv(file_path)

    input_columns = [col for col in dataframe.columns if col.startswith('x')]
    output_columns = [col for col in dataframe.columns if col.startswith('y')]

    X = dataframe[input_columns]
    y = dataframe[output_columns]

    # Load scaling information
    scaling_info = joblib.load(scaler_path)

    # Normalize data
    X = (X - scaling_info["X_min"]) / (scaling_info["X_max"] - scaling_info["X_min"])
    y = (y - scaling_info["y_min"]) / (scaling_info["y_max"] - scaling_info["y_min"])

    return X, y, scaling_info, output_columns

def reverse_scaling(y_scaled, scaling_info, output_columns):
    """
    Reverses the scaling for output values.

    Args:
        y_scaled (numpy.ndarray): Scaled output values.
        scaling_info (dict): Dictionary with scaling information.
        output_columns (list): List of output column names.

    Returns:
        pd.DataFrame: Reversed scaled values as a DataFrame.
    """
    y_reversed = pd.DataFrame()
    for i, col in enumerate(output_columns):
        y_reversed[col] = y_scaled[:, i] * (scaling_info["y_max"][col] - scaling_info["y_min"][col]) + scaling_info["y_min"][col]
    return y_reversed
