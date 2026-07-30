export default function ErrorAlert({ message, onDismiss }) {
  if (!message) return null;

  return (
    <div className="flex items-start justify-between gap-3 rounded-lg border border-red-500/30 bg-red-950/40 px-4 py-3 text-sm text-red-300">
      <span>{message}</span>
      <button
        onClick={onDismiss}
        aria-label="Dismiss error"
        className="shrink-0 text-red-400/70 transition hover:text-red-300"
      >
        ✕
      </button>
    </div>
  );
}
