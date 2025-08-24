import re
from pathlib import Path

INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1f]'

def safe_name(name: str) -> str:
    """Удаляет недопустимые для Windows символы из ``name``.

    Русские буквы и пробелы сохраняются. Также удаляются символы
    ``<>:"/\\|?*`` и управляющие символы. В конце убираются пробелы
    и точки, чтобы имя было совместимо с Windows.
    """
    sanitized = re.sub(INVALID_CHARS, '', name)
    sanitized = sanitized.rstrip(' .')
    return sanitized


def make_curve_path(base_project_dir: str, top: str, analysis: str, id_: str, ext: str) -> Path:
    """Формирует путь для сохранения файлов анализа.

    :param base_project_dir: базовая директория проекта
    :param top: верхний уровень (TOP)
    :param analysis: тип анализа
    :param id_: идентификатор
    :param ext: расширение файла без точки или с точкой
    :return: объект :class:`Path` c безопасным путём
    """
    ext = ext.lstrip('.')
    safe_top = safe_name(top)
    safe_analysis = safe_name(analysis)
    safe_id = safe_name(id_)
    return Path(base_project_dir) / 'curves' / safe_top / safe_analysis / f"{safe_id}.{ext}"
