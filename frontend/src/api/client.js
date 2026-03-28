export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  const contentType = response.headers.get("content-type") ?? "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      payload?.detail ??
      payload?.message ??
      `API request failed with status ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

export async function fetchHealth() {
  return request("/health");
}

export async function fetchLatestRun(ticker) {
  return request(`/runs/latest?ticker=${encodeURIComponent(ticker)}`);
}

export async function fetchRunHistory(ticker) {
  return request(`/runs/history?ticker=${encodeURIComponent(ticker)}`);
}

export async function triggerRun(ticker) {
  return request("/runs/trigger", {
    method: "POST",
    body: JSON.stringify({ ticker }),
  });
}

export async function resetRuns(ticker) {
  return request(`/runs?ticker=${encodeURIComponent(ticker)}`, {
    method: "DELETE",
  });
}
