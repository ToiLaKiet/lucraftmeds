# LuCraftMeds

LuCraftMeds là dự án Retrieval-Augmented Generation (RAG), được tổ chức thành
hai phần độc lập: backend xử lý dữ liệu và truy vấn, cùng frontend phục vụ giao
diện người dùng.

> Dự án hiện đang ở giai đoạn khởi tạo cấu trúc. Các module, dependency và lệnh
> chạy sẽ được bổ sung trong quá trình phát triển.

## Cấu trúc dự án

```text
lucraftmeds/
├── lucraftmeds@be/       # Backend và RAG pipeline
├── lucraftmeds@fe/       # Frontend
├── .gitignore
└── README.md
```

Toàn bộ mã nguồn và tài nguyên của backend nằm trong `lucraftmeds@be/`. Vì vậy,
các lệnh liên quan đến Python, indexing, API hoặc test cần được chạy từ thư mục
này.

### Backend

| Đường dẫn | Vai trò |
| --- | --- |
| `lucraftmeds@be/main.py` | Entry point của ứng dụng backend. |
| `lucraftmeds@be/config.yaml` | Cấu hình model, chunking, index, database, cache và evaluation. |
| `lucraftmeds@be/requirements.txt` | Danh sách dependency Python. |
| `lucraftmeds@be/.env` | Biến môi trường và API key; không commit file này lên Git. |
| `lucraftmeds@be/data/` | Tài liệu nguồn, dữ liệu đã xử lý và bộ dữ liệu đánh giá. |
| `lucraftmeds@be/schemas/` | Các schema cho document, chunk và kết quả truy vấn. |
| `lucraftmeds@be/ingestion/` | Connector và parser cho PDF, HTML, bảng, OCR và website. |
| `lucraftmeds@be/chunking/` | Chiến lược chia nhỏ tài liệu và quản lý giới hạn token. |
| `lucraftmeds@be/embeddings/` | Sinh embedding và quản lý phiên bản embedding model. |
| `lucraftmeds@be/vectordb/` | Tích hợp và thao tác với vector database. |
| `lucraftmeds@be/lexical/` | BM25 và keyword index cho hybrid search. |
| `lucraftmeds@be/retrieval/` | Truy xuất hybrid, metadata filter và hợp nhất kết quả. |
| `lucraftmeds@be/rerank/` | Rerank các kết quả truy xuất. |
| `lucraftmeds@be/query/` | Query rewriting, routing, multi-query và HyDE. |
| `lucraftmeds@be/cache/` | Exact cache và semantic cache. |
| `lucraftmeds@be/prompts/` | Các prompt template có quản lý phiên bản. |
| `lucraftmeds@be/generation/` | Sinh câu trả lời có căn cứ và trích dẫn nguồn. |
| `lucraftmeds@be/api/` | Lớp API phục vụ indexing và truy vấn. |
| `lucraftmeds@be/pipelines/` | Pipeline indexing offline và query online. |
| `lucraftmeds@be/jobs/` | Các tác vụ indexing, reindexing và evaluation định kỳ. |
| `lucraftmeds@be/eval/` | Đánh giá faithfulness, recall@k và chất lượng RAG. |
| `lucraftmeds@be/observability/` | Trace, latency, chi phí và quality metrics. |
| `lucraftmeds@be/security/` | Xác thực, phân quyền theo chunk và xử lý dữ liệu nhạy cảm. |
| `lucraftmeds@be/tests/` | Unit test, integration test và retrieval regression test. |
| `lucraftmeds@be/logs/` | Log phục vụ theo dõi và debug. |
| `lucraftmeds@be/utils/` | Các tiện ích dùng chung. |

### Frontend

Mã nguồn giao diện được đặt trong `lucraftmeds@fe/` và được phát triển độc lập
với backend.

## Luồng xử lý dự kiến

```text
Tài liệu
  -> Ingestion
  -> Chunking
  -> Embeddings + Lexical index
  -> Vector database
  -> Retrieval
  -> Rerank
  -> Generation
  -> Câu trả lời kèm nguồn tham chiếu
```

## Thiết lập backend

Di chuyển vào thư mục backend trước khi tạo môi trường hoặc chạy các lệnh
Python:

```bash
cd lucraftmeds@be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tạo `lucraftmeds@be/.env` trên máy local để lưu các biến môi trường cần thiết.
Không đưa API key hoặc thông tin nhạy cảm vào mã nguồn.

Sau khi `main.py`, `requirements.txt` và `config.yaml` được hoàn thiện, backend
sẽ được khởi động từ `lucraftmeds@be/`. Lệnh chạy cụ thể sẽ được cập nhật tại
đây cùng với entry point của ứng dụng.

## Quy ước phát triển

- Chạy lệnh backend từ `lucraftmeds@be/`.
- Đặt test trong `lucraftmeds@be/tests/`.
- Không commit `.env`, log, dữ liệu nhạy cảm hoặc dữ liệu sinh ra khi chạy.
- Cập nhật README khi bổ sung entry point, dependency hoặc dịch vụ hạ tầng mới.
