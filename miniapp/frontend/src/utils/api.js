// utils/api.js
export const BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function getInitData() {
  try { return window.Telegram?.WebApp?.initData || ""; }
  catch { return ""; }
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "x-tg-init-data": getInitData(),
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Ошибка запроса");
  }
  return res.json();
}

export const api = {
  getLots:    ()         => request("/api/lots"),
  getMyLots:  ()         => request("/api/lots/mine"),
  getLot:     (id)       => request(`/api/lots/${id}`),
  buyLot:     (lot_id)   => request("/api/buy", { method: "POST", body: JSON.stringify({ lot_id }) }),
  contact:    ()         => request("/api/contact", { method: "POST" }),
};
