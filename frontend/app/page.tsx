"use client";

import { FormEvent, useState } from "react";

type IconName =
  | "book"
  | "shield"
  | "activity"
  | "search"
  | "document"
  | "heart"
  | "stethoscope"
  | "clip"
  | "send"
  | "sparkles";

function Icon({ name, className = "h-5 w-5" }: { name: IconName; className?: string }) {
  const paths: Record<IconName, React.ReactNode> = {
    book: <><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H11v16H6.5A2.5 2.5 0 0 0 4 21.5v-16Z" /><path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H13v16h4.5a2.5 2.5 0 0 1 2.5 2.5v-16Z" /></>,
    shield: <path d="M12 22s8-3.8 8-10V5l-8-3-8 3v7c0 6.2 8 10 8 10Z" />,
    activity: <path d="M3 12h4l2.5-7 5 14 2.5-7h4" />,
    search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
    document: <><path d="M6 2h8l4 4v16H6z" /><path d="M14 2v5h4M9 12h6M9 16h6" /></>,
    heart: <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z" />,
    stethoscope: <><path d="M6 3v5a4 4 0 0 0 8 0V3M4 3h4M12 3h4M10 13v2a5 5 0 0 0 10 0v-1" /><circle cx="20" cy="11" r="2" /></>,
    clip: <path d="m21.4 11.6-8.9 8.9a6 6 0 0 1-8.5-8.5l9.6-9.6a4 4 0 0 1 5.7 5.7l-9.6 9.6a2 2 0 1 1-2.8-2.8l8.9-8.9" />,
    send: <path d="m22 2-7 20-4-9-9-4 20-7ZM11 13 22 2" />,
    sparkles: <path d="m12 3 1.2 3.3L16.5 7.5l-3.3 1.2L12 12l-1.2-3.3-3.3-1.2 3.3-1.2L12 3ZM5 14l.9 2.1L8 17l-2.1.9L5 20l-.9-2.1L2 17l2.1-.9L5 14ZM19 13l.8 1.8 1.7.7-1.7.7L19 18l-.8-1.8-1.7-.7 1.7-.7L19 13Z" />,
  };

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  );
}

const suggestions = [
  { icon: "stethoscope" as const, title: "Tra cứu triệu chứng", description: "Đau đầu kéo dài có thể liên quan đến những nguyên nhân nào?", color: "bg-blue-50 text-blue-600" },
  { icon: "document" as const, title: "Đọc kết quả xét nghiệm", description: "Giải thích các chỉ số thường gặp trong xét nghiệm máu.", color: "bg-violet-50 text-violet-600" },
  { icon: "heart" as const, title: "Chăm sóc sức khỏe", description: "Gợi ý chế độ sinh hoạt tốt cho sức khỏe tim mạch.", color: "bg-rose-50 text-rose-600" },
];

