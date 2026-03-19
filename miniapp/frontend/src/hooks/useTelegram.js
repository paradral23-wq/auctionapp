// hooks/useTelegram.js
import { useEffect, useState } from "react";

export function useTelegram() {
  const [tg, setTg]   = useState(null);
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const webapp = window.Telegram?.WebApp;
    if (webapp) {
      webapp.ready();
      webapp.expand();
      webapp.setHeaderColor?.("#0c0c10");
      webapp.setBackgroundColor?.("#0c0c10");
      setTg(webapp);
      setUser(webapp.initDataUnsafe?.user || null);
    } else {
      setUser({ id: 123456, first_name: "Dev", username: "devuser" });
    }
    setReady(true);
  }, []);

  const showBack = (cb) => { tg?.BackButton?.show(); tg?.BackButton?.onClick(cb); };
  const hideBack = ()   => { tg?.BackButton?.hide(); tg?.BackButton?.offClick?.(); };
  const haptic = (t = "light") => {
    try {
      if (t === "success" || t === "error" || t === "warning") {
        tg?.HapticFeedback?.notificationOccurred(t);
      } else {
        tg?.HapticFeedback?.impactOccurred(t);
      }
    } catch {}
  };

  const openTgLink = (url) => {
    if (tg?.openTelegramLink) tg.openTelegramLink(url);
    else window.open(url, "_blank");
  };

  return { tg, user, ready, showBack, hideBack, haptic, openTgLink };
}
