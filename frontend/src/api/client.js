const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const error = new Error(`API request failed with status ${response.status}`);
    error.status = response.status;
    throw error;
  }

  return response.json();
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
