// pages/LotDetail.jsx
import { useEffect, useState, useCallback, useRef } from "react";
import { api } from "../utils/api";
import { fmtAed, fmtCountdown } from "../utils/format";
import { useDropTimer } from "../hooks/useDropTimer";
import BuySheet from "../components/BuySheet";
import MediaCarousel from "../components/MediaCarousel";

function MI({ icon }) {
  return <span className="material-icons" style={{ fontSize: 13, verticalAlign: "middle" }}>{icon}</span>;
}

function PropTags({ lot }) {
  const tags = [];
  if (lot.property_type) tags.push({ key: "type",    icon: "bed",       val: lot.property_type });
  if (lot.area_sqft)     tags.push({ key: "area",    icon: "grid_view", val: `${lot.area_sqft.toLocaleString("en-US")} sqft` });
  if (lot.floor_level)   tags.push({ key: "floor",   icon: "apartment", val: lot.floor_level });
  if (lot.view_type)     tags.push({ key: "view",    icon: "landscape", val: lot.view_type });
  if (lot.parking_spots != null) tags.push({ key: "park", icon: "directions_car", val: `${lot.parking_spots} мест` });
  if (lot.property_status) tags.push({ key: "status", icon: "key",      val: lot.property_status });
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 6, padding: "0 16px 12px" }}>
      {tags.map(t => (
        <span key={t.key} style={{ display: "inline-flex", alignItems: "center", gap: 4, background: "#ffffff", border: "1px solid #dde0ee", borderRadius: 6, padding: "3px 7px", fontSize: 11, color: "#1e2d4a" }}>
          <MI icon={t.icon} />{t.val}
        </span>
      ))}
    </div>
  );
}

function StatusBadge({ lot }) {
  if (lot.status === "active")
    return <div className="status-badge badge-active" style={{ fontSize: 14, padding: "5px 12px", fontWeight: 700, color: "#36cc64", background: "rgba(54,204,100,0.12)", border: "1px solid rgba(54,204,100,0.35)" }}><span className="live-dot" />активен</div>;
  if (lot.status === "paused")
    return <div className="status-badge badge-paused">⏸ Пауза</div>;
  if (lot.status === "scheduled")
    return <div className="status-badge badge-scheduled">🕐 Скоро</div>;
  if (lot.status === "finished" && lot.i_bought)
    return <div className="status-badge badge-won">🏆 Куплено</div>;
  if (lot.status === "finished")
    return <div className="status-badge badge-finished">завершён</div>;
  return null;
}

