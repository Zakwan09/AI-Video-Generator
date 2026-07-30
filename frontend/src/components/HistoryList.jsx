export default function HistoryList({ history, isLoading, onSelect, onDelete }) {
  return (
    <div className="space-y-3">
      <h2 className="font-display text-xl text-gold-400">History</h2>

      {isLoading && <p className="text-sm text-stone-500">Loading history…</p>}

      {!isLoading && history.length === 0 && (
        <p className="text-sm text-stone-500">
          Your last five generated videos will appear here.
        </p>
      )}

      <ul className="thin-scroll max-h-[520px] space-y-2 overflow-y-auto pr-1">
        {history.map((item) => (
          <li
            key={item.id}
            className="group flex items-center gap-3 rounded-lg border border-obsidian-700 bg-obsidian-900/50 p-3 transition hover:border-gold-500/40"
          >
            <button
              onClick={() => onSelect(item)}
              className="flex-1 text-left"
              disabled={item.status !== "completed"}
            >
              <p className="truncate text-sm text-stone-200">{item.prompt}</p>
              <p className="mt-1 text-xs uppercase tracking-wide text-stone-500">
                {item.status}
              </p>
            </button>
            <button
              onClick={() => onDelete(item.id)}
              aria-label="Delete from history"
              className="shrink-0 rounded-md px-2 py-1 text-stone-500 opacity-0 transition group-hover:opacity-100 hover:text-red-400"
            >
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
