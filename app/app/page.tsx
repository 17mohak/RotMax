"use client";

import { useState } from "react";

export default function Home() {
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setVideoUrl(null);

    try {
      // This connects to your Python backend
      const response = await fetch("http://127.0.0.1:8000/generate-video", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ notes }),
      });

      if (!response.ok) throw new Error("Failed to generate");

      // Convert the response to a video blob URL
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setVideoUrl(url);
    } catch (error) {
      console.error(error);
      alert("Something broke! Check your Python terminal.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white p-10 flex flex-col items-center">
      <h1 className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-8">
        ROTMAX
      </h1>

      {/* Input Area */}
      <div className="w-full max-w-2xl space-y-4">
        <textarea
          className="w-full h-40 p-4 bg-gray-900 border border-gray-700 rounded-xl focus:ring-2 focus:ring-purple-500 outline-none text-lg"
          placeholder="Paste your boring study notes here..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />

        <button
          onClick={handleGenerate}
          disabled={loading || !notes}
          className={`w-full py-4 rounded-xl font-bold text-xl transition-all ${
            loading
              ? "bg-gray-700 cursor-not-allowed"
              : "bg-purple-600 hover:bg-purple-500 hover:scale-105"
          }`}
        >
          {loading ? "COOKING... 🍳" : "GENERATE BRAINROT 🚀"}
        </button>
      </div>

      {/* Video Output */}
      {videoUrl && (
        <div className="mt-10 animate-in fade-in slide-in-from-bottom-10">
          <h2 className="text-2xl font-bold mb-4 text-center">It's Ready.</h2>
          <video
            src={videoUrl}
            controls
            autoPlay
            className="rounded-xl border-4 border-purple-500 shadow-2xl w-full max-w-md"
          />
          <a
            href={videoUrl}
            download="brainrot.mp4"
            className="block text-center mt-4 text-gray-400 hover:text-white underline"
          >
            Download MP4
          </a>
        </div>
      )}
    </main>
  );
}