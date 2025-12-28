# 🔐 HƯỚNG DẪN CẤU HÌNH FIREBASE CHO STREAMLIT

## 📋 Bước 1: Lấy Firebase Service Account Key

### 1.1. Vào Firebase Console
1. Truy cập: https://console.firebase.google.com/
2. Chọn project của bạn: **nlmt-duy**

### 1.2. Tạo Service Account
1. Click vào **⚙️ Project Settings** (bánh răng ở góc trên bên trái)
2. Chọn tab **Service accounts**
3. Scroll xuống phần **"Firebase Admin SDK"**
4. Click nút **"Generate new private key"**
5. Xác nhận và tải file JSON về

### 1.3. Đặt tên file
- Đổi tên file JSON thành: `firebase-key.json`
- Copy file vào thư mục project (cùng thư mục với `app.py`)

---

## 📁 Bước 2: Cấu hình trong Streamlit

### Cách 1: Sử dụng file JSON (Local - KHUYẾN NGHỊ)

1. Đặt file `firebase-key.json` trong thư mục project:
   ```
   giao_dien_streamlit/
   ├── app.py
   ├── firebase-key.json  ← File này
   ├── requirements.txt
   └── ...
   ```

2. Code sẽ tự động nhận diện file và kết nối Firebase

3. **QUAN TRỌNG**: Thêm `firebase-key.json` vào `.gitignore` để không đẩy lên GitHub!

---

### Cách 2: Sử dụng Streamlit Secrets (Deploy lên Cloud)

Nếu bạn deploy lên Streamlit Cloud:

1. Vào [share.streamlit.io](https://share.streamlit.io/)
2. Chọn app của bạn → **Settings** → **Secrets**
3. Thêm nội dung file JSON vào Secrets:

```toml
[firebase]
type = "service_account"
project_id = "nlmt-duy"
private_key_id = "abc123..."
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxxxx@nlmt-duy.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40nlmt-duy.iam.gserviceaccount.com"
```

4. Lưu lại và app sẽ tự động sử dụng secrets

---

## 🔒 Bước 3: Cấu hình Firebase Database Rules

Đảm bảo Firebase Realtime Database cho phép đọc dữ liệu:

1. Vào Firebase Console → **Realtime Database**
2. Click tab **Rules**
3. Đảm bảo rules cho phép đọc (hoặc sử dụng authentication):

```json
{
  "rules": {
    "sensor_data": {
      ".read": true,  // Cho phép đọc (hoặc thay bằng auth != null)
      ".write": false  // Không cho phép ghi từ web
    }
  }
}
```

4. Click **Publish**

---

## ✅ Bước 4: Kiểm tra kết nối

1. Chạy Streamlit:
   ```powershell
   streamlit run app.py
   ```

2. Chọn ngày và giờ có dữ liệu trong Firebase

3. Click **"🔄 Load Data"**

4. Nếu thành công, bạn sẽ thấy:
   - ✅ "Đã tải X bản ghi từ Firebase"
   - Dữ liệu hiển thị trong bảng và biểu đồ

5. Nếu lỗi:
   - ❌ Kiểm tra file `firebase-key.json` có đúng tên không
   - ❌ Kiểm tra đường dẫn file có đúng không
   - ❌ Kiểm tra Firebase Database Rules

---

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "FileNotFoundError: firebase-key.json"
- **Nguyên nhân**: File không tồn tại hoặc sai tên
- **Giải pháp**: Kiểm tra tên file phải chính xác là `firebase-key.json`

### Lỗi: "Permission denied"
- **Nguyên nhân**: Firebase Rules không cho phép đọc
- **Giải pháp**: Cập nhật Rules như Bước 3

### Lỗi: "Invalid credentials"
- **Nguyên nhân**: File JSON bị sai hoặc thiếu thông tin
- **Giải pháp**: Tải lại file từ Firebase Console

### Lỗi: "Database URL not found"
- **Nguyên nhân**: Database URL sai
- **Giải pháp**: Kiểm tra URL trong Firebase Console → Realtime Database → Data

---

## 📝 Cấu trúc dữ liệu trong Firebase

App sẽ đọc dữ liệu từ path:
```
/sensor_data/{YYYY-MM-DD}/{HH}/{HH:MM:SS}
```

Ví dụ:
```
/sensor_data/2025-12-26/17/17:32:05
  ├── U: 12.5
  ├── Current: 0.5
  ├── milliWatt: 6000
  ├── energy: 100.5
  ├── Lux: 50000
  ├── Temp: 28.5
  └── Humi: 65.0
```

---

## 🔐 Bảo mật

⚠️ **QUAN TRỌNG**:
- **KHÔNG** đẩy file `firebase-key.json` lên GitHub
- File này chứa thông tin bảo mật quan trọng
- Đã có trong `.gitignore` để tự động bỏ qua

✅ **An toàn**:
- Sử dụng Streamlit Secrets khi deploy
- Chỉ share file JSON với người tin cậy
- Nếu lỡ đẩy lên GitHub, hãy xóa ngay và tạo key mới

---

## 🎯 Tóm tắt nhanh

1. ✅ Tải `firebase-key.json` từ Firebase Console
2. ✅ Đặt file trong thư mục project
3. ✅ Chạy `streamlit run app.py`
4. ✅ Chọn ngày/giờ và click "Load Data"
5. ✅ Xem dữ liệu thật từ Firebase!

---

**Chúc bạn thành công! 🚀**

