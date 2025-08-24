from tkinter import filedialog, messagebox
from logging_utils import get_logger

logger = get_logger(__name__)


def ask_file() -> str:
    """Открывает диалог выбора файла."""
    path = filedialog.askopenfilename()
    if not path:
        logger.info("Файл не выбран")
    return path


def ask_directory() -> str:
    """Открывает диалог выбора папки."""
    path = filedialog.askdirectory()
    if not path:
        logger.info("Папка не выбрана")
    return path


def show_error(title: str, message: str) -> None:
    """Показывает сообщение об ошибке и логирует его."""
    logger.error("%s: %s", title, message)
    messagebox.showerror(title, message)
