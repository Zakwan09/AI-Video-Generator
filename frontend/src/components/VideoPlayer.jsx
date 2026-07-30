export default function VideoPlayer({ video }) {
  if (!video) return null;

  return (
    <div className="space-y-4 rounded-lg border border-obsidian-700 bg-obsidian-900/60 p-4">
      <video
        key={video.id}
        src={video.video_url}
        controls
        autoPlay
        loop
        className="w-full rounded-md bg-black"
      />

      <div className="flex flex-wrap items-center justify-between gap-3">
        <p
          className="max-w-md truncate font-body text-sm text-stone-400"
          title={video.prompt}
        >
          {video.prompt}
        </p>

        <a
          href={video.video_url}
          download
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 rounded-md border border-gold-500/40 px-4 py-2 text-sm font-medium text-gold-400 transition hover:bg-gold-500/10"
        >
          Download
        </a>
      </div>
    </div>
  );
}