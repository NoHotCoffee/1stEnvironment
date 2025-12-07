import fetch from 'node-fetch';

export function buildDevotionalPrompt({ verse_refs, tone, length, audience, content }: { verse_refs: string; tone: string; length: string; audience: string; content?: string }) {
  return `You are a Christian devotional writer. Create a ${length} devotional in a ${tone} tone for a ${audience} audience. Base it on the following passages: ${verse_refs}. Include reflection, application, and a short prayer. If user provided additional context, weave it in: ${content ?? 'n/a'}.`;
}

export function buildApologeticsPrompt({ topic, stance }: { topic: string; stance: string }) {
  return `You are an apologetics trainer. Provide a concise argument defending ${topic}. Then generate a skeptic objection and craft an ideal response. Use scripture references where helpful. Desired stance: ${stance}.`;
}

export async function callAI(prompt: string) {
  const apiKey = process.env.AI_API_KEY;
  const providerUrl = process.env.AI_PROVIDER_URL || 'https://example.com/llm';
  if (!apiKey) {
    // Offline stub
    return `DEV MODE RESPONSE: ${prompt.substring(0, 120)}...`;
  }
  const resp = await fetch(providerUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ prompt }),
  });
  if (!resp.ok) {
    throw new Error('AI provider error');
  }
  const json = await resp.json();
  return json.completion || json.output || JSON.stringify(json);
}
