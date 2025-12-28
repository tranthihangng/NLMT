# 🔐 Hướng dẫn cấu hình Firebase trên Streamlit Cloud

## ⚠️ Vấn đề
Khi chạy app trên Streamlit Cloud, file `firebase-key.json` không có sẵn (vì lý do bảo mật). Bạn cần cấu hình Firebase credentials qua **Streamlit Secrets**.

## 📋 Các bước cấu hình

### Bước 1: Vào Streamlit Cloud Dashboard
1. Truy cập: https://share.streamlit.io/
2. Đăng nhập vào tài khoản của bạn
3. Chọn app **nlmt-duy** (hoặc tên app của bạn)

### Bước 2: Mở Settings và Secrets
1. Click vào **⚙️ Settings** (ở góc dưới bên trái sidebar)
2. Trong menu, click **🔐 Secrets**

### Bước 3: Thêm cấu hình Firebase
Copy **TOÀN BỘ** nội dung sau và paste vào editor:

```toml
[firebase]
type = "service_account"
project_id = "nlmt-duy"
private_key_id = "9c9c675eaf744554e32dfebb61cde80d1fe97a97"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDNtTxePWSv79rd\nUliNJncf0ucgQIhT4x2FTyMy855l8nEbUreGUk1xvWXtc9lNsQ2d3grDdEiW6pLC\nOyjJ5ddr4Gtcxl3Oa6bPTUT7T5fjN4lDaHs02uLrDk2r47wCBybdY6tm5fLtYFXN\n2BIIwKbcH+HKP/Dymm0Kucukv0GIlvDVhNFWlOCJUo1FIIvlGK3WwPhhA+KHpDWD\nj3vhGZAs93k+Rdddyel7LkZWTjb48Q8VbHHJv1mzLYEdsiJ+Lq4GshwOPxBjzbPx\nx0dgbsDLiy+C527++klNUkN4TI16eAjLkpUDx95jzNC2pRBBKqhC5pRs0almfc1h\nzCV+HvVjAgMBAAECggEAAYcMAOicVlVXEoEHO0KPWcyJckyfAwblxTKBXab7RjVO\n/j66lgHPLrrqg0OLn94kJrIHh9jC8PBwpTuQvfMqUpKIUcJ2EZKn5zUOx8KS8Be2\nCw6czofwgEN25ypTAQHsow459CvgVGTs0CP8fVI/J9VmoMeIoIjbUsZC9g/b2+qK\nuygWKGNWbG4sfJVhHVJK6Whk+iAYr438lvgveuakqsU8vw2FL++W41YY/Y0pfvBL\nOMYADbGp2DthC/I03F/9m2uA7YNpWX4ldHgUJKrcRLeMsRdg8vQ/u9+bf591nMBx\nvWb2A/OtpxaISmtFsR0bOiHeiu4svBN6r3sdZ7jNiQKBgQDz/beIa7OqTdGBHnvU\ns22DACXZmlqkYKhN8smqbB8jWGS+viorYwBS2nI9LkaOSbVI/AwT9JEY9cW57QAh\n3vaEW3fNNVI//U61SIt8YlOl+WYmhKYIRo8TiS+5js+PLE7JgfuOFo28P/sza7X5\n6fiSSsYilq6jRTo1FkBporln3QKBgQDX1Sb0yMk6kBL7litfdwG2W2QRokmXOR5X\nevbZeASsNjjw0xt0qOuXUj9Iemi4RX7RGQDIe91r/ncAhh0U7yO4j3TV+noe18t9\nbs591lssff9lAenaTIdOLoKBSNahH9PL4k+F5rQjU+YPFU2JLDfYz4hiyhjINT5Y\nMOMdobSePwKBgQDOXe9I9Idu6QjlY+oq2mQq5Aofhd1aoOJZo5uMiIzBsXbsmh1C\nuya/7UGom6ZTnOY3R+/TRQ0ghmfpvRpai6IICvFGYO4jb1WOIUDRQL0tacdLlvBz\nmXJUfLkgAjluCHTPHSCuakcRTTBjqputOIbk/VeeU8J8GAaGdj6e2mJlBQKBgFRZ\nDNxlC59DZufDjDfGvniRxs3Nao0a2Wy+tXHPoaPbnO0g034H9eoxTmH41KwPHLyC\n1PeE0Me/rqoZv4vK2V7rUXG+bbNYCkJ+51vuRbthkknbMZUKi2ZWbtIvsRFO6uqn\nCwT9YDDePO5wGNke2sR0doyFBqJXjIHSuS9/XqLpAoGBALV0KXrfeymi6g5bq2Ez\nkCbWpy+ydmlN3ywRL/OiDIZpu7NcvPhgiMqsGCq29ZqgOQS63ra8t57b3ANeY58A\nr5Vcz8/Zf84A+KJ6l1+gxQGJInHgPt5ibZxGZthBQqcSmY67z0wAhvf+guGP7Z0L\nF7CMB6z8oHCpQQ3xqQWw5Cj2\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-fbsvc@nlmt-duy.iam.gserviceaccount.com"
client_id = "102300141875323288580"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40nlmt-duy.iam.gserviceaccount.com"
databaseURL = "https://nlmt-duy-default-rtdb.firebaseio.com"
```

### Bước 4: Lưu và chờ redeploy
1. Click nút **💾 Save** (hoặc **Save secrets**)
2. Streamlit Cloud sẽ tự động redeploy app
3. Chờ vài phút để app redeploy xong

### Bước 5: Kiểm tra
1. Refresh trang app
2. Vào phần **"🔬 Phân tích nâng cao"**
3. Nếu không còn lỗi Firebase, bạn đã cấu hình thành công! ✅

## 📸 Hình ảnh minh họa

```
Streamlit Cloud Dashboard
├── [App của bạn]
│   ├── ⚙️ Settings
│   │   └── 🔐 Secrets  ← Click vào đây!
│   │       └── [Editor để paste cấu hình]
│   │           └── 💾 Save
```

## ⚠️ Lưu ý quan trọng

1. **Copy TOÀN BỘ** private_key (bao gồm cả `\n` ở cuối)
2. **Giữ nguyên format** - không thay đổi bất kỳ ký tự nào
3. **Đảm bảo** có dấu `[firebase]` ở đầu
4. **Sau khi save**, app sẽ tự động redeploy (có thể mất 1-2 phút)

## 🔍 Kiểm tra nếu vẫn lỗi

Nếu sau khi cấu hình vẫn còn lỗi:

1. **Kiểm tra lại Secrets:**
   - Vào Settings → Secrets
   - Đảm bảo có section `[firebase]`
   - Đảm bảo tất cả các trường đã được điền

2. **Kiểm tra format:**
   - Private key phải có `\n` ở cuối
   - Không có dấu ngoặc kép thừa
   - Format TOML đúng

3. **Reboot app:**
   - Vào Settings → General
   - Click **"Reboot app"** để force redeploy

## ✅ Sau khi cấu hình thành công

App sẽ:
- ✅ Kết nối Firebase thành công
- ✅ Hiển thị dữ liệu từ Firebase
- ✅ Không còn lỗi "No such file or directory"

---

**Nếu vẫn gặp vấn đề, vui lòng kiểm tra lại các bước trên hoặc liên hệ hỗ trợ.**

