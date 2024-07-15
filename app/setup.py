import sys
from cx_Freeze import setup, Executable

# Определение основного файла
filename = 'main.py'

# Создание исполняемого файла
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(script=filename, base=base)

# Конфигурация сборки
build_exe_options = {
    'include_files': [
        'ui/',
        'resources/',
    ],
    'packages': [
        'PyQt5',
    ],
    'excludes': [],  # Можно добавить сюда модули, которые не нужны в сборке
}

# Настройка сборки
setup(
    name='ClickMe',
    version='1.0',
    description='Clicker-Novel Game',
    options={
        'build_exe': build_exe_options,
    },
    executables=[exe]
)
