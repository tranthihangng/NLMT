# 🚀 HƯỚNG DẪN CHẠY STREAMLIT DASHBOARD

## 📋 Bước 1: Cài đặt Python

Nếu chưa có Python, tải và cài đặt từ: https://www.python.org/downloads/
- Chọn phiên bản Python 3.9 trở lên
- **QUAN TRỌNG**: Tick chọn "Add Python to PATH" khi cài đặt

---

## 📦 Bước 2: Cài đặt thư viện

Mở **PowerShell** hoặc **Command Prompt** trong thư mục project, chạy:

```powershell
pip install -r requirements.txt
```

Hoặc cài từng thư viện:

```powershell
pip install streamlit firebase-admin plotly pandas
```

---

## 🔐 Bước 3: Cấu hình Firebase

### Cách lấy Service Account Key:

1. Vào [Firebase Console](https://console.firebase.google.com/)
2. Chọn project của bạn (nlmt-duy)
3. Click **⚙️ Project Settings** (bánh răng)
4. Chọn tab **Service accounts**
5. Click **"Generate new private key"**
6. Tải file JSON về

### Cách sử dụng:

**Cách 1: Sử dụng file JSON (KHUYẾN NGHỊ)**

1. Đổi tên file JSON thành `firebase-key.json`
2. Copy vào thư mục project
3. Mở `app.py`, tìm dòng ~175, sửa thành:

```python
cred = credentials.Certificate("firebase-key.json")
```

4. Comment hoặc xóa phần `service_account_info = {...}`

**Cách 2: Sử dụng biến môi trường (cho deploy)**

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="path/to/firebase-key.json"
```

---

## ▶️ Bước 4: Chạy ứng dụng

```powershell
streamlit run app.py
```

Hoặc double-click file `run_streamlit.bat` (tôi sẽ tạo cho bạn)

### Kết quả:
- Trình duyệt sẽ tự động mở
- Địa chỉ mặc định: `http://localhost:8501`
- Nhấn `Ctrl+C` trong terminal để dừng

---

## 🌐 Bước 5: Deploy lên Streamlit Cloud (MIỄN PHÍ)

### 5.1. Đẩy code lên GitHub

1. Tạo repository mới trên GitHub
2. Push code lên:

```powershell
git init
git add .
git commit -m "Solar Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**LƯU Ý**: KHÔNG đẩy file `firebase-key.json` lên GitHub!

Tạo file `.gitignore`:
```
firebase-key.json
__pycache__/
*.pyc
.env
```

### 5.2. Deploy trên Streamlit Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io/)
2. Đăng nhập bằng GitHub
3. Click **"New app"**
4. Chọn repository và branch
5. Main file path: `app.py`
6. Click **"Deploy!"**

### 5.3. Thêm Firebase Secrets

1. Trong Streamlit Cloud, vào **Settings > Secrets**
2. Thêm nội dung file `firebase-key.json`:

```toml
[firebase]
type = "service_account"
project_id = "nlmt-duy"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
# ... (copy tất cả từ file JSON)
```

3. Sửa code để đọc secrets (trong `app.py`):

```python
import streamlit as st

service_account_info = dict(st.secrets["firebase"])
cred = credentials.Certificate(service_account_info)
```

---

## 🔧 Xử lý lỗi thường gặp

### Lỗi: "streamlit không nhận diện được"
```powershell
python -m streamlit run app.py
```

### Lỗi: Firebase connection
- Kiểm tra đường dẫn file `firebase-key.json`
- Kiểm tra quyền đọc database trong Firebase Rules

### Lỗi: Module not found
```powershell
pip install --upgrade streamlit firebase-admin plotly pandas
```

---

## 📁 Cấu trúc thư mục

```
giao_dien_streamlit/
├── app.py              # File chính Streamlit
├── requirements.txt    # Thư viện cần cài
├── firebase-key.json   # Firebase credentials (KHÔNG đẩy lên GitHub!)
├── .gitignore          # Bỏ qua files nhạy cảm
├── index.html          # Phiên bản HTML (backup)
├── run_streamlit.bat   # Script chạy nhanh
└── README.md           # Hướng dẫn
```

---

## 🎯 Tính năng Dashboard

✅ **7 Metric Cards** - Hiển thị giá trị real-time với % thay đổi  
✅ **6 Biểu đồ** - Voltage, Current, Power, Lux, Temp, Humidity  
✅ **Bảng dữ liệu** - Hiển thị tất cả records, mới nhất trước  
✅ **Thống kê** - Min/Avg/Max cho mỗi chỉ số  
✅ **Auto Refresh** - Tự động cập nhật mỗi 10 giây  
✅ **Export CSV** - Xuất dữ liệu ra file  
✅ **Dark Theme** - Giao diện chuyên nghiệp  
✅ **Responsive** - Tự động điều chỉnh trên mọi thiết bị  

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Python version: `python --version` (cần >= 3.9)
2. Pip version: `pip --version`
3. Streamlit version: `streamlit version`
4. Firebase console logs

Happy coding! 🎉