type Message = { id: number; role: "user" | "assistant"; content: string };

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);

  const sendMessage = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const question = input.trim();
    if (!question) return;
    setMessages((current) => [
      ...current,
      { id: Date.now(), role: "user", content: question },
      { id: Date.now() + 1, role: "assistant", content: "Tôi đã tìm thấy một số thông tin liên quan trong kho dữ liệu y khoa. Để đưa ra hướng dẫn phù hợp, bạn có thể mô tả thêm thời điểm xuất hiện, mức độ và các triệu chứng đi kèm. Nếu triệu chứng nghiêm trọng hoặc diễn tiến nhanh, hãy liên hệ cơ sở y tế gần nhất." },
    ]);
    setInput("");
  };

  return (
    <div className="flex h-[100dvh] min-h-[640px] overflow-hidden bg-[#f7f9fc] font-sans text-slate-900">
      <section className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 shrink-0 items-center border-b border-slate-200/80 bg-white/90 px-5 backdrop-blur sm:px-8">
          <div className="flex items-center gap-3">
            <div className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 shadow-md shadow-blue-500/20">
              <span className="absolute h-4 w-1.5 rounded-full bg-white" />
              <span className="absolute h-1.5 w-4 rounded-full bg-white" />
            </div>
            <h1 className="text-lg font-bold tracking-tight text-slate-900">LucraftMeds</h1>
          </div>
        </header>

        <main className="flex min-h-0 flex-1 flex-col overflow-y-auto">
          {messages.length === 0 ? (
            <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-5 py-10 sm:px-8 lg:py-14">
              <div className="mx-auto w-full max-w-3xl text-center">
                <div className="mb-3 inline-flex items-center gap-1.5 rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-[11px] font-semibold text-blue-700"><Icon name="sparkles" className="h-3.5 w-3.5" />AI hỗ trợ tra cứu y khoa</div>
                <h2 className="text-balance text-2xl font-bold tracking-[-0.03em] text-slate-900 sm:text-3xl lg:text-[34px]">Xin chào, tôi có thể hỗ trợ gì cho bạn?</h2>
                <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-500 sm:text-[15px]">Đặt câu hỏi về sức khỏe và nhận thông tin được tổng hợp từ các nguồn y khoa đáng tin cậy, kèm tài liệu tham khảo rõ ràng.</p>
              </div>

              <div className="mx-auto mt-8 grid w-full max-w-4xl gap-3 sm:grid-cols-3">
                {suggestions.map((suggestion) => (
                  <button key={suggestion.title} onClick={() => setInput(suggestion.description)} className="group rounded-2xl border border-slate-200 bg-white p-4 text-left shadow-sm transition duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/60 focus:outline-none focus:ring-4 focus:ring-blue-100">
                    <div className={`mb-3 flex h-9 w-9 items-center justify-center rounded-xl ${suggestion.color}`}><Icon name={suggestion.icon} className="h-[18px] w-[18px]" /></div>
                    <p className="text-sm font-semibold text-slate-800">{suggestion.title}</p><p className="mt-1.5 text-xs leading-5 text-slate-500">{suggestion.description}</p>
                  </button>
                ))}
              </div>

              <div className="mx-auto mt-5 flex w-full max-w-4xl items-start gap-3 rounded-xl border border-amber-100 bg-amber-50/70 px-4 py-3 text-xs leading-5 text-amber-900/70">
                <Icon name="shield" className="mt-0.5 h-4 w-4 shrink-0 text-amber-600" /><p>LucraftMeds cung cấp thông tin tham khảo, không thay thế chẩn đoán hoặc chỉ định điều trị từ bác sĩ. Trong trường hợp khẩn cấp, hãy gọi 115.</p>
              </div>
            </div>
          ) : (
            <div className="mx-auto w-full max-w-3xl flex-1 space-y-7 px-5 py-8 sm:px-8">
              <div className="flex items-center justify-center"><span className="rounded-full border border-slate-200 bg-white px-3 py-1 text-[11px] text-slate-400">Hôm nay</span></div>
              {messages.map((message) => (
                <div key={message.id} className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                  {message.role === "assistant" && <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 text-white shadow-md shadow-blue-500/20"><Icon name="activity" className="h-5 w-5" /></div>}
                  <div className="max-w-[85%]">
                    <div className={`rounded-2xl px-4 py-3 text-sm leading-6 shadow-sm ${message.role === "user" ? "rounded-tr-md bg-blue-600 text-white shadow-blue-600/10" : "rounded-tl-md border border-slate-200 bg-white text-slate-600"}`}>{message.content}</div>
                    {message.role === "assistant" && (
                      <div className="mt-2 rounded-xl border border-blue-100 bg-blue-50/70 p-3">
                        <div className="flex items-center gap-2 text-xs font-semibold text-blue-800"><Icon name="book" className="h-4 w-4" />Nguồn tham khảo</div>
                        <div className="mt-2 flex items-center justify-between rounded-lg bg-white px-3 py-2 text-[11px] text-slate-500"><span className="truncate">Hướng dẫn chăm sóc sức khỏe cộng đồng</span><span className="ml-3 shrink-0 font-medium text-blue-600">Độ phù hợp 94%</span></div>
                      </div>
                    )}
                  </div>
                  {message.role === "user" && <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-800 text-[10px] font-bold text-white">ND</div>}
                </div>
              ))}
            </div>
          )}
        </main>

        <footer className="shrink-0 border-t border-slate-200/80 bg-white px-4 pb-3 pt-3 sm:px-6 sm:pb-4">
          <form onSubmit={sendMessage} className="mx-auto max-w-3xl">
            <div className="rounded-2xl border border-slate-200 bg-white p-2 shadow-[0_8px_30px_rgba(15,23,42,0.08)] transition focus-within:border-blue-300 focus-within:ring-4 focus-within:ring-blue-50">
              <textarea rows={1} value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); event.currentTarget.form?.requestSubmit(); } }} placeholder="Nhập câu hỏi về sức khỏe của bạn..." aria-label="Nội dung câu hỏi" className="max-h-32 min-h-11 w-full resize-none bg-transparent px-3 py-2.5 text-sm leading-6 text-slate-800 outline-none placeholder:text-slate-400" />
              <div className="flex items-center justify-between gap-3 px-1 pb-1">
                <div className="flex items-center gap-1">
                  <button type="button" aria-label="Đính kèm tài liệu" className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600"><Icon name="clip" className="h-[18px] w-[18px]" /></button>
                  <button type="button" className="flex items-center gap-1.5 rounded-lg px-2 py-1.5 text-[11px] font-medium text-slate-500 transition hover:bg-slate-100"><Icon name="search" className="h-4 w-4 text-blue-600" /><span className="hidden sm:inline">Tìm trong nguồn y khoa</span><span className="ml-0.5 h-2 w-2 rounded-full bg-emerald-500" /></button>
                </div>
                <button type="submit" disabled={!input.trim()} aria-label="Gửi câu hỏi" className="flex h-9 items-center gap-2 rounded-xl bg-blue-600 px-3.5 text-xs font-semibold text-white shadow-md shadow-blue-600/20 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none"><span className="hidden sm:inline">Gửi câu hỏi</span><Icon name="send" className="h-4 w-4" /></button>
              </div>
            </div>
            <p className="mt-2 text-center text-[10px] leading-4 text-slate-400">Thông tin do AI cung cấp có thể chưa chính xác. Hãy tham khảo ý kiến chuyên gia y tế trước khi quyết định.</p>
          </form>
        </footer>
      </section>
    </div>
  );
}
