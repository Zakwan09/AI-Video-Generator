export default function LoadingSpinner({ label = "Generating your video…" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 rounded-lg border border-obsidian-700 bg-obsidian-900/60 py-14">
      <div className="h-10 w-10 animate-spin rounded-full border-2 border-gold-500/25 border-t-gold-400" />
      <p className="font-body text-sm text-stone-400">{label}</p>
    </div>
  );
}
