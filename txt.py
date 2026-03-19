"""
collect_context.py — Сборщик контекста проекта для LLM.

Использование:
    python collect_context.py

Создаёт файл project_context.md с деревом проекта и содержимым всех файлов.
"""

import os
from pathlib import Path

# === НАСТРОЙКИ ===

OUTPUT_FILE = "project_context.md"

# Папки, которые НЕ сканируются
IGNORE_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__",
    "venv", ".venv", "env",
    "node_modules", ".mypy_cache", ".pytest_cache",
    "dist", "build", "backups",
    "pg_data", "redis_data",
    "gemini_context", "logs",
    "temp_broadcast_photos",
}

# Файлы, которые НЕ включаются
IGNORE_FILES = {
    OUTPUT_FILE,
    "project_context.md",
    "collect_context.py",
    "txt.py",
    ".env",
    ".env.bak",
    "database_dump.sql",
}

# Расширения файлов для включения
ALLOWED_EXTENSIONS = {
    ".py", ".sql", ".json", ".ini", ".toml",
    ".yml", ".yaml", ".sh", ".bat", ".md",
    ".html", ".css", ".js",
}

# Точные имена файлов (без расширения в списке)
ALLOWED_FILENAMES = {
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "requirements.txt",
    ".gitignore",
}

# Подсветка синтаксиса для Markdown
LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".json": "json",
    ".sh": "bash",
    ".bat": "batch",
    ".toml": "toml",
    ".ini": "ini",
    ".md": "markdown",
}


def should_include(filename: str) -> bool:
    """Проверяет, нужно ли включить файл."""
    if filename in IGNORE_FILES:
        return False
    if filename in ALLOWED_FILENAMES:
        return True
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def build_tree(root_path: Path) -> str:
    """Строит дерево файлов проекта."""
    lines = ["# PROJECT STRUCTURE", "```text"]

    for root, dirs, files in os.walk(root_path):
        # Фильтруем папки in-place
        dirs[:] = sorted([d for d in dirs if d not in IGNORE_DIRS])

        level = len(Path(root).relative_to(root_path).parts)
        indent = "    " * level

        if root != str(root_path):
            lines.append(f"{indent}{Path(root).name}/")

        file_indent = "    " * (level + 1) if root != str(root_path) else "    "
        for f in sorted(files):
            if should_include(f):
                lines.append(f"{file_indent}{f}")

    lines.append("```")
    return "\n".join(lines)


def collect_files(root_path: Path) -> str:
    """Собирает содержимое всех файлов."""
    blocks = []

    for root, dirs, files in os.walk(root_path):
        dirs[:] = sorted([d for d in dirs if d not in IGNORE_DIRS])

        for f in sorted(files):
            if not should_include(f):
                continue

            file_path = Path(root) / f
            rel_path = file_path.relative_to(root_path)

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"  ⚠️ Ошибка чтения {rel_path}: {e}")
                continue

            lang = LANG_MAP.get(file_path.suffix.lower(), "")
            block = f"\n\n## File: {rel_path}\n```{lang}\n{content}\n```"
            blocks.append(block)

    return "\n".join(blocks)


def main():
    root_path = Path(".").resolve()
    output_path = root_path / OUTPUT_FILE

    print(f"📦 Сборка контекста проекта...")
    print(f"   Корень: {root_path}")

    # 1. Дерево
    tree = build_tree(root_path)

    # 2. Содержимое файлов
    files_content = collect_files(root_path)

    # 3. Подсчёт
    file_count = files_content.count("\n## File: ")

    # 4. Запись
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tree)
        f.write(files_content)

    size_kb = output_path.stat().st_size / 1024
    print(f"✅ Готово!")
    print(f"   Файлов: {file_count}")
    print(f"   Размер: {size_kb:.1f} KB")
    print(f"   Результат: {output_path.name}")


if __name__ == "__main__":
    main()