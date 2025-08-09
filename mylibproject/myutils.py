import ctypes

def to_percent(y, pos):
    return f"{y:.2f}%"  # Форматирование с двумя знаками после запятой

def is_russian_layout():
    """Проверяет, активна ли русская раскладка."""
    # Получаем текущую раскладку клавиатуры
    layout = ctypes.windll.user32.GetKeyboardLayout(0)
    return (layout & 0xFFFF) == 0x0419  # 0x0419 — это код для русской раскладки
