// components/MediaCarousel.jsx
// Карусель фото + видео. Видео загружается только если есть в медиа.
import { useState, useRef, useCallback } from "react";

const BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function PhotoSlide({ fileId }) {
  const [err, setErr] = useState(false);
  if (err) return (
    <div className="carousel-slide carousel-slide-err">
      <span style={{ fontSize: 40, opacity: 0.3 }}>🖼</span>
    </div>
  );
  return (
    <div className="carousel-slide">
      <img
        src={`${BASE}/api/photo/${fileId}`}
        alt=""
        className="carousel-img"
        onError={() => setErr(true)}
      />
    </div>
  );
}

function VideoSlide({ fileId, active }) {
  const videoRef = useRef(null);
  const [loaded, setLoaded] = useState(false);

  // Останавливаем видео когда слайд не активен
  if (!active && videoRef.current) {
    videoRef.current.pause();
  }

  return (
    <div className="carousel-slide carousel-slide-video">
      {!loaded && (
        <div className="carousel-video-placeholder">
          <div className="carousel-play-icon">▶</div>
          <div className="carousel-video-label">Видео</div>
        </div>
      )}
      <video
        ref={videoRef}
        className="carousel-video"
        controls
        playsInline
        preload="metadata"
        src={`${BASE}/api/video/${fileId}`}
        onLoadedMetadata={() => setLoaded(true)}
        style={{ display: loaded ? "block" : "none" }}
      />
    </div>
  );
}

function Dots({ total, current, onDotClick }) {
  if (total <= 1) return null;
  return (
    <div className="carousel-dots">
      {Array.from({ length: total }).map((_, i) => (
        <div
          key={i}
          className={`carousel-dot${i === current ? " carousel-dot-active" : ""}`}
          onClick={() => onDotClick(i)}
        />
      ))}
    </div>
  );
}

export default function MediaCarousel({ media, emoji }) {
  const [current, setCurrent] = useState(0);
  const touchStart = useRef(null);
  const touchEnd   = useRef(null);

  // Если нет медиа — показываем эмодзи-заглушку
  if (!media || media.length === 0) {
    return (
      <div className="hero">
        <span style={{ position: "relative", zIndex: 2, fontSize: 80 }}>{emoji}</span>
      </div>
    );
  }

  const total = media.length;
  const item  = media[current];

  const prev = useCallback(() => setCurrent(c => Math.max(0, c - 1)), []);
  const next = useCallback(() => setCurrent(c => Math.min(total - 1, c + 1)), [total]);

  // Свайп
  const onTouchStart = (e) => { touchStart.current = e.targetTouches[0].clientX; };
  const onTouchMove  = (e) => { touchEnd.current   = e.targetTouches[0].clientX; };
  const onTouchEnd   = () => {
    if (!touchStart.current || !touchEnd.current) return;
    const diff = touchStart.current - touchEnd.current;
    if (Math.abs(diff) > 40) diff > 0 ? next() : prev();
    touchStart.current = null;
    touchEnd.current   = null;
  };

  return (
    <div
      className="carousel"
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
    >
      {/* Слайд */}
      {item.media_type === "video"
        ? <VideoSlide fileId={item.file_id} active={true} />
        : <PhotoSlide fileId={item.file_id} />
      }

      {/* Стрелки навигации (только если > 1 слайда) */}
      {total > 1 && current > 0 && (
        <button className="carousel-arrow carousel-arrow-left" onClick={prev}>‹</button>
      )}
      {total > 1 && current < total - 1 && (
        <button className="carousel-arrow carousel-arrow-right" onClick={next}>›</button>
      )}

      {/* Счётчик */}
      {total > 1 && (
        <div className="carousel-counter">{current + 1} / {total}</div>
      )}

      {/* Тип слайда (видео) */}
      {item.media_type === "video" && (
        <div className="carousel-type-badge">🎥 Видео</div>
      )}

      {/* Точки */}
      <Dots total={total} current={current} onDotClick={setCurrent} />
    </div>
  );
}
