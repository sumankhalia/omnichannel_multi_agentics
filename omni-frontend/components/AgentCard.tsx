export default function AgentCard({ title, value }: any) {
    return (
        <div className="bg-black border border-purple-500 rounded-xl p-4 shadow-lg">
            <p className="text-purple-400 text-xs">{title}</p>
            <p className="text-white text-xl">{value}</p>
        </div>
    );
}
