# Data Creation Notebooks

Thư mục này chứa các notebook dùng để khảo sát URL, crawl nội dung web và tạo dữ liệu Markdown cho Lucraftmeds.

Các notebook được chia thành hai luồng chính:

1. **Crawl toàn bộ corpus** trên Kaggle và lưu checkpoint trực tiếp lên Google Drive.
2. **Phân tích domain/layout**, sau đó lấy 10 bài từ mỗi domain để LLM đánh giá chất lượng dữ liệu.

## Cấu trúc thư mục

```text
data-creation/
├── crawl4ai-dataset-crawl/
│   ├── v1-crawl4ai-html-to-md.ipynb
│   └── merge-batches.ipynb
├── domains-analyzation/
│   ├── domains-analysis.ipynb
│   └── domain_profiling_output/
│       └── domain_profiles.json
└── reapeated-pattern-analysis/
    └── md-urls-pattern-crawl.ipynb
```

## 1. `v1-crawl4ai-html-to-md.ipynb`

**Vị trí:** `crawl4ai-dataset-crawl/`

Notebook chính để crawl dữ liệu từ các URL trong corpus `AIGuruTinix/ViBioMIR` trên Kaggle.

Chức năng:

- Chia danh sách URL thành các shard để nhiều worker có thể chạy song song.
- Dùng Crawl4AI để tải HTML và chuyển nội dung sang Markdown.
- Phân loại kết quả thành công và lỗi trong cùng bản ghi JSONL thông qua trường `success`.
- Sau mỗi batch, upload checkpoint trực tiếp từ RAM lên thư mục Google Drive dùng chung.
- Đọc lịch sử đã crawl của ngày hôm trước để tránh xử lý lại URL.
- Không cần ghi toàn bộ kết quả crawl xuống ổ đĩa cục bộ của Kaggle.

Đầu vào chính:

- Dataset `AIGuruTinix/ViBioMIR`, cấu hình `corpus`.
- Kaggle Secret `GOOGLE_DRIVE_TOKEN`.
- Các cấu hình worker như `WORKER_ID`, `NUM_WORKERS`, `BATCH_SIZE` và `DRIVE_FOLDER_ID`.

Đầu ra:

```text
worker_<worker-id>_batch_<timestamp>_<uuid>.jsonl
```

Các file batch được ghi trực tiếp vào thư mục Google Drive đã cấu hình. Mỗi file chứa cả kết quả crawl thành công và lỗi.

## 2. `merge-batches.ipynb`

**Vị trí:** `crawl4ai-dataset-crawl/`

Notebook checkpoint dùng để gom các batch được tạo bởi `v1-crawl4ai-html-to-md.ipynb` sau mỗi phiên chạy Kaggle.

Chức năng:

- Đọc các file `worker_*_batch_*.jsonl` trong thư mục Drive dùng chung.
- Kết hợp batch mới với kết quả tích lũy của hôm qua và hôm nay.
- Loại URL trùng lặp.
- Ưu tiên bản ghi crawl thành công nếu một URL tồn tại ở cả tập thành công và tập lỗi.
- Ghi kết quả theo ngày để notebook crawler có thể dùng làm lịch sử skip trong lần chạy tiếp theo.
- Không xóa các batch nguồn sau khi gộp.

Đầu ra:

```text
results/DD-MM-YYYY/
├── success.jsonl
└── errors.jsonl
```

Notebook ghi vào file tạm `.part` trước, sau đó mới thay thế file kết quả chính nhằm hạn chế tạo file dở dang khi quá trình gộp bị gián đoạn.

## 3. `domains-analysis.ipynb`

**Vị trí:** `domains-analyzation/`

Notebook phân tích phân bố domain và profile cấu trúc trang theo URL pattern.

Chức năng:

- Thống kê các domain xuất hiện trong corpus URL.
- Nhóm URL thành các pattern đại diện.
- Lấy mẫu URL theo từng domain và pattern.
- Crawl mẫu để nhận diện loại trang, selector tiêu đề, selector nội dung, metadata, phân trang và mức phụ thuộc JavaScript.
- Phát hiện domain có khả năng sử dụng nhiều template/layout.
- Hỗ trợ checkpoint để có thể tiếp tục quá trình profiling khi bị gián đoạn.

Đầu ra chính:

```text
domains-analyzation/domain_profiling_output/domain_profiles.json
```

File này chứa profile của từng domain cùng danh sách template và `url_pattern` tương ứng.

## 4. `md-urls-pattern-crawl.ipynb`

**Vị trí:** `reapeated-pattern-analysis/`

