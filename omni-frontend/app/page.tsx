"use client";

import { useState } from "react";
import { runAgentLab, runWarRoom } from "@/services/api";
import Loader from "@/components/Loader";
import InsightPanel from "@/components/InsightPanel";

export default function Home() {
  const [query, setQuery] = useState("");
  const [insight, setInsight] = useState("");
  const [loading, setLoading] = useState(false);
  const [loaderMsg, setLoaderMsg] = useState("");

  async function handleLab() {
    setLoading(true);
    setLoaderMsg("Tactical Intelligence Agent Processing...");

    const res = await runAgentLab(query);

    setInsight(res.insight);
    setLoading(false);
  }

  async function handleWarRoom() {
    setLoading(true);

    const stages = [
      "Analyst Agent evaluating signals...",
      "Risk Agent stress testing assumptions...",
      "Growth Agent modelling scenarios...",
      "Debate Engine resolving conflicts...",
      "Executive Synthesis Agent generating report...",
    ];

    for (const msg of stages) {
      setLoaderMsg(msg);
      await new Promise(r => setTimeout(r, 700));
    }

    const res = await runWarRoom(query);

    setInsight(res.insight);
    setLoading(false);
  }

  return (
    <main className="min-h-screen bg-black text-white p-10">

      <h1 className="text-3xl text-cyan-400 mb-8">
        Omnichannel Intelligence System
      </h1>

      <div className="flex gap-4 mb-6">

        <input
          className="bg-black border border-cyan-500 rounded-lg p-3 flex-1"
          placeholder="Ask intelligence system..."
          onChange={(e) => setQuery(e.target.value)}
        />

        <button
          onClick={handleLab}
          className="bg-cyan-500 text-black px-4 rounded-lg"
        >
          Agent Lab
        </button>

        <button
          onClick={handleWarRoom}
          className="bg-purple-500 px-4 rounded-lg"
        >
          War Room
        </button>

      </div>

      {loading && <Loader message={loaderMsg} />}

      {insight && <InsightPanel insight={insight} />}

    </main>
  );
}
