# 🔒 HƯỚNG DẪN BẢO MẬT FIREBASE

## ⚠️ CẢNH BÁO
Firebase đang cảnh báo: "Your security rules are defined as public, so anyone can steal, modify, or delete data in your database"

## 🛡️ GIẢI PHÁP

### 1. CẬP NHẬT FIREBASE SECURITY RULES

Vào **Firebase Console** → **Realtime Database** → **Rules**

#### Option A: Chỉ cho phép ĐỌC (phù hợp cho dashboard công khai)

```json
{
  "rules": {
    "sensor_data": {
      ".read": true,
      ".write": false
    }
  }
}
```

**Lưu ý:** Với rule này:
- ✅ Mọi người có thể XEM dữ liệu (Dashboard HTML hoạt động)
- ❌ Không ai có thể GHI dữ liệu từ client (chỉ ESP32/Arduino với Service Account mới ghi được)

#### Option B: Yêu cầu Authentication (bảo mật hơn)

```json
{
  "rules": {
    "sensor_data": {
      ".read": "auth != null",
      ".write": "auth != null && auth.token.admin === true"
    }
  }
}
```

**Lưu ý:** Cần thêm Firebase Authentication vào HTML Dashboard.

#### Option C: Cho phép ESP32 ghi, Dashboard chỉ đọc (KHUYẾN NGHỊ)

```json
{
  "rules": {
    "sensor_data": {
      ".read": true,
      ".write": "auth != null || request.auth.uid == 'esp32-device'"
    }
  }
}
```

---

### 2. PHÂN BIỆT CÁC LOẠI KEY

| Key/Config | Loại | Có thể public? | Vị trí |
|------------|------|----------------|--------|
| `firebase-key.json` | Service Account Private Key | ❌ **KHÔNG BAO GIỜ** | Local/Streamlit Secrets |
| `apiKey` trong HTML | Web API Key | ✅ Có thể (bảo mật bởi Rules) | index.html |
| `projectId` | Project ID | ✅ Có thể | index.html |
| `databaseURL` | Database URL | ✅ Có thể | index.html |

### 3. GIẢI THÍCH

#### Firebase Web Config (apiKey, projectId, etc.)
- **Được thiết kế để public** - không phải bí mật
- Bảo mật đến từ **Firebase Security Rules**, không phải từ việc giấu config
- Giống như địa chỉ nhà - ai cũng biết, nhưng có khóa cửa (Rules)

#### Service Account Key (firebase-key.json)
- **TUYỆT ĐỐI KHÔNG ĐƯỢC PUBLIC**
- Dùng cho backend (Python, Node.js)
- Có toàn quyền truy cập database
- Giống như chìa khóa master - ai có là vào được

---

### 4. CHECKLIST BẢO MẬT

- [x] `firebase-key.json` trong `.gitignore`
- [x] Không commit `firebase-key.json` lên GitHub
- [x] Dùng Streamlit Secrets cho production
- [ ] **CẬP NHẬT Firebase Security Rules** ← QUAN TRỌNG NHẤT
- [ ] (Tùy chọn) Thêm Firebase Authentication

---

### 5. CÁCH CẬP NHẬT FIREBASE RULES

1. Truy cập: https://console.firebase.google.com/
2. Chọn project `nlmt-duy`
3. Vào **Realtime Database** (menu bên trái)
4. Click tab **Rules**
5. Thay đổi rules như hướng dẫn ở trên
6. Click **Publish**

---

### 6. KIỂM TRA ĐÃ AN TOÀN CHƯA

Sau khi cập nhật rules, thử:

```javascript
// Trong console trình duyệt, thử ghi dữ liệu
firebase.database().ref('sensor_data/test').set({test: 'hack'})
```

Nếu rules đúng, sẽ báo lỗi: `PERMISSION_DENIED`

---

## 📌 TÓM TẮT

| Vấn đề | Giải pháp |
|--------|-----------|
| "Security rules are public" | Cập nhật Firebase Rules |
| Lộ firebase-key.json | Thêm vào .gitignore (đã có) |
| Lộ API key trong HTML | Không sao, đây là thiết kế của Firebase. Bảo mật bởi Rules |
| ESP32 cần ghi dữ liệu | Dùng Service Account hoặc custom token |

---

**Quan trọng nhất: CẬP NHẬT FIREBASE SECURITY RULES ngay bây giờ!**

