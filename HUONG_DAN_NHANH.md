# ⚡ HƯỚNG DẪN NHANH - TẠO FILE FIREBASE-KEY.JSON

## 🎯 Mục tiêu
Tạo file `firebase-key.json` để Streamlit có thể kết nối Firebase và lấy dữ liệu thật.

---

## 📋 3 BƯỚC ĐƠN GIẢN

### Bước 1: Vào Firebase Console
1. Mở trình duyệt, vào: **https://console.firebase.google.com/**
2. Đăng nhập và chọn project: **nlmt-duy**

### Bước 2: Tải file JSON
1. Click **⚙️ Project Settings** (bánh răng góc trên bên trái)
2. Chọn tab **Service accounts**
3. Scroll xuống, tìm phần **"Firebase Admin SDK"**
4. Click nút **"Generate new private key"** (màu xanh)
5. Xác nhận → File JSON sẽ tự động tải về

### Bước 3: Đặt file vào project
1. Tìm file vừa tải (thường ở thư mục Downloads)
2. **Đổi tên** file thành: `firebase-key.json`
3. **Copy** file vào thư mục project:
   ```
   D:\research2025\a Duy\giao_dien_streamlit\
   ```
   (Cùng thư mục với file `app.py`)

---

## ✅ Kiểm tra

Sau khi đặt file, thư mục của bạn sẽ có:
```
giao_dien_streamlit/
├── app.py
├── firebase-key.json  ← File này
├── requirements.txt
└── ...
```

---

## 🚀 Chạy lại app

1. Trong Streamlit, click **"🔄 Load Data"**
2. Nếu thành công, bạn sẽ thấy:
   - ✅ "Đã tải X bản ghi từ Firebase"
   - Dữ liệu hiển thị trong bảng

---

## ⚠️ Lưu ý

- **KHÔNG** đẩy file `firebase-key.json` lên GitHub
- File này chứa thông tin bảo mật quan trọng
- Nếu mất file, tải lại từ Firebase Console

---

## 🆘 Vẫn không được?

1. Kiểm tra tên file phải chính xác: `firebase-key.json` (không có khoảng trắng)
2. Kiểm tra file có trong đúng thư mục không
3. Thử tải lại file mới từ Firebase Console
4. Xem file `CAU_HINH_FIREBASE.md` để biết chi tiết hơn

---

**Xong! Bây giờ app sẽ lấy dữ liệu thật từ Firebase! 🎉**

