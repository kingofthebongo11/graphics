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


def _add_images_from_dir(document: Document, directory: Path) -> None:
    """Добавляет все PNG изображения из каталога в документ."""
    for image_path in sorted(directory.glob("*.png")):
        document.add_picture(str(image_path))


def build_report(curves_root: Path | str) -> Path:
    """Собирает отчет по PNG файлам в каталоге Curves.

    Параметры:
        curves_root: Каталог с топ-папками.

    Возвращает:
        Путь к созданному файлу ``Report.docx``.
    """
    root = Path(curves_root)
    document = Document()

    for top_path in sorted(filter(Path.is_dir, root.iterdir())):
        document.add_heading(_format_section_title(top_path.name), level=1)
        for analysis_dir in sorted(filter(Path.is_dir, top_path.iterdir())):
            document.add_heading(analysis_dir.name, level=2)
            _add_images_from_dir(document, analysis_dir)

    output_path = root / "Report.docx"
    document.save(str(output_path))
    return output_path


if __name__ == "__main__":
    build_report(Path(__file__).resolve().parent / "Curves")