export default function LotDetail({ lotId, onBack, visible, haptic }) {
  const [lot,     setLot]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [sheet,   setSheet]   = useState(false);
  const [success, setSuccess] = useState(null);
  const pollRef    = useRef(null);
  const successRef = useRef(false);

  const dropSecs  = useDropTimer(lot?.seconds_until_drop);
  const startSecs = useDropTimer(lot?.seconds_until_start);

  const load = useCallback(async () => {
    if (!lotId || successRef.current) return;
    try {
      const data = await api.getLot(lotId);
      setLot(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, [lotId]);

  useEffect(() => {
    if (!visible || !lotId) return;
    setLoading(true);
    setLot(null);
    setSheet(false);
    setSuccess(null);
    successRef.current = false;
    load();
    pollRef.current = setInterval(load, 3000);
    return () => clearInterval(pollRef.current);
  }, [lotId, visible, load]);

  function handleBuySuccess(res) {
    successRef.current = true;
    clearInterval(pollRef.current);
    setSheet(false);
    setSuccess(res);
    setLot(prev => prev ? { ...prev, status: "finished", i_bought: true, final_price: res.final_price } : prev);
    try { haptic?.("medium"); } catch {}
  }

  function handleCloseSuccess() {
    successRef.current = false;
    setSuccess(null);
    onBack();
  }

  if (!visible) return null;

  const isActive    = lot?.status === "active";
  const isPaused    = lot?.status === "paused";
  const isScheduled = lot?.status === "scheduled";
  const isBought    = lot?.i_bought;

  return (
    <div className="screen">
      {/* Header — лот-код + название + статус */}
      <div style={{ padding: "14px 16px 0", display: "flex", alignItems: "flex-start", gap: 10 }}>
        <button className="tg-back" onClick={onBack} style={{ flexShrink: 0, marginTop: 2 }}>‹</button>
        <div style={{ flex: 1 }}>
          {lot && <div className="d-code" style={{ marginBottom: 4 }}>{lot.lot_code}</div>}
          <div style={{ fontSize: 19, fontWeight: 700, lineHeight: 1.25, color: "var(--text)" }}>
            {loading ? "Загрузка…" : lot ? `${lot.emoji} ${lot.title}` : "Лот не найден"}
          </div>
        </div>
        {lot && (
          <div style={{ flexShrink: 0, marginTop: 2 }}>
            <StatusBadge lot={lot} />
          </div>
        )}
      </div>

      {/* Prop tags */}
      {lot && <div style={{ marginTop: 8 }}><PropTags lot={lot} /></div>}

      {/* Body — flex, всё на одном экране */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", minHeight: 0 }}>
        {loading ? (
          <div className="loading-wrap"><div className="loading-spinner" /></div>
        ) : !lot ? (
          <div className="empty"><div className="empty-ico">❌</div><div className="empty-ttl">Лот не найден</div></div>
        ) : (
          <>
            {/* Media */}
            <div style={{ margin: "0 16px 8px", borderRadius: 12, overflow: "hidden", flex: "1 1 0", minHeight: 60, maxHeight: "45vh" }}>
              <MediaCarousel media={lot.media} emoji={lot.emoji} />
            </div>

            <div className="d-body" style={{ padding: "0 16px 4px", flexShrink: 0 }}>
              {/* Описание скрыто */}
              {/* {lot.description && <div className="d-desc">{lot.description}</div>} */}

              {/* Цены: покупки + рыночная */}
              <div className="stats3" style={{ gridTemplateColumns: "1fr 1fr", marginBottom: 6 }}>
                <div className="s3-box">
                  <div className="s3-val" style={{ fontSize: 11 }}>
                    {lot.purchase_price ? fmtAed(lot.purchase_price).replace("AED ", "") : "—"}
                  </div>
                  <div className="s3-lbl">Цена покупки</div>
                </div>
                <div className="s3-box">
                  <div className="s3-val" style={{ fontSize: 11 }}>
                    {lot.market_price ? fmtAed(lot.market_price).replace("AED ", "") : "—"}
                  </div>
                  <div className="s3-lbl">Рыночная</div>
                </div>
              </div>

              {/* Текущая цена — во всю строку */}
              <div className="stats3" style={{ gridTemplateColumns: "1fr", marginBottom: 6 }}>
                <div className="s3-box">
                  <div className="s3-val s3-val-gold" style={{ fontSize: 16 }}>
                    {fmtAed(lot.current_price)}
                  </div>
                  <div className="s3-lbl">Сейчас</div>
                </div>
              </div>

              {/* Won bar */}
              {isBought && (
                <div className="my-bar my-bar-won" style={{ marginBottom: 14 }}>
                  <span className="my-bar-icon">🏆</span>
                  <span className="my-bar-text">Вы купили этот объект</span>
                  <span className="my-bar-val my-bar-val-green">
                    {fmtAed(lot.final_price || lot.current_price)}
                  </span>
                </div>
              )}

              {/* Drop info */}
              {isActive && lot.price_drop_interval_minutes && (
                <div className="drop-block" style={{ marginBottom: 6 }}>
                  <div className="drop-row">
                    <span className="drop-left">Шаг снижения</span>
                    <span className="drop-right drop-right-gold">{fmtAed(lot.bid_step)}</span>
                  </div>
                  <div className="drop-divider" />
                  <div className="drop-row">
                    <span className="drop-left">Интервал</span>
                    <span className="drop-right">каждые {lot.price_drop_interval_minutes} мин</span>
                  </div>
                  <div className="drop-divider" />
                  <div className="drop-row">
                    <span className="drop-left">Следующее снижение</span>
                    <span className="drop-right drop-right-red">
                      {dropSecs > 0 ? `через ${fmtCountdown(dropSecs)}` : "скоро"}
                    </span>
                  </div>
                </div>
              )}

              {isPaused && lot.price_drop_interval_minutes && (
                <div className="drop-block" style={{ marginBottom: 6 }}>
                  <div className="drop-row">
                    <span className="drop-left">Шаг снижения</span>
                    <span className="drop-right drop-right-gold">{fmtAed(lot.bid_step)}</span>
                  </div>
                  <div className="drop-divider" />
                  <div className="drop-row">
                    <span className="drop-left">Снижение цены</span>
                    <span className="drop-right" style={{ color: "var(--gold)" }}>приостановлено</span>
                  </div>
                </div>
              )}

              {isScheduled && (
                <div className="drop-block" style={{ marginBottom: 6 }}>
                  <div className="drop-row">
                    <span className="drop-left">Старт аукциона</span>
                    <span className="drop-right drop-right-gold">
                      {lot.starts_at ? new Date(lot.starts_at).toLocaleString("ru-RU", {
                        day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit"
                      }) : "—"}
                    </span>
                  </div>
                  <div className="drop-divider" />
                  <div className="drop-row">
                    <span className="drop-left">Начало через</span>
                    <span className="drop-right" style={{ color: "var(--blue)" }}>
                      {fmtCountdown(startSecs)}
                    </span>
                  </div>
                  {lot.price_drop_interval_minutes && (
                    <>
                      <div className="drop-divider" />
                      <div className="drop-row">
                        <span className="drop-left">Шаг / интервал</span>
                        <span className="drop-right">{fmtAed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин</span>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {/* CTA */}
      {!loading && lot && (
        <div className="bid-cta-wrap">
          {isActive ? (
            <button className="bid-cta" onClick={() => { try { haptic?.("light"); } catch {} setSheet(true); }}>
              <span style={{ display: "block", fontSize: 13, fontWeight: 400, color: "rgba(255,255,255,0.6)" }}>Купить по текущей цене</span>
              <span style={{ display: "block", fontSize: 16, fontWeight: 800, color: "#fafafc" }}>{fmtAed(lot.current_price)}</span>
            </button>
          ) : isPaused ? (
            <div className="lot-closed">⏸ Аукцион приостановлен</div>
          ) : isScheduled ? (
            <div className="lot-closed">🕐 Аукцион ещё не начался</div>
          ) : isBought ? (
            <div className="lot-closed lot-closed-green">🏆 Вы купили этот объект</div>
          ) : (
            <div className="lot-closed">Аукцион завершён</div>
          )}
        </div>
      )}

      {/* Buy Sheet */}
      {sheet && lot && (
        <BuySheet
          lot={lot}
          onClose={() => setSheet(false)}
          onSuccess={handleBuySuccess}
          haptic={haptic}
        />
      )}

      {/* Success overlay */}
      {success && (
        <div className="success-overlay">
          <div className="success-ico">🏆</div>
          <div className="success-ttl">Вы победили!</div>
          <div className="success-sub">
            Объект куплен за<br />
            <span className="success-price">{success.final_price_fmt}</span>
          </div>
          <div className="success-note">Менеджер свяжется с вами в течение 1 часа</div>
          <button
            style={{ marginTop: 16, background: "var(--s2)", border: "1px solid var(--border2)", borderRadius: 12, padding: "12px 32px", color: "var(--text)", cursor: "pointer", fontSize: 14, fontWeight: 600 }}
            onClick={handleCloseSuccess}
          >
            Закрыть
          </button>
        </div>
      )}
    </div>
  );
}
