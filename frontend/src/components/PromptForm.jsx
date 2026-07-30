export default function PromptForm({ prompt, setPrompt, onGenerate, isGenerating }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <label htmlFor="prompt" className="block font-display text-2xl text-gold-400">
        Describe your video
      </label>
      <textarea
        id="prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="A luxury perfume bottle rotating on a black marble surface with golden lighting."
        rows={4}
        disabled={isGenerating}
        className="w-full resize-none rounded-lg border border-obsidian-700 bg-obsidian-900/80 px-4 py-3 text-stone-100 placeholder:text-stone-500 shadow-inner shadow-black/40 outline-none transition focus:border-gold-500/60 focus:ring-1 focus:ring-gold-500/40 disabled:opacity-60"
      />
      <button
        type="submit"
        disabled={isGenerating}
        className="group relative inline-flex items-center justify-center rounded-lg bg-gradient-to-r from-gold-600 via-gold-500 to-gold-400 px-6 py-3 font-body font-semibold text-obsidian-950 shadow-lg shadow-gold-500/10 transition hover:shadow-gold-500/25 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isGenerating ? "Generating…" : "Generate Video"}
      </button>
    </form>
  );
}
