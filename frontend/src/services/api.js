const BASE_URL = "http://127.0.0.1:8000";

export async function sendQuestion(payload) {
  const res = await fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const text = await res.text();
  console.log("STATUS:", res.status);
  console.log("RESPONSE:", text);

  if (!res.ok) {
    throw new Error(text);
  }

  return JSON.parse(text);
}