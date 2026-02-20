const AGENTS_BASE_URL = "https://omnichannel-multi-agentics-agents.onrender.com";

export async function runAgentLab(query: string) {
    const res = await fetch(`${AGENTS_BASE_URL}/agent/lab`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    return res.json();
}

export async function runWarRoom(query: string) {
    const res = await fetch(`${AGENTS_BASE_URL}/agent/warroom`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    return res.json();
}
