import { useState } from "react";
import PromptForm from "./components/PromptForm";
import LoadingSpinner from "./components/LoadingSpinner";
import ErrorAlert from "./components/ErrorAlert";
import VideoPlayer from "./components/VideoPlayer";
import HistoryList from "./components/HistoryList";
import { useVideoGeneration } from "./hooks/useVideoGeneration";

export default function App() {
  const {
    prompt,
    setPrompt,
    isGenerating,
    currentVideo,
    error,
    setError,
    history,
    isHistoryLoading,
    handleGenerate,
    handleDeleteHistoryItem,
  } = useVideoGeneration();

  const [previewVideo, setPreviewVideo] = useState(null);

  const displayedVideo = currentVideo || previewVideo;

  return (
    <div className="min-h-screen px-4 py-10 sm:px-8 lg:px-16">
      <header className="mb-10 text-center">
        <p className="font-body text-xs uppercase tracking-[0.3em] text-gold-500/70">
          Text to Cinema
        </p>
        <h1 className="mt-2 font-display text-4xl font-semibold text-stone-100 sm:text-5xl">
          AI Video Generator
        </h1>
        <p className="mx-auto mt-3 max-w-xl font-body text-sm text-stone-400">
          Turn a single sentence into a short AI-generated video.
        </p>
      </header>

      <main className="mx-auto grid max-w-6xl gap-8 lg:grid-cols-[2fr_1fr]">
        <section className="space-y-6">
          <div className="rounded-xl border border-obsidian-700 bg-obsidian-900/40 p-6 shadow-2xl shadow-black/30">
            <PromptForm
              prompt={prompt}
              setPrompt={setPrompt}
              onGenerate={handleGenerate}
              isGenerating={isGenerating}
            />
          </div>

          <ErrorAlert message={error} onDismiss={() => setError(null)} />

          {isGenerating && <LoadingSpinner />}

          {!isGenerating && displayedVideo && <VideoPlayer video={displayedVideo} />}
        </section>

        <aside className="rounded-xl border border-obsidian-700 bg-obsidian-900/40 p-6 shadow-2xl shadow-black/30">
          <HistoryList
            history={history}
            isLoading={isHistoryLoading}
            onSelect={setPreviewVideo}
            onDelete={handleDeleteHistoryItem}
          />
        </aside>
      </main>
    </div>
  );
}
