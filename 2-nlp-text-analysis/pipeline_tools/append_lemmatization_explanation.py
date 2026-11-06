import json

file_path = 'd:/PROJECT/phantichdulieu/Phân_tích_python.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_add = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Giải thích: Stemming vs Lemmatization trong Tiếng Việt\n',
            '\n',
            '**Quyết định:** Chọn **Lemmatization** (thể hiện qua bước Chuẩn hóa Teencode).\n',
            '\n',
            '**Giải thích lý do:**\n',
            '\n',
            '1. **Đặc điểm hình thái của Tiếng Việt:** Khác với tiếng Anh (ngôn ngữ hòa kết), tiếng Việt là ngôn ngữ đơn lập (isolating language). Từ ngữ trong tiếng Việt không bao giờ biến đổi hình thái (không chia động từ, không thêm `s/es/ed/ing`). Do đó, thuật toán **Stemming** (cắt bỏ tiền tố/hậu tố để lấy thân từ, ví dụ `running` -> `run`) là **không thể áp dụng** và vô nghĩa đối với tiếng Việt.\n',
            '\n',
            '2. **Lemmatization trong ngữ cảnh Tiếng Việt:** Bản chất của Lemmatization là đưa từ bị biến đổi về dạng nguyên thể (lemma) chuẩn trong từ điển. Trên mạng xã hội hay thương mại điện tử, sự "biến dạng" của tiếng Việt không đến từ ngữ pháp, mà đến từ thói quen viết tắt, sai chính tả, từ lóng (ví dụ: `ko`, `k`, `khg` đều là biến thể của `không`; `sp` là `sản phẩm`; `dc` là `được`).\n',
            '\n',
            '3. **Kết luận:** Quá trình tạo và áp dụng **Từ điển Teencode** để quy chuẩn các từ lóng/viết tắt về từ gốc tiếng Việt ở các bước trên chính là cách tiếp cận **Lemmatization tối ưu nhất** cho bài toán này. Nó giúp thu gọn không gian đặc trưng (vocabulary) và giữ lại đúng ý nghĩa gốc của từ mà không cần đến các thuật toán Stemming dư thừa.'
        ]
    }
]

nb['cells'].extend(cells_to_add)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Appended Lemmatization explanation.")
