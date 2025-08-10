class FigureNames:
    def __init__(self, name):
        self.name = name
        self.axes = ['X', 'Y', 'Z', 'XR', 'YR', 'ZR']

    def generate_filename(self):
        names = {}
        # Генерация словаря для X, Y, Z и соответствующих процентов и частот
        for axis in self.axes:
            names[f'pr{axis}mass'] = f'Масса в процентах по {axis}'
            names[f'totalpr{axis}mass'] = f'Общая собранная масса в процентах по {axis}'
            names[f'{axis}mass'] = f'Масса по {axis}'
            names[f'{axis}eig'] = f'Частота по максимальному вкладу по {axis}'
            names[f'{axis}N'] = f'Номер частоты по максимальному вкладу по {axis}'
        return names.get(self.name, 'Неизвестное имя')

    def generate_plot_title(self):
        return self.generate_filename()

    def generate_plot_ylabel(self):

        if any(self.name == f'pr{axis}mass' for axis in self.axes):
            return 'Масса, %'
        elif any(self.name == f'totalpr{axis}mass' for axis in self.axes):
            return 'Общая собранная масса, %'
        elif any(self.name == f'{axis}mass' for axis in self.axes):
            return 'Масса, кг'
        elif any(self.name == f'{axis}eig' for axis in self.axes):
            return 'Частота ${f}_{\mathit{1}}$, Гц'
        elif any(self.name == f'{axis}N' for axis in self.axes):
            return 'Номер частоты'
        else:
            return 'Неизвестное имя'
