import pandas as pd
import numpy as np

# 데이터 생성 함수
def generate_trend_data(file_name, n_samples=1000):
    # Input 데이터 생성
    x1 = np.random.rand(n_samples) * 10  # x1: [0, 10]
    x2 = np.random.rand(n_samples) * 10  # x2: [0, 10]
    x3 = np.random.rand(n_samples) * 10  # x3: [0, 10]

    # Output 데이터 생성 (트렌드와 노이즈 추가)
    noise_y1 = np.random.normal(0, 0.5, n_samples)  # 작은 노이즈
    noise_y2 = np.random.normal(0, 0.5, n_samples)  # 작은 노이즈

    y1 = np.exp(x1) + x2 ** 2 + 1 / (x3 + 1e-6) + noise_y1
    y2 = np.log(x1 + 1e-6) + x2 + x3 ** 3 + noise_y2

    # 데이터프레임으로 결합
    data = pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "x3": x3,
        "y1": y1,
        "y2": y2
    })

    # 데이터 저장
    data.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

# 실행
data_file_name = "trend_sample_data.csv"
generate_trend_data(data_file_name)
