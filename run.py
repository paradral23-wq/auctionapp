"""
run.py — запускает всё одной командой:
  • auction_admin_bot
  • auction_group_bot
  • miniapp/backend (uvicorn)

Запуск:  python run.py
Стоп:    Ctrl+C  (останавливает все процессы)
"""
import subprocess
import sys
import os
import signal
import time

ROOT = os.path.dirname(os.path.abspath(__file__))

PYTHON = sys.executable

processes = []


def start():
    procs = [
        {
            "name": "Admin Bot",
            "cmd": [PYTHON, "bot.py"],
            "cwd": os.path.join(ROOT, "auction_admin_bot"),
        },
        {
            "name": "Group Bot",
            "cmd": [PYTHON, "bot.py"],
            "cwd": os.path.join(ROOT, "auction_group_bot"),
        },
        {
            "name": "Mini App API",
            "cmd": [PYTHON, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
            "cwd": os.path.join(ROOT, "miniapp", "backend"),
        },
    ]

    for p in procs:
        print(f"▶  Starting {p['name']}...")
        proc = subprocess.Popen(
            p["cmd"],
            cwd=p["cwd"],
            # Каждый процесс пишет в свой лог-файл И в консоль
            stdout=None,
            stderr=None,
        )
        processes.append((p["name"], proc))
        time.sleep(0.5)  # небольшая пауза между стартами

    print("\n✅ Все процессы запущены. Ctrl+C для остановки.\n")

    try:
        while True:
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n⚠️  {name} завершился с кодом {proc.returncode}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n⏹  Остановка...")
        for name, proc in processes:
            print(f"   Stopping {name}...")
            proc.terminate()
        for name, proc in processes:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        print("✅ Остановлено.")


if __name__ == "__main__":
    start()
