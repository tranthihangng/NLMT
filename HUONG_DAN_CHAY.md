# 📖 HƯỚNG DẪN CHẠY FILE HTML

## Cách 1: Mở trực tiếp (Đơn giản nhất) ⚡

1. **Double-click** vào file `index.html`
2. File sẽ mở bằng trình duyệt mặc định (Chrome, Edge, Firefox...)
3. ✅ **Lưu ý**: Có thể gặp lỗi CORS với Firebase khi mở trực tiếp

---

## Cách 2: Mở bằng trình duyệt thủ công 🌐

1. Mở trình duyệt (Chrome, Edge, Firefox...)
2. Nhấn `Ctrl + O` (hoặc File > Open)
3. Chọn file `index.html`
4. Click "Open"

---

## Cách 3: Chạy Local Server (KHUYẾN NGHỊ) ✅

### Option A: Dùng Python (Nếu đã cài Python)

1. Mở **PowerShell** hoặc **Command Prompt** trong thư mục chứa file
2. Chạy lệnh:
   ```powershell
   python -m http.server 8000
   ```
   hoặc nếu dùng Python 2:
   ```powershell
   python -m SimpleHTTPServer 8000
   ```
3. Mở trình duyệt, vào: `http://localhost:8000`
4. Click vào `index.html`

### Option B: Dùng Node.js (Nếu đã cài Node.js)

1. Cài đặt `http-server` (chỉ cần 1 lần):
   ```powershell
   npm install -g http-server
   ```
2. Mở PowerShell trong thư mục chứa file
3. Chạy:
   ```powershell
   http-server -p 8000
   ```
4. Mở trình duyệt, vào: `http://localhost:8000`

### Option C: Dùng VS Code Live Server

1. Cài extension **"Live Server"** trong VS Code
2. Right-click vào file `index.html`
3. Chọn **"Open with Live Server"**

---

## Cách 4: Dùng script tự động (Windows) 🚀

Tôi đã tạo file `chay.bat` - chỉ cần **double-click** vào file đó!

---

## ⚠️ LƯU Ý QUAN TRỌNG:

1. **Cấu hình Firebase trước**: Phải điền Firebase config trong file `index.html` (dòng 19-26)
2. **Nếu gặp lỗi CORS**: Dùng Cách 3 (Local Server) thay vì mở trực tiếp
3. **Kiểm tra kết nối Internet**: Cần internet để load Firebase SDK và Chart.js

---

## 🎯 BƯỚC TIẾP THEO:

1. ✅ Mở file `index.html`
2. ✅ Điền Firebase config (apiKey, projectId, appId...)
3. ✅ Chọn ngày và giờ
4. ✅ Click "Load Data"
5. ✅ Xem dữ liệu và biểu đồ!

