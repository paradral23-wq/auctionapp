// App.jsx
import { useState, useEffect } from "react";
import { useTelegram } from "./hooks/useTelegram";
import LotList  from "./pages/LotList";
import LotDetail from "./pages/LotDetail";
import Help from "./pages/Help";
import "./index.css";

// Экраны
const SCREEN = { LIST: "list", DETAIL: "detail", HELP: "help" };

export default function App() {
  const { tg, haptic, showBack, hideBack } = useTelegram();
  const [screen,    setScreen]    = useState(SCREEN.LIST);
  const [lotId,     setLotId]     = useState(null);
  const [prevScreen, setPrev]     = useState(null);

  // Telegram BackButton
  useEffect(() => {
    if (screen !== SCREEN.LIST) {
      showBack(goBack);
    } else {
      hideBack();
    }
  }, [screen]); // eslint-disable-line

  function openLot(id) {
    haptic("light");
    setPrev(screen);
    setLotId(id);
    setScreen(SCREEN.DETAIL);
  }

  function openHelp() {
    haptic("light");
    setPrev(screen);
    setScreen(SCREEN.HELP);
  }

  function goBack() {
    haptic("light");
    setScreen(prevScreen || SCREEN.LIST);
    if ((prevScreen || SCREEN.LIST) === SCREEN.LIST) setLotId(null);
  }

  return (
    <div className="app">
      {/* LIST — всегда в DOM, скрываем через CSS */}
      <div className={screen !== SCREEN.LIST ? "screen screen-hidden-left" : "screen"}>
        <LotList
          visible={screen === SCREEN.LIST}
          onLotClick={openLot}
          onHelpClick={openHelp}
        />
      </div>

      {/* DETAIL */}
      {screen === SCREEN.DETAIL && (
        <LotDetail
          lotId={lotId}
          onBack={goBack}
          visible={true}
          haptic={haptic}
        />
      )}

      {/* HELP */}
      {screen === SCREEN.HELP && (
        <Help
          onBack={goBack}
          visible={true}
        />
      )}
    </div>
  );
}
