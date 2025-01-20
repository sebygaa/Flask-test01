import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import MeanSquaredError
import joblib

# 데이터 준비 함수
def prepare_data(file_path, scaler_path):
    # 데이터 읽기
    dataframe = pd.read_csv(file_path)
    input_columns = [col for col in dataframe.columns if col.startswith('x')]
    output_columns = [col for col in dataframe.columns if col.startswith('y')]
    X = dataframe[input_columns]
    y = dataframe[output_columns]

    # 스케일링 정보 로드
    scaling_info = joblib.load(scaler_path)

    # 데이터 정규화 (Reverse Scaling 필요 시 이를 사용)
    X = (X - scaling_info["X_min"]) / (scaling_info["X_max"] - scaling_info["X_min"])
    y = (y - scaling_info["y_min"]) / (scaling_info["y_max"] - scaling_info["y_min"])

    return X, y, scaling_info, output_columns

# Reverse Scaling 함수
def reverse_scaling(y_scaled, scaling_info, output_columns):
    y_reversed = pd.DataFrame()
    for i, col in enumerate(output_columns):
        y_reversed[col] = y_scaled[:, i] * (scaling_info["y_max"][col] - scaling_info["y_min"][col]) + scaling_info["y_min"][col]
    return y_reversed

# Parity Plot 생성 함수
def plot_parity(y_true, y_pred, output_columns):
    num_outputs = len(output_columns)
    plt.figure(figsize=(8, 6 * num_outputs))

    for i, col in enumerate(output_columns):
        plt.subplot(num_outputs, 1, i + 1)
        plt.scatter(y_true[col], y_pred[col], alpha=0.7, label=f"{col} (True vs Predicted)")
        plt.plot([y_true[col].min(), y_true[col].max()], 
                 [y_true[col].min(), y_true[col].max()], 
                 color='red', linestyle='--', label="Perfect Parity")
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Parity Plot for {col}")
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()

# 실행 코드
def main():
    model_path = "dnn_model.h5"
    data_path = "trend_sample_data.csv"
    scaler_path = "scaling_info.pkl"

    # 모델 불러오기 (metrics 정의)
    custom_objects = {"mse": MeanSquaredError()}
    model = load_model(model_path, custom_objects=custom_objects)
    print(f"Model loaded from {model_path}")

    # 데이터 불러오기 및 스케일링 정보 로드
    X, y_true_scaled, scaling_info, output_columns = prepare_data(data_path, scaler_path)
    print(f"Data loaded from {data_path}")

    # 예측 생성
    y_pred_scaled = model.predict(X)
    print("Predictions generated.")

    # Reverse Scaling for true and predicted values
    y_true = reverse_scaling(y_true_scaled.values, scaling_info, output_columns)
    y_pred = reverse_scaling(y_pred_scaled, scaling_info, output_columns)

    # Parity Plot 생성
    plot_parity(y_true, y_pred, output_columns)

if __name__ == "__main__":
    main()
