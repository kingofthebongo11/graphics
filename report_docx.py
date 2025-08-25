"""Формирование отчета в формате DOCX."""

from __future__ import annotations

from pathlib import Path
from docx import Document


def _format_section_title(folder_name: str) -> str:
    """Форматирует название топ-папки для заголовка раздела."""
    first, *rest = folder_name.split("-", 1)
    if rest:
        return f"{first} ({rest[0]})"
    return first


def build_report(curves_root: Path | str) -> Path:
    """Собирает отчет по PNG файлам в каталоге Curves.

    Для каждой топ-папки создаёт заголовок первого уровня и добавляет
    все найденные в ней графики (PNG) из вложенных каталогов.

    Параметры:
        curves_root: Каталог с топ-папками.

    Возвращает:
        Путь к созданному файлу ``Report.docx``.
    """
    root = Path(curves_root)
    document = Document()

    for top_path in sorted(filter(Path.is_dir, root.iterdir())):
        document.add_heading(_format_section_title(top_path.name), level=1)
        for image_path in sorted(top_path.rglob("*.png")):
            document.add_picture(str(image_path))

    output_path = root / "Report.docx"
    document.save(str(output_path))
    return output_path


if __name__ == "__main__":
    build_report(Path(__file__).resolve().parent / "Curves")
