import joblib
import numpy as np

class CiperType:
    # 1. Tải mô hình, vectorizer và label encoder đã được lưu
    model_path = 'Model/svm_model_ascii.joblib'
    vectorizer_path = 'Model/tfidf_vectorizer_ascii.joblib'
    label_encoder_path = 'Model/label_encoder_ascii.joblib'

    # Tải các đối tượng đã lưu
    svm_model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    label_encoder = joblib.load(label_encoder_path)

    # 2. Hàm chuyển đổi ciphertext thành mã ASCII
    @staticmethod
    def text_to_ascii(text):
        return ' '.join(str(ord(char)) for char in text)
    # 3. Hàm dự đoán kiểu mã hóa
    
    @staticmethod
    def predict_cipher_type(ciphertext):
        # Chuyển ciphertext thành ASCII
        ciphertext_ascii = CiperType.text_to_ascii(ciphertext)
        
        # Chuyển đổi ciphertext thành đặc trưng số
        X_input = CiperType.vectorizer.transform([ciphertext_ascii])
        
        # Dự đoán kiểu mã hóa
        y_pred = CiperType.svm_model.predict(X_input)
        
        # Chuyển đổi kết quả dự đoán từ số thành nhãn (tên kiểu mã hóa)
        cipher_type = CiperType.label_encoder.inverse_transform(y_pred)
                
        return cipher_type[0]