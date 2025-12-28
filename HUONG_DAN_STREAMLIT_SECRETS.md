# Hướng dẫn cấu hình Firebase trên Streamlit Cloud

## Vấn đề
File `firebase-key.json` chứa thông tin nhạy cảm (private key) nên **KHÔNG NÊN** commit lên GitHub. GitHub sẽ tự động chặn push nếu phát hiện secret.

## Giải pháp: Dùng Streamlit Secrets

### Bước 1: Lấy nội dung file firebase-key.json
Mở file `firebase-key.json` và copy toàn bộ nội dung JSON.

### Bước 2: Cấu hình trên Streamlit Cloud

1. Vào **Streamlit Cloud Dashboard**: https://share.streamlit.io/
2. Chọn app của bạn
3. Click **"Settings"** (⚙️) ở góc dưới bên trái
4. Click **"Secrets"** trong menu
5. Thêm cấu hình sau:

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

**Lưu ý quan trọng:**
- Copy **toàn bộ** private_key (bao gồm cả `\n` ở cuối)
- Giữ nguyên format `\n` trong private_key
- Click **"Save"** sau khi thêm

### Bước 3: Deploy lại app
Sau khi lưu secrets, Streamlit Cloud sẽ tự động redeploy app. App sẽ tự động đọc credentials từ secrets.

## Cách hoạt động

Code đã được cập nhật để:
1. **Ưu tiên** đọc từ Streamlit Secrets (cho production/cloud)
2. **Fallback** về file `firebase-key.json` (cho development local)

## Lợi ích

✅ **Bảo mật**: Credentials không bị lộ trên GitHub  
✅ **An toàn**: Streamlit Cloud mã hóa và bảo vệ secrets  
✅ **Dễ quản lý**: Có thể cập nhật secrets mà không cần commit code mới

