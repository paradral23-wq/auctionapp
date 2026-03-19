// src/hooks/useTimer.js
import { useEffect, useState } from "react";
import { fmtTimer, isEndingSoon } from "../utils/format";

export function useTimer(endsAt) {
  const [display, setDisplay] = useState(fmtTimer(endsAt));
  const [ending, setEnding] = useState(isEndingSoon(endsAt));

  useEffect(() => {
    if (!endsAt) return;
    const tick = () => {
      setDisplay(fmtTimer(endsAt));
      setEnding(isEndingSoon(endsAt));
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [endsAt]);

  return { display, ending };
}
