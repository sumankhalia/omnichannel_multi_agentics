export default function InsightPanel({ insight }: { insight: string }) {
  return (
    <div className="bg-linear-to-br from-black to-gray-900 border border-cyan-500 rounded-xl p-6 shadow-xl mt-6">

      <h2 className="text-cyan-400 text-lg mb-3">
        AI Intelligence Output
      </h2>

      <pre className="text-green-400 whitespace-pre-wrap text-sm">
        {insight}
      </pre>

    </div>
  );
}
