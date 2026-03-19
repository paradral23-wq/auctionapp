// src/components/BidSheet.jsx
import { useState, useEffect, useRef } from "react";
import { fmtPrice } from "../utils/format";
import { api } from "../utils/api";
import { useTelegram } from "../hooks/useTelegram";

export default function BidSheet({ lot, onClose, onSuccess }) {
  const { haptic } = useTelegram();
  const [selected, setSelected] = useState(1); // index: 0,1,2 or "custom"
  const [customVal, setCustomVal] = useState("");
  const [customError, setCustomError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); // {ok, msg}
  const inputRef = useRef(null);

  const min   = lot.current_price + lot.bid_step;
  const step  = lot.bid_step;
  const opts  = [min, min + step, min + step * 2];

  // Focus input when custom selected
  useEffect(() => {
    if (selected === "custom") {
      setTimeout(() => inputRef.current?.focus(), 80);
    }
  }, [selected]);

  function getAmount() {
    if (selected === "custom") {
      const v = parseInt(customVal.replace(/\D/g, ""), 10);
      return isNaN(v) ? null : v;
    }
    return opts[selected];
  }

  function validateCustom(raw) {
    const v = parseInt(raw.replace(/\D/g, ""), 10);
    if (!raw || isNaN(v)) { setCustomError(""); return; }
    if (v < min) {
      setCustomError(`Минимум: ${fmtPrice(min)}`);
    } else {
      setCustomError("");
    }
    setCustomVal(raw.replace(/\D/g, ""));
  }

  async function submit() {
    const amount = getAmount();
    if (!amount || amount < min) return;
    haptic("medium");
    setLoading(true);
    try {
      const res = await api.placeBid(lot.id, amount);
      if (res.success) {
        haptic("heavy");
        setResult({ ok: true, msg: res.message });
        setTimeout(() => { onSuccess(res.new_price); }, 1400);
      } else {
        haptic("rigid");
        setResult({ ok: false, msg: res.message });
        setTimeout(() => setResult(null), 2500);
      }
    } catch (e) {
      haptic("rigid");
      setResult({ ok: false, msg: e.message });
      setTimeout(() => setResult(null), 2500);
    } finally {
      setLoading(false);
    }
  }

  const amount = getAmount();
  const canSubmit = amount && amount >= min && !customError && !loading;

  const btnLabel = () => {
    if (loading) return "Отправляем...";
    if (result?.ok) return "✅ Ставка принята!";
    if (result && !result.ok) return result.msg;
    if (!canSubmit) return selected === "custom" ? "✏️ Введите сумму" : "Выберите ставку";
    return `🔨 Поставить ${fmtPrice(amount)}`;
  };

  return (
    <div className="sheet-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="sheet">
        <div className="sheet-handle" />
        <div className="sheet-title">Сделать ставку</div>
        <div className="sheet-lot">{lot.emoji} {lot.title}</div>

        <div className="bid-opts">
          {opts.map((v, i) => (
            <div
              key={i}
              className={`bid-opt${selected === i ? " sel" : ""}`}
              onClick={() => { setSelected(i); haptic("light"); }}
            >
              <div className="opt-val">{fmtPrice(v)}</div>
              <div className="opt-lbl">
                {i === 0 ? "+1 шаг" : i === 1 ? "+2 шага 🔥" : "+3 шага"}
              </div>
            </div>
          ))}

          <div
            className={`bid-opt${selected === "custom" ? " sel" : ""}`}
            onClick={() => { setSelected("custom"); haptic("light"); }}
          >
            <div className="opt-val" style={{ fontSize: 12, color: "var(--text2)" }}>Своя</div>
            <div className="opt-lbl">ввести сумму</div>
          </div>
        </div>

        {/* Custom input */}
        {selected === "custom" && (
          <div className="custom-wrap">
            <div style={{ position: "relative" }}>
              <input
                ref={inputRef}
                type="number"
                inputMode="numeric"
                placeholder={`от ${fmtPrice(min)}`}
                value={customVal}
                onChange={(e) => validateCustom(e.target.value)}
                className="custom-input"
              />
              <span className="custom-rub">₽</span>
            </div>
            {customError && (
              <div className="custom-hint error">{customError}</div>
            )}
            {customVal && !customError && (
              <div className="custom-hint ok">✓ Сумма принята</div>
            )}
          </div>
        )}

        <button
          className={`sheet-confirm${!canSubmit ? " disabled" : ""}${result?.ok ? " success" : ""}${result && !result.ok ? " error" : ""}`}
          onClick={submit}
          disabled={!canSubmit}
        >
          {btnLabel()}
        </button>
        <div className="sheet-note">
          Шаг: {fmtPrice(lot.bid_step)} · Антиснайп: 5 мин
        </div>
      </div>
    </div>
  );
}
