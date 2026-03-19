// components/LotCard.jsx
import { useDropTimer } from "../hooks/useDropTimer";
import { fmtAed, fmtCountdown } from "../utils/format";

function MI({ icon }) {
  return <span className="material-icons" style={{ fontSize: 13, verticalAlign: "middle" }}>{icon}</span>;
}

function PropTags({ lot }) {
  const tags = [];
  if (lot.property_type) tags.push({ key: "type",   icon: "bed",           val: lot.property_type });
  if (lot.area_sqft)     tags.push({ key: "area",   icon: "grid_view",     val: `${lot.area_sqft.toLocaleString("en-US")} sqft` });
  if (lot.floor_level)   tags.push({ key: "floor",  icon: "apartment",     val: lot.floor_level });
  if (lot.view_type)     tags.push({ key: "view",   icon: "landscape",     val: lot.view_type });
  if (lot.parking_spots != null) tags.push({ key: "park", icon: "directions_car", val: `${lot.parking_spots} мест` });
  if (lot.property_status) tags.push({ key: "stat", icon: "key",           val: lot.property_status });
  return (
    <div className="c-props">
      {tags.map(t => (
        <span key={t.key} className="prop-tag prop-tag-icon" style={{ display: "inline-flex", alignItems: "center", gap: 3 }}>
          <MI icon={t.icon} />{t.val}
        </span>
      ))}
    </div>
  );
}

function StatusBadge({ lot }) {
  const { status } = lot;
  if (status === "active")    return <div className="status-badge badge-active"><span className="live-dot" />LIVE</div>;
  if (status === "paused")    return <div className="status-badge badge-paused">⏸ Пауза</div>;
  if (status === "scheduled") return <div className="status-badge badge-scheduled">🕐 Скоро</div>;
  if (status === "finished")  return lot.i_bought
    ? <div className="status-badge badge-won" style={{ fontSize: 12, padding: "4px 10px" }}>🏆 Куплено вами</div>
    : <div className="status-badge badge-finished">завершён</div>;
  if (status === "cancelled") return <div className="status-badge badge-finished">не состоялся</div>;
  return null;
}

export default function LotCard({ lot, onClick }) {
  const dropSecs    = useDropTimer(lot.seconds_until_drop);
  const startSecs   = useDropTimer(lot.seconds_until_start);
  const isBought    = lot.i_bought;
  const isActive    = lot.status === "active";
  const isScheduled = lot.status === "scheduled";

  const cardClass = `lot-card${
    isBought    ? " lot-card-bought"    :
    isActive    ? " lot-card-active"    :
    isScheduled ? " lot-card-scheduled" : ""
  }`;

  return (
    <div className={cardClass} onClick={onClick}>
      <div className="card-top">
        {/* Убран c-emoji */}
        <div className="c-info" style={{ flex: 1 }}>
          <div className="c-code">{lot.lot_code}</div>
          <div className="c-title">{lot.title}</div>
          <PropTags lot={lot} />
        </div>
        <div style={{ flexShrink: 0 }}>
          <StatusBadge lot={lot} />
        </div>
      </div>

      <div className="card-bottom">
        <div>
          <div className="c-price-label">
            {isBought ? "КУПЛЕНО ЗА" : isScheduled ? "СТАРТ" : "ТЕКУЩАЯ ЦЕНА"}
          </div>
          <div className={`c-price${isBought ? " c-price-green" : ""}`}>
            {fmtAed(isBought ? (lot.final_price || lot.current_price) : lot.current_price)}
          </div>
        </div>
        <div className="c-right-info">
          {isActive && lot.seconds_until_drop != null ? (
            <>
              <div className="c-drop-label">СНИЖЕНИЕ ЧЕРЕЗ</div>
              <div className="c-drop">📉 {fmtCountdown(dropSecs)}</div>
            </>
          ) : lot.status === "paused" ? (
            <>
              <div className="c-drop-label">СНИЖЕНИЕ</div>
              <div className="c-drop-upcoming">приостановлено</div>
            </>
          ) : isScheduled && lot.starts_at ? (
            <>
              <div className="c-drop-label">НАЧАЛО ЧЕРЕЗ</div>
              <div className="c-drop" style={{ color: "var(--blue)" }}>{fmtCountdown(startSecs)}</div>
            </>
          ) : null}
        </div>
      </div>

      {/* Баннер победы */}
      {lot.i_bought && (
        <div style={{
          marginTop: 8,
          background: "rgba(54,204,122,0.1)",
          border: "1px solid rgba(54,204,122,0.3)",
          borderRadius: 8, padding: "8px 12px",
          display: "flex", alignItems: "center", gap: 8,
        }}>
          <span style={{ fontSize: 18 }}>🏆</span>
          <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: "var(--green)" }}>Вы купили этот объект</div>
            <div style={{ fontSize: 10, color: "var(--text2)" }}>Менеджер свяжется с вами</div>
          </div>
        </div>
      )}
    </div>
  );
}
