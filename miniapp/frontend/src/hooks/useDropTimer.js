// hooks/useDropTimer.js
import { useEffect, useRef, useState } from "react";

export function useDropTimer(serverSeconds) {
  const [secs, setSecs] = useState(serverSeconds || 0);
  const secsRef = useRef(secs);

  // Синхронизация с сервером при каждом поллинге
  useEffect(() => {
    if (serverSeconds == null) return;
    secsRef.current = serverSeconds;
    setSecs(serverSeconds);
  }, [serverSeconds]);

  // Локальный тик — создаётся один раз
  useEffect(() => {
    const id = setInterval(() => {
      if (secsRef.current > 0) {
        secsRef.current -= 1;
        setSecs(secsRef.current);
      }
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return secs;
}
