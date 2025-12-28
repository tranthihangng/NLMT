# 🌓 Hướng dẫn sử dụng Theme và Xử lý dữ liệu

## 🎨 Chuyển đổi giao diện Sáng/Tối

### Cách sử dụng:
1. Mở sidebar (bên trái)
2. Tìm phần **"🎨 Giao diện"**
3. Click vào nút:
   - **🌙 Tối**: Chuyển sang giao diện tối (dark mode)
   - **☀️ Sáng**: Chuyển sang giao diện sáng (light mode)

### Tính năng:
- ✅ Tự động lưu lựa chọn trong phiên làm việc
- ✅ Áp dụng ngay lập tức cho toàn bộ giao diện
- ✅ Màu sắc được tối ưu cho cả 2 chế độ

---

## 🔧 Xử lý dữ liệu 0 từ Firebase

### Vấn đề:
Khi phần cứng không truyền dữ liệu liên tục, Firebase có thể trả về giá trị 0 không hợp lý (ví dụ: có ánh sáng nhưng công suất = 0).

### Giải pháp:
Hệ thống cung cấp 5 phương pháp xử lý trong sidebar:

#### 1. **Smart** (Mặc định - Khuyến nghị)
- Kết hợp forward fill và backward fill
- Lấy giá trị gần nhất (trước hoặc sau)
- Phù hợp cho hầu hết trường hợp

#### 2. **Forward Fill**
- Lấy giá trị gần nhất **trước đó**
- Phù hợp khi dữ liệu mới nhất thường đáng tin hơn

#### 3. **Backward Fill**
- Lấy giá trị gần nhất **sau đó**
- Phù hợp khi dữ liệu cũ hơn đáng tin hơn

#### 4. **Interpolate**
- Nội suy tuyến tính giữa các giá trị
- Tạo giá trị mượt mà, liên tục
- Phù hợp cho phân tích xu hướng

#### 5. **Remove**
- Xóa hoàn toàn các dòng có giá trị 0 không hợp lý
- Chỉ giữ lại dữ liệu hợp lệ
- Phù hợp khi muốn dữ liệu chính xác 100%

---

## 📊 Trạng thái dữ liệu

Hệ thống tự động hiển thị trạng thái dữ liệu:

- **🟢 Dữ liệu mới**: Dữ liệu hợp lệ, được cập nhật gần đây (< 5 phút)
- **🟡 Dữ liệu cũ**: Dữ liệu có nhiều giá trị 0 hoặc cập nhật > 5 phút
- **🔴 Không có dữ liệu**: Không tìm thấy dữ liệu cho thời gian đã chọn

---

## ⚙️ Cấu hình

### Trong Sidebar:
1. **🔧 Xử lý dữ liệu**: Chọn phương pháp xử lý giá trị 0
2. **⚙️ Thông số tấm pin**: Cấu hình thông số kỹ thuật tấm pin

### Ngưỡng phát hiện giá trị 0 không hợp lý:
- **Điện áp (U)**: < 0.1V
- **Dòng điện (Current)**: < 0.001A
- **Công suất (milliWatt)**: < 1.0mW
- **Ánh sáng (Lux)**: < 10 Lux (có thể là ban đêm)
- **Nhiệt độ (Temp)**: < -50°C
- **Độ ẩm (Humi)**: < 0%

**Lưu ý đặc biệt**: Nếu có ánh sáng (Lux > 100) nhưng công suất = 0, hệ thống sẽ coi là dữ liệu không hợp lý.

---

## 💡 Gợi ý sử dụng

### Khi nào dùng phương pháp nào?

1. **Smart**: Dùng mặc định cho mọi trường hợp
2. **Forward Fill**: Khi dữ liệu mới nhất thường đáng tin
3. **Backward Fill**: Khi dữ liệu cũ hơn đáng tin hơn
4. **Interpolate**: Khi cần biểu đồ mượt mà, phân tích xu hướng
5. **Remove**: Khi cần dữ liệu chính xác 100%, không muốn nội suy

### Ví dụ:
- **Giám sát real-time**: Dùng **Smart** hoặc **Forward Fill**
- **Phân tích lịch sử**: Dùng **Interpolate** để có biểu đồ mượt
- **Báo cáo chính xác**: Dùng **Remove** để chỉ hiển thị dữ liệu thực tế

---

## 🔍 Kiểm tra chất lượng dữ liệu

Hệ thống tự động kiểm tra:
- ✅ Giá trị 0 không hợp lý
- ✅ Mất cân bằng V-I-P (Voltage × Current ≠ Power)
- ✅ Thời gian cập nhật dữ liệu
- ✅ Điều kiện môi trường (ánh sáng vs công suất)

---

## 📝 Lưu ý

1. **Theme** được lưu trong session, sẽ reset khi refresh trang
2. **Phương pháp xử lý dữ liệu** có thể thay đổi bất cứ lúc nào
3. Dữ liệu được cache 30 giây để tối ưu hiệu suất
4. Click nút **🔄 Làm mới dữ liệu** để xóa cache và tải lại

---

**Chúc bạn sử dụng hiệu quả! 🚀**

