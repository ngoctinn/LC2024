# TOEIC Listening Practice - Integrated Chunking Technique

Hệ thống luyện nghe TOEIC Part 3 & 4 ứng dụng kỹ thuật **Integrated Chunking (Gộp nhóm thông tin tích hợp)**.

## 🚀 Kỹ Thuật Chunking

Chunking là cơ chế nhóm các mảnh dữ liệu rời rạc thành các cấu trúc vĩ mô có ý nghĩa. Trong thực chiến TOEIC, kỹ thuật này giúp:

- **Vượt qua giới hạn trí nhớ ngắn hạn:** Thay vì nhớ từng từ đơn lẻ, chúng ta nhớ theo cụm (chunks).
- **Xử lý câu dài:** Giảm tải áp lực cho não bộ khi gặp các cấu trúc phức tạp.
- **Tăng tốc độ phản xạ:** Nhận diện ngay lập tức ý nghĩa của một nhóm từ thay vì phải dịch từng từ.

## 🛠 Tính Năng Hệ Thống

- **Sticky Audio Player:** Trình phát âm thanh luôn cố định ở đầu trang, hỗ trợ phím tắt (A-B loop, Speed control).
- **Interactive Sidebar:** Điều hướng nhanh giữa các bài học, tự động tập trung vào bài đang học.
- **Shadowing Flow:** Bản đọc chia theo cụm từ (chunks) kèm bản dịch tiếng Việt tương ứng.
- **Integrated Knowledge Table:** Bảng kiến thức tích hợp Chunks, IPA, Nghĩa và **Paraphrasing** (Cận ngôn) ngay trong một bảng.
- **Chunking Challenge:** Bài tập điền từ theo cụm để củng cố khả năng nhận diện chunks.

## 📚 Cấu Trúc Bài Học

Mỗi bài học được chia thành 4 phần chính:

1. **BẢN ĐỌC CHUNKING:** Nghe và nhìn theo các cụm từ ý nghĩa. (Đã loại bỏ các chỉ số câu hỏi như (32), (33) để tăng trải nghiệm tập trung).
2. **KIẾN THỨC TRỌNG TÂM:** Bảng tổng hợp các cụm từ quan trọng, cách chúng được diễn đạt lại (paraphrase) trong câu hỏi.
3. **ĐIỀN CỤM TỪ:** Thử thách điền các cụm từ chunks vào kịch bản bài nghe.
4. **CHẾ ĐỘ TỰ LUYỆN TẬP (NEW):** Hệ thống ẩn bản dịch tiếng Việt và giải thích. Người học phải chọn đáp án A, B, C, D và nhấn "Nộp bài" để xem kết quả và lời giải.

---

_Dữ liệu được cập nhật dựa trên kịch bản chuẩn ETS 2024._

## 🧭 Quy ước trình bày & Cách thêm lesson mới

Dưới đây là hướng dẫn chuẩn để bạn dễ dàng thêm một lesson mới vào kho học. Thao tác đúng theo các bước sẽ giúp hệ thống tự nhận diện audio, sidebar và tính năng chunking.

### 1) Quy ước trình bày kịch bản (Transcription Standards)

Để đảm bảo trải nghiệm shadowing tốt nhất, kịch bản (transcript) cần tuân thủ:
- **Loại bỏ chỉ số câu hỏi:** Không để các dấu ngoặc số như `(32)`, `(33)` trong phần Bản đọc Chunking.
- **Phân tách Chunk:** Sử dụng dấu `/` để ngăn cách các cụm từ có nghĩa.
- **Đồng bộ tiếng Việt:** Bản dịch trong `.chunk-vi` phải có số lượng dấu `/` khớp hoàn toàn với bản tiếng Anh trong `<strong>`.

### 2) Đặt file HTML

- File lesson phải theo định dạng tên: `LC-T{testNum}-P{part}-Q{range}.html`
  - Ví dụ: `LC-T4-P3-Q32-34.html` (Test 4, Part 3, câu 32–34)
- Đặt file vào thư mục tương ứng (ví dụ `Test 4/`).

### 2) Đặt audio

- Tên file audio phải theo định dạng: `Test_{NN}-{range}.mp3` (với `NN` là số test 2 chữ số)
  - Ví dụ: `Test_04-32-34.mp3`
- Đặt file audio vào `audio/Test_{NN}/` (ví dụ `audio/Test_04/Test_04-32-34.mp3`).
- Hệ thống sẽ tự ghép đường dẫn dựa trên file HTML khi khởi tạo audio player.

### 3) Cấu trúc HTML cơ bản cho lesson

- Các thành phần chính mà script tìm kiếm:
  - Một phần chứa `strong` cho bản đọc tiếng Anh (chunking) và một phần `.chunk-vi` cho bản dịch.
  - Container có id `shadowingContainer` để script `enhanceChunkingLayout()` tự động tách chunk.

- Mẫu HTML tối thiểu (dán vào file lesson):

```html
<div id="shadowingContainer">
  <div class="flex gap-4">
    <div class="w-full">
      <strong>
        Thanks for taking my call. / As I mentioned in my e-mail, / I'm
        interested in working / in your field.
      </strong>
      <div class="chunk-vi">
        Cảm ơn đã nhận cuộc gọi của tôi. / Như tôi đã đề cập trong e-mail, / Tôi
        quan tâm đến việc làm / trong lĩnh vực của bạn.
      </div>
    </div>
  </div>
</div>
```

Lưu ý: dấu `/` dùng để tách chunk; script sẽ thay thế `/` thành phân đoạn và hiển thị pseudo-element `/` giữa các chunk.

### 4) Cập nhật sidebar / navigation (nếu cần thủ công)

- Hầu hết các bài được phát hiện tự động theo cấu trúc thư mục, nhưng nếu bạn muốn cập nhật thủ công hoặc thêm nhãn riêng, chỉnh arrays `TOEIC_TESTS` trong `assets/script.js`.

### 5) Kiểm tra nhanh sau khi thêm

- Mở file HTML trong trình duyệt (môi trường local). Nếu audio không xuất hiện, kiểm tra tên file audio và thư mục.
- Xác nhận rằng các chunk hiển thị đúng và không bị dồn sát (nếu cần chỉnh CSS, xem `assets/style.css`).

### 6) Checklist ngắn

- [ ] File HTML theo tên chuẩn
- [ ] Audio có tên + đặt đúng folder
- [ ] `shadowingContainer` tồn tại và chứa `strong` + `.chunk-vi`
- [ ] Mở trang kiểm tra hiển thị chunk và audio

Nếu bạn muốn, mình có thể tạo một script nhỏ (CLI) để tự động sinh file HTML template và đặt audio path — bạn muốn mình làm không?
