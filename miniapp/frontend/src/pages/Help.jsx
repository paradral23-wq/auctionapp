// pages/Help.jsx
import { api } from "../utils/api";
import { useTelegram } from "../hooks/useTelegram";

const HOW_IT_WORKS = [
  {
    ico: "📉",
    title: "Голландский аукцион",
    body: "Цена начинается высокой и снижается каждые несколько минут. Первый кто нажмёт «Купить» — побеждает и получает объект по текущей цене.",
  },
  {
    ico: "⏱",
    title: "Таймер снижения",
    body: "На карточке лота показывается время до следующего снижения цены. Чем дольше ждёте — тем ниже цена, но риск что купит другой участник.",
  },
  {
    ico: "🏠",
    title: "Как купить",
    body: "Откройте лот → нажмите «Купить по текущей цене» → подтвердите. После подтверждения сделка считается заключённой.",
  },
];

const STATUSES = [
  { ico: "🔴", title: "LIVE — идёт сейчас",   body: "Аукцион активен, цена снижается. Можно купить прямо сейчас." },
  { ico: "⏸",  title: "Пауза",                body: "Аукцион временно приостановлен. Снижение цены остановлено, покупка недоступна." },
  { ico: "🕐",  title: "Скоро начнётся",       body: "Аукцион запланирован и начнётся в указанное время." },
];

export default function Help({ onBack, visible }) {
  const { openTgLink } = useTelegram();

  async function handleContact() {
    try {
      openTgLink("tg://resolve?domain=Fikhor");
    } catch (e) {
      console.error(e);
    }
  }

  if (!visible) return null;

  return (
    <div className="screen">
      <div className="tg-bar">
        <button className="tg-back" onClick={onBack}>‹</button>
        <div className="tg-info">
          <div className="tg-title">Помощь</div>
          <div className="tg-sub tg-sub-default">Инструкция и поддержка</div>
        </div>
        <div className="tg-ava">❓</div>
      </div>

      <div className="help-scroll">

        <div className="help-section">
          <div className="help-section-title">Как работает аукцион</div>
          {HOW_IT_WORKS.map(item => (
            <div key={item.title} className="help-item">
              <div className="help-ico">{item.ico}</div>
              <div>
                <div className="help-text-title">{item.title}</div>
                <div className="help-text-body">{item.body}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="help-section">
          <div className="help-section-title">Статусы лотов</div>
          {STATUSES.map(item => (
            <div key={item.title} className="help-item">
              <div className="help-ico">{item.ico}</div>
              <div>
                <div className="help-text-title">{item.title}</div>
                <div className="help-text-body">{item.body}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="help-section">
          <div className="help-section-title">Поддержка</div>
          <button className="contact-btn" onClick={handleContact}>
            <span>💬</span>
            <span>Написать администратору @Fikhor</span>
          </button>
        </div>

      </div>
    </div>
  );
}
