import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib

# 데이터 준비 함수
def prepare_data(file_path):
    # 데이터 읽기
    dataframe = pd.read_csv(file_path)

    # x로 시작하는 컬럼은 입력 데이터, y로 시작하는 컬럼은 출력 데이터로 분리
    input_columns = [col for col in dataframe.columns if col.startswith('x')]
    output_columns = [col for col in dataframe.columns if col.startswith('y')]

    X = dataframe[input_columns]
    y = dataframe[output_columns]

    # NaN 값 및 무한 값 처리
    X = X.replace([np.inf, -np.inf], np.nan).dropna()
    y = y.replace([np.inf, -np.inf], np.nan).dropna()

    # 데이터 정규화
    X_min, X_max = X.min(), X.max()
    y_min, y_max = y.min(), y.max()
    X = (X - X_min) / (X_max - X_min)
    y = (y - y_min) / (y_max - y_min)

    # 정규화 정보를 반환
    scaling_info = {
        "X_min": X_min, "X_max": X_max,
        "y_min": y_min, "y_max": y_max
    }

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, scaling_info

# DNN 모델 생성 및 학습 함수
def train_dnn(X_train, X_test, y_train, y_test, scaling_info, model_path="dnn_model.h5", scaler_path="scaling_info.pkl"):
    # DNN 모델 정의
    model = Sequential([
        Dense(8, activation='relu', input_dim=X_train.shape[1]),
        Dense(8, activation='relu'),
        Dense(8, activation='relu'),
        Dense(y_train.shape[1])  # 출력 노드 수는 y의 열 개수에 맞춤
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['mse'])

    # 조기 종료 설정
    early_stopping = EarlyStopping(patience=10, restore_best_weights=True)

    # 모델 학습
    model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=100,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=1
    )

    # 모델 평가
    loss, mse = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test MSE: {mse:.4f}")

    # 모델 저장
    model.save(model_path)
    print(f"Model saved to {model_path}")

    # 스케일링 정보 저장
    joblib.dump(scaling_info, scaler_path)
    print(f"Scaling info saved to {scaler_path}")

    return model

# 실행 코드
def main():
    data_file_path = "trend_sample_data.csv"  # 데이터 파일 경로
    model_save_path = "dnn_model.h5"  # 모델 저장 경로
    scaler_save_path = "scaling_info.pkl"  # 스케일링 정보 저장 경로

    # 데이터 준비
    X_train, X_test, y_train, y_test, scaling_info = prepare_data(data_file_path)

    # DNN 모델 학습 및 저장
    model = train_dnn(X_train, X_test, y_train, y_test, scaling_info, model_path=model_save_path, scaler_path=scaler_save_path)

if __name__ == "__main__":
    main()
