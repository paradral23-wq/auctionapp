// components/BuySheet.jsx
import { useState } from "react";
import { fmtAed } from "../utils/format";
import { api } from "../utils/api";

export default function BuySheet({ lot, onClose, onSuccess, haptic }) {
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState(null);

  async function handleConfirm() {
    haptic?.("medium");
    setLoading(true);
    setError(null);
    try {
      // Таймаут 15 секунд
      const res = await Promise.race([
        api.buyLot(lot.id),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("Превышено время ожидания. Попробуйте снова.")), 15000)
        ),
      ]);
      console.log("Buy success:", JSON.stringify(res));
      haptic?.("success");
      onSuccess(res);
    } catch (e) {
      haptic?.("error");
      setError(e.message || "Ошибка при покупке");
      setLoading(false);
    }
  }

  return (
    <div className="sheet-overlay" onClick={e => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="sheet">
        <div className="sheet-handle" />
        <div className="sheet-title">Подтвердите покупку</div>
        <div className="sheet-sub">{lot.emoji} {lot.title}</div>

        <div className="sheet-price-big">
          <div className="sheet-price-label">ВЫ ПОКУПАЕТЕ ПО ТЕКУЩЕЙ ЦЕНЕ</div>
          <div className="sheet-price-val">{fmtAed(lot.current_price)}</div>
        </div>

        <div className="sheet-warn">
          ⚠️ Это действие необратимо.<br />
          После подтверждения сделка считается заключённой.
        </div>

        {error && (
          <div style={{
            background: "rgba(255,71,87,0.1)",
            border: "1px solid rgba(255,71,87,0.3)",
            borderRadius: 10,
            padding: "10px 14px",
            color: "var(--red)",
            fontSize: 13,
            textAlign: "center",
            marginBottom: 12,
            lineHeight: 1.4,
          }}>
            ❌ {error}
          </div>
        )}

        <button
          className="sheet-confirm"
          onClick={handleConfirm}
          disabled={loading}
        >
          {loading ? "⏳ Обрабатывается..." : "✅ Точно подтверждаю покупку"}
        </button>
        <div className="sheet-note">Менеджер свяжется с вами в течение 1 часа</div>

        {!loading && (
          <button
            onClick={onClose}
            style={{
              marginTop: 10,
              width: "100%",
              background: "none",
              border: "none",
              color: "var(--text2)",
              fontSize: 13,
              cursor: "pointer",
              padding: "8px",
            }}
          >
            Отмена
          </button>
        )}
      </div>
    </div>
  );
}
