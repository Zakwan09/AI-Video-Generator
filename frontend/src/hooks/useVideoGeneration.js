import { useCallback, useEffect, useState } from "react";
import {
  deleteHistoryItem,
  extractErrorMessage,
  fetchHistory,
  generateVideo,
} from "../api/client";

/**
 * Encapsulates all state and API interaction for the video generator page:
 * prompt handling, generation lifecycle, error messages, and history.
 */
export function useVideoGeneration() {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentVideo, setCurrentVideo] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);

  const loadHistory = useCallback(async () => {
    setIsHistoryLoading(true);
    try {
      const data = await fetchHistory();
      setHistory(data);
    } catch (err) {
      // History load failures shouldn't block the main generation flow.
      console.error("Failed to load history:", extractErrorMessage(err));
    } finally {
      setIsHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const handleGenerate = useCallback(async () => {
    setError(null);

    if (!prompt.trim()) {
      setError("Please enter a prompt before generating a video.");
      return;
    }

    setIsGenerating(true);
    setCurrentVideo(null);

    try {
      const video = await generateVideo(prompt.trim());
      setCurrentVideo(video);
      await loadHistory();
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setIsGenerating(false);
    }
  }, [prompt, loadHistory]);

  const handleDeleteHistoryItem = useCallback(async (id) => {
    try {
      await deleteHistoryItem(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  }, []);

  return {
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
  };
}
