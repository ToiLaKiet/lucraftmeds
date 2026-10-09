```mermaid
sequenceDiagram
    participant UI as Frontend
    participant API as Backend
    participant RAG as Retrieval
    participant LLM as Model

    UI->>UI: Hiển thị câu hỏi và ô trả lời trống
    UI->>API: POST /api/chat/stream
    API-->>UI: start
    API-->>UI: status: retrieving
    API->>RAG: Tìm tài liệu liên quan
    RAG-->>API: Context và nguồn
    API-->>UI: sources
    API->>LLM: Prompt + context, bật streaming
    loop Khi model sinh thêm nội dung
        LLM-->>API: Text delta
        API-->>UI: delta
        UI->>UI: Nối nội dung vào ô trả lời
    end
    API->>API: Lưu câu trả lời hoàn chỉnh
    API-->>UI: done
