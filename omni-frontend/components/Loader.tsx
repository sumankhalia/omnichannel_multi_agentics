export default function Loader({ message }: { message: string }) {
  return (
    <div className="bg-black border border-cyan-500 p-4 rounded-xl animate-pulse">
      <p className="text-cyan-400 text-sm tracking-widest">
        {message}
      </p>
    </div>
  );
}