Notebook crawl dữ liệu Markdown mẫu theo 97 domain để chuẩn bị dataset cho LLM phân tích và đánh giá chất lượng nội dung.

Chức năng:

- Đọc trực tiếp 97 domain từ `domain_profiles.json`; bỏ qua toàn bộ template và URL pattern.
- Quét corpus để tìm URL thuộc từng domain.
- Chọn tối đa 30 URL ứng viên ổn định theo seed cho mỗi domain, tránh chỉ lấy các URL đầu tiên trong corpus.
- Crawl đến khi đủ 10 bài thành công cho mỗi domain hoặc hết URL ứng viên.
- Crawl URL bằng Crawl4AI và chuyển HTML sang Markdown.
- Lưu checkpoint riêng cho từng domain để có thể tiếp tục sau khi dừng.
- Ghi lại cả dữ liệu crawl thành công và toàn bộ lần thử/lỗi để phục vụ kiểm tra.

Đầu vào chính:

```text
domains-analyzation/domain_profiling_output/domain_profiles.json
```

Đầu ra mặc định trong thư mục `pattern_cleanliness/`:

```text
pattern_cleanliness/
├── selected_urls.json
├── dataset.jsonl
├── crawl_attempts.jsonl
├── domain_summary.csv
├── run_settings.json
└── checkpoints/
```

Trong đó:

- `selected_urls.json`: URL thật được chọn cho từng domain.
- `dataset.jsonl`: các bản ghi Markdown crawl thành công, dùng làm dữ liệu đầu vào cho LLM.
- `crawl_attempts.jsonl`: toàn bộ lần crawl, bao gồm cả thành công và thất bại.
- `domain_summary.csv`: thống kê kết quả theo từng domain.
- `run_settings.json`: cấu hình của lần chạy.
- `checkpoints/`: trạng thái crawl của từng pattern.

`success=true` chỉ cho biết Crawl4AI lấy được Markdown và không phát hiện trang chặn. Nó chưa khẳng định nội dung sạch, đúng bài viết hoặc phù hợp để huấn luyện; phần này cần được LLM đánh giá ở bước tiếp theo.

## Luồng chạy notebook

### Luồng A — Crawl toàn bộ corpus

```text
AIGuruTinix/ViBioMIR corpus
        │
        ▼
v1-crawl4ai-html-to-md.ipynb
        │
        ▼
worker_*_batch_*.jsonl trên Google Drive
        │
        ▼
merge-batches.ipynb
        │
        ├── results/DD-MM-YYYY/success.jsonl
        └── results/DD-MM-YYYY/errors.jsonl
```

Thứ tự đề xuất:

1. Chạy `v1-crawl4ai-html-to-md.ipynb` trên Kaggle cho từng worker.
2. Sau mỗi session hoặc sau khi các worker hoàn thành, chạy `merge-batches.ipynb` để tạo checkpoint tích lũy theo ngày.
3. Ở session Kaggle tiếp theo, crawler đọc lịch sử ngày hôm trước và bỏ qua các URL đã được xử lý.

### Luồng B — Lấy mẫu theo domain cho LLM

```text
AIGuruTinix/ViBioMIR corpus
    │
    ▼
domains-analysis.ipynb
    │
    ▼
domain_profiles.json (97 domain)
    │
    ▼
md-urls-pattern-crawl.ipynb
    │
    ▼
970 bài tối đa + crawl_attempts.jsonl + domain_summary.csv
    │
    ▼
LLM phân tích độ sạch và chất lượng nội dung
```

Thứ tự chạy:

1. Chạy `domains-analysis.ipynb` để tạo `domain_profiles.json` chứa 97 domain.
2. Kiểm tra `DOMAINS_FILE` trong `md-urls-pattern-crawl.ipynb` nếu đường dẫn đầu vào khác mặc định.
3. Chạy `md-urls-pattern-crawl.ipynb`; notebook bỏ qua URL pattern và lấy tối đa 10 bài thành công/domain.
4. Dùng `dataset.jsonl` làm đầu vào cho bước đánh giá bằng LLM.

## Lưu ý vận hành

- Không chạy nhiều phiên `merge-batches.ipynb` cùng lúc trên cùng thư mục Drive.
- Các worker Kaggle phải dùng cùng cấu hình chia shard và có `WORKER_ID` khác nhau.
- Kiểm tra quyền ghi Google Drive và Kaggle Secret trước khi chạy crawler.
- Không xem mọi bản ghi `success=true` là dữ liệu sạch; cần đánh giá nội dung ở pipeline phía sau.
- Khi thay đổi danh sách domain hoặc cấu hình chọn mẫu, nên dùng một thư mục output mới để tránh trộn checkpoint không tương thích.
