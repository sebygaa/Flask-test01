import pandas as pd
import matplotlib.pyplot as plt

# 입력 변수와 출력 변수의 관계를 시각화
def plot_input_vs_output(file_path):
    # 파일에서 데이터 읽기
    dataframe = pd.read_csv(file_path)

    # Input과 Output 구분
    input_columns = [col for col in dataframe.columns if col.startswith('x')]
    output_columns = [col for col in dataframe.columns if col.startswith('y')]

    plt.figure(figsize=(15, 5 * len(output_columns) * len(input_columns)))

    plot_num = 1
    for output_column in output_columns:
        for input_column in input_columns:
            plt.subplot(len(output_columns), len(input_columns), plot_num)
            plt.scatter(dataframe[input_column], dataframe[output_column], alpha=0.7, label=f"{input_column} vs {output_column}")
            plt.xlabel(input_column)
            plt.ylabel(output_column)
            plt.title(f"{input_column} vs {output_column}")
            plt.grid(True)
            plt.legend()
            plot_num += 1

    plt.tight_layout()
    plt.show()

# 실행
data_file_path = "trend_sample_data.csv"  # 제공된 샘플 데이터 파일 경로
plot_input_vs_output(data_file_path)
