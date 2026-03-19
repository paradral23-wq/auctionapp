// utils/format.js

export function fmtAed(amount) {
  if (amount == null) return "—";
  return "AED " + amount.toLocaleString("en-US").replace(/,/g, " ");
}

export function fmtAedShort(amount) {
  if (amount == null) return "—";
  if (amount >= 1_000_000) return `AED ${(amount / 1_000_000).toFixed(1)}M`;
  if (amount >= 1_000)     return `AED ${Math.round(amount / 1_000)}K`;
  return `AED ${amount}`;
}

/** Таймер обратного отсчёта из секунд */
export function fmtCountdown(seconds) {
  if (seconds == null || seconds <= 0) return "0:00";
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${m}:${String(s).padStart(2, "0")}`;
}

/** Таймер до даты (ISO string) */
export function fmtTimerTo(isoDate) {
  if (!isoDate) return null;
  const diff = Math.max(0, Math.floor((new Date(isoDate) - Date.now()) / 1000));
  return fmtCountdown(diff);
}

export function isEndingSoon(seconds) {
  return seconds > 0 && seconds < 600; // < 10 мин
}

export function getLotStatus(lot) {
  return lot.status; // active | paused | scheduled | finished | cancelled
}

export function getLotMyStatus(lot) {
  if (!lot.i_bid && !lot.i_bought) return null;
  if (lot.i_bought) return "bought";
  if (lot.status === "finished" && !lot.i_bought) return "lost";
  if (lot.status === "active") return "participating";
  return null;
}
