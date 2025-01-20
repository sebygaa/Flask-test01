from flask import Flask, request, render_template, jsonify
import os
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
from utils.prepare_data import prepare_data
from utils.plot_parity import plot_parity

app = Flask(__name__)

# 업로드 파일 저장 경로 설정
UPLOAD_FOLDER = './uploads'
MODEL_FOLDER = './models'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_FOLDER'] = MODEL_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # 파일 저장
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # 모델 및 스케일링 정보 로드
    model_path = os.path.join(app.config['MODEL_FOLDER'], 'dnn_model.h5')
    scaler_path = os.path.join(app.config['MODEL_FOLDER'], 'scaling_info.pkl')
    model = load_model(model_path)
    scaling_info = joblib.load(scaler_path)

    # 데이터 준비
    X, y_true, scaling_info, output_columns = prepare_data(file_path, scaler_path)
    y_pred_scaled = model.predict(X)

    # 결과 복원 및 시각화
    y_true_reversed = reverse_scaling(y_true.values, scaling_info, output_columns)
    y_pred_reversed = reverse_scaling(y_pred_scaled, scaling_info, output_columns)
    plot_path = plot_parity(y_true_reversed, y_pred_reversed, output_columns)

    return jsonify({"message": "File processed successfully.", "plot_path": plot_path})

if __name__ == "__main__":
    app.run(debug=True)
