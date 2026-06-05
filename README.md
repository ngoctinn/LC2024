# TOEIC Listening Coach - Project Instructions

Tài liệu này hướng dẫn cách tạo các bài học TOEIC Listening tương tác theo chuẩn định dạng hiện tại.

## 1. Cấu trúc Thư mục & Assets
- **Gốc:** `/home/ngoctin/Documents/Study/LC2024/`
- **Assets:** `/home/ngoctin/Documents/Study/LC2024/assets/`
  - `style.css`: Chứa toàn bộ giao diện và class dùng chung (glass-card, input-blank, main-container...).
  - `script.js`: Chứa logic tương tác (ẩn/hiện dịch, check đáp án) và tự động inject Navigation.
- **Thư mục con:** `Test [Số]/` (Ví dụ: `Test 1`, `Test 2`...)
- **Tên file:** `LC-T[Số]-P[Phần]-Q[Số câu].html` (Ví dụ: `LC-T1-P3-Q65-67.html`)

## 2. Quy tắc Nội dung (Format chuẩn)
Mỗi file HTML mới cần link đến assets dùng chung để đảm bảo tính đồng bộ:
- `<link rel="stylesheet" href="../assets/style.css">`
- `<script src="../assets/script.js"></script>`

Các file bài học phải bao gồm 4 Module chính bên trong `<div class="main-container space-y-8">`:

### Module 1: BẢN ĐỌC CHUNKING
- **Quy tắc:** 1 dòng Tiếng Anh (In đậm) - 1 dòng Tiếng Việt (Dưới, màu xám nhạt).
- **Tính năng:** Tự động hỗ trợ bởi `script.js` (Nút "Ẩn/Hiện tiếng Việt").

### Module 2: TỪ VỰNG TRỌNG TÂM
- Bảng 2 cột: `Từ vựng & Phiên âm` | `Ý nghĩa`.
- Sử dụng class `glass-card` cho container và `table-header` cho header bảng.

### Module 3: ĐIỀN TỪ
- Hiển thị script với các ô `<input class="input-blank" data-answer="...">`.
- Nút "Kiểm tra Đáp án" (`id="checkAnswersBtn"`) sẽ tự động xử lý logic qua `script.js`.

### Module 4: CÂU HỎI BÀI TẬP
- Hiển thị câu hỏi + 4 đáp án (A, B, C, D).
- **Song ngữ:** Luôn có dịch tiếng Việt bên dưới mỗi câu hỏi/lựa chọn.

## 3. Tech Stack
- **Framework:** Tailwind CSS (CDN) cho layout nhanh.
- **Styling:** Vanilla CSS (`assets/style.css`) cho các component đặc thù.
- **Icons:** Font Awesome 6.
- **Logic:** Vanilla JavaScript (`assets/script.js`) - Xử lý tập trung.

---
*Ghi chú cho Agent: Khi tạo bài học mới, không copy-paste code CSS/JS vào file HTML. Chỉ cần link đến assets và sử dụng đúng ID/Class quy định.*
