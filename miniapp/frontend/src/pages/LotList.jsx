// pages/LotList.jsx
import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "../utils/api";
import LotCard from "../components/LotCard";

function SectionHeader({ label, count, live }) {
  return (
    <div className="sec-head" style={count === undefined ? {} : {}}>
      <span className="sec-lbl">{label}{count !== undefined ? ` · ${count}` : ""}</span>
      {live && (
        <span className="live-pill">
          <span className="live-dot" />LIVE
        </span>
      )}
    </div>
  );
}

function AllTab({ lots, onLotClick }) {
  const active    = lots.filter(l => l.status === "active");
  const paused    = lots.filter(l => l.status === "paused");
  const scheduled = lots.filter(l => l.status === "scheduled");
  const finished  = lots.filter(l => l.status === "finished" || l.status === "cancelled");
  const liveCount = active.length + paused.length;

  if (!lots.length) {
    return (
      <div className="empty">
        <div className="empty-ico">🏠</div>
        <div className="empty-ttl">Нет активных аукционов</div>
        <div className="empty-sub">Следите за новыми лотами</div>
      </div>
    );
  }

  return (
    <>
      {(active.length > 0 || paused.length > 0) && (
        <>
          <SectionHeader label="Идут сейчас" count={liveCount} live={active.length > 0} />
          {active.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
          {paused.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
        </>
      )}
      {scheduled.length > 0 && (
        <>
          <SectionHeader label="Скоро начнутся" count={scheduled.length} />
          {scheduled.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
        </>
      )}
      {finished.length > 0 && (
        <>
          <div className="sec-head" style={{ marginTop: 18 }}>
            <span className="sec-lbl">Завершённые</span>
          </div>
          {finished.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
        </>
      )}
    </>
  );
}

function MyTab({ lots, onLotClick }) {
  const participating = lots.filter(l => l.status === "active" || l.status === "paused");
  const bought        = lots.filter(l => l.i_bought);
  const notBought     = lots.filter(l => !l.i_bought && (l.status === "finished" || l.status === "cancelled"));

  if (!lots.length) {
    return (
      <div className="empty">
        <div className="empty-ico">📋</div>
        <div className="empty-ttl">Вы ещё не участвовали</div>
        <div className="empty-sub">Откройте лот и нажмите «Купить»</div>
      </div>
    );
  }

  return (
    <>
      {participating.length > 0 && (
        <>
          <SectionHeader label="Участвую сейчас" count={participating.length} live={participating.some(l => l.status === "active")} />
          {participating.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
        </>
      )}
      {bought.length > 0 && (
        <>
          <div className="sec-head" style={{ marginTop: participating.length ? 18 : 0 }}>
            <span className="sec-lbl">Куплено · {bought.length}</span>
          </div>
          {bought.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
        </>
      )}
      {notBought.length > 0 && (
        <>
          <div className="sec-head" style={{ marginTop: 18 }}>
            <span className="sec-lbl">Не купил · {notBought.length}</span>
          </div>
          {notBought.map(l => <LotCard key={l.id} lot={l} onClick={() => onLotClick(l.id)} />)}
        </>
      )}
    </>
  );
}

export default function LotList({ onLotClick, onHelpClick, visible }) {
  const [tab, setTab]     = useState(0);
  const [lots, setLots]   = useState([]);
  const [myLots, setMyLots] = useState([]);
  const [loading, setLoading] = useState(true);
  const pillRef = useRef(null);
  const segRef  = useRef(null);
  const pollRef = useRef(null);

  const load = useCallback(async () => {
    try {
      const [all, mine] = await Promise.all([api.getLots(), api.getMyLots()]);
      setLots(all.lots || []);
      setMyLots(mine.lots || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
    pollRef.current = setInterval(load, 3000);
    return () => clearInterval(pollRef.current);
  }, [load]);

  // Segment pill
  useEffect(() => {
    const seg  = segRef.current;
    const pill = pillRef.current;
    if (!seg || !pill) return;
    const w = seg.offsetWidth / 2;
    pill.style.width     = w + "px";
    pill.style.transform = `translateX(${tab * w}px)`;
  }, [tab]);

  const activeCount = lots.filter(l => l.status === "active").length;

  return (
    <div className={`screen${!visible ? " screen-hidden-right" : ""}`}>
      {/* Header */}
      <div className="tg-bar">
        <div style={{ width: 32 }} />
        <div className="tg-info">
          <div className="tg-title">Dutch Auction</div>
          <div className={`tg-sub ${activeCount > 0 ? "tg-sub-green" : "tg-sub-muted"}`}>
            {activeCount > 0 ? `● ${activeCount} активных лота` : "нет активных аукционов"}
          </div>
        </div>
        <button className="tg-btn-icon" onClick={onHelpClick}>?</button>
      </div>

      {/* Segment скрыт */}

      {/* Content */}
      <div className="scroll">
        {loading ? (
          <div className="loading-wrap" style={{ marginTop: 60 }}>
            <div className="loading-spinner" />
          </div>
        ) : (
          <AllTab lots={lots} onLotClick={onLotClick} />
        )}
      </div>
    </div>
  );
}
